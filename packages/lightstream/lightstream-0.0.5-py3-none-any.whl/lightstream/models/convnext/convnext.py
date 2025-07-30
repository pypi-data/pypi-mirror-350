import torch
import torch.nn as nn
import torchvision

from torchmetrics import MetricCollection
from lightstream.modules.imagenet_template import ImageNetClassifier
from torchvision.models import convnext_tiny, convnext_small


def _toggle_stochastic_depth(model, training=False):
    for m in model.modules():
        if isinstance(m, torchvision.ops.StochasticDepth):
            m.training = training


def _set_layer_scale(model, val=1.0):
    for x in model.modules():
        if hasattr(x, "layer_scale"):
            x.layer_scale.data.fill_(val)


class StreamingConvnext(ImageNetClassifier):
    model_choices = {"convnext_tiny": convnext_tiny, "convnext_small": convnext_small}

    def __init__(
        self,
        model_name: str,
        tile_size: int,
        loss_fn: torch.nn.functional,
        train_streaming_layers: bool = True,
        use_stochastic_depth: bool = False,
        metrics: MetricCollection | None = None,
        **kwargs,
    ):
        assert model_name in list(StreamingConvnext.model_choices.keys())

        self.model_name = model_name
        self.use_stochastic_depth = use_stochastic_depth

        network = StreamingConvnext.model_choices[model_name](weights="DEFAULT")
        stream_network, head = network.features, torch.nn.Sequential(network.avgpool, network.classifier)
        self._get_streaming_options(**kwargs)

        super().__init__(
            stream_network,
            head,
            tile_size,
            loss_fn,
            train_streaming_layers=train_streaming_layers,
            metrics=metrics,
            **self.streaming_options,
        )

        # By default, the after_streaming_init callback turns sd off
        _toggle_stochastic_depth(self.stream_network.stream_module, training=self.use_stochastic_depth)

    def _get_streaming_options(self, **kwargs):
        """Set streaming defaults, but overwrite them with values of kwargs if present."""

        streaming_options = {
            "verbose": True,
            "copy_to_gpu": False,
            "statistics_on_cpu": True,
            "normalize_on_gpu": True,
            "mean": [0.485, 0.456, 0.406],
            "std": [0.229, 0.224, 0.225],
            "before_streaming_init_callbacks": [_set_layer_scale],
            "after_streaming_init_callbacks": [_toggle_stochastic_depth]
        }
        self.streaming_options = {**streaming_options, **kwargs}


if __name__ == "__main__":
    print(" is cuda available? ", torch.cuda.is_available())
    img = torch.rand((1, 3, 4160, 4160)).to("cuda")
    network = StreamingConvnext(
        "convnext_tiny",
        4800,
        nn.MSELoss,
        use_stochastic_depth=False,
        mean=[0, 0, 0],
        std=[1, 1, 1],
        normalize_on_gpu=False,
    )
    network.to("cuda")
    network.stream_network.device = torch.device("cuda")

    network.stream_network.mean = network.stream_network.mean.to("cuda")
    network.stream_network.std = network.stream_network.std.to("cuda")

    out_streaming = network(img)

    network.disable_streaming_hooks()
    normal_net = network.stream_network.stream_module
    out_normal = normal_net(img)
    out_final = network.head(out_normal)
    diff = out_streaming - out_final
    print(diff.max())
