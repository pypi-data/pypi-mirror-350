from model_wrapper.training import predict_dataset, acc_predict_dataset
from model_wrapper.wrapper import (
    ModelWrapper,
    FastModelWrapper,
    FastModelWrapper as SimpleModelWrapper,
    SplitModelWrapper,
    ClassifyModelWrapper,
    FastClassifyModelWrapper,
    FastClassifyModelWrapper as SimpleClassifyModelWrapper,
    SplitClassifyModelWrapper,
    RegressModelWrapper,
    FastRegressModelWrapper,
    FastRegressModelWrapper as SimpleRegressModelWrapper,
    SplitRegressModelWrapper,
)

__all__ = [
    "ModelWrapper",
    "FastModelWrapper",
    "SimpleModelWrapper",
    "SplitModelWrapper",
    "ClassifyModelWrapper",
    "FastClassifyModelWrapper",
    "SimpleClassifyModelWrapper",
    "SplitClassifyModelWrapper",
    "RegressModelWrapper",
    "FastRegressModelWrapper",
    "SimpleRegressModelWrapper",
    "SplitRegressModelWrapper",
    "predict_dataset",
    "acc_predict_dataset",
]
