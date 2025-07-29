from tkinter import E
from .activations import Activation
from .layers import ConvLayer, DenseLayer, FlattenLayer, RNNLayer
from .loss import (
    BCEWithLogitsLoss,
    CrossEntropyLoss,
    MeanAbsoluteErrorLoss,
    MeanSquaredErrorLoss,
    HuberLoss,
)
from .neuralNetworkBase import NeuralNetworkBase
from .neuralNetworkBaseBackend import BaseBackendNeuralNetwork
from .optimizers import AdadeltaOptimizer, AdamOptimizer, SGDOptimizer
from .schedulers import lr_scheduler_exp, lr_scheduler_plateau, lr_scheduler_step

__all__ = [
    "AdamOptimizer",
    "SGDOptimizer",
    "AdadeltaOptimizer",
    "lr_scheduler_exp",
    "lr_scheduler_plateau",
    "lr_scheduler_step",
    "CrossEntropyLoss",
    "BCEWithLogitsLoss",
    "MeanSquaredErrorLoss",
    "MeanAbsoluteErrorLoss",
    "HuberLoss",
    "DenseLayer",
    "FlattenLayer",
    "ConvLayer",
    "RNNLayer",
    "Activation",
    "NeuralNetworkBase",
    "BaseBackendNeuralNetwork",
]

try:
    from .layers_jit import JITConvLayer, JITDenseLayer, JITFlattenLayer, JITRNNLayer
    from .loss_jit import (
        JITBCEWithLogitsLoss,
        JITCrossEntropyLoss,
        JITMeanSquaredErrorLoss,
        JITMeanAbsoluteErrorLoss,
        JITHuberLoss,
    )
    from .neuralNetworkNumbaBackend import NumbaBackendNeuralNetwork
    from .numba_utils import *
    from .optimizers_jit import JITAdadeltaOptimizer, JITAdamOptimizer, JITSGDOptimizer

    __all__.extend(
        [
            "JITAdamOptimizer",
            "JITSGDOptimizer",
            "JITAdadeltaOptimizer",
            "JITBCEWithLogitsLoss",
            "JITCrossEntropyLoss",
            "JITMeanSquaredErrorLoss",
            "JITMeanAbsoluteErrorLoss",
            "JITHuberLoss",
            "JITDenseLayer",
            "JITFlattenLayer",
            "JITConvLayer",
            "JITRNNLayer",
            "NumbaBackendNeuralNetwork",
        ]
    )
except Exception as _e:
    pass

try:
    from .layers_cupy import CuPyActivation, CuPyDenseLayer
    from .loss_cupy import CuPyBCEWithLogitsLoss, CuPyCrossEntropyLoss
    from .neuralNetworkCuPyBackend import CuPyBackendNeuralNetwork
    from .optimizers_cupy import (
        CuPyAdadeltaOptimizer,
        CuPyAdamOptimizer,
        CuPySGDOptimizer,
    )

    __all__.extend(
        [
            "CuPyBackendNeuralNetwork",
            "CuPyActivation",
            "CuPyDenseLayer",
            "CuPyAdamOptimizer",
            "CuPySGDOptimizer",
            "CuPyAdadeltaOptimizer",
            "CuPyBCEWithLogitsLoss",
            "CuPyCrossEntropyLoss",
            "CuPyDenseLayer",
        ]
    )
except Exception as _e:
    pass
