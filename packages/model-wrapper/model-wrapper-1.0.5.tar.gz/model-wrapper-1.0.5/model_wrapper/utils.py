import os
from typing import Collection, List, Tuple, Union
from functools import reduce
import numpy as np
import torch


def get_device(device: Union[str, int, torch.device] = "auto"):
    if isinstance(device, str):
        device = device.lower()
        assert device in {"auto", "cpu", "cuda"} or device.startswith("cuda:")
        if device == "auto":
            return torch.device("cuda" if torch.cuda.is_available() else "cpu")
        return torch.device(device)

    if isinstance(device, torch.device):
        return device

    if isinstance(device, int):
        return torch.device(f"cuda:{device}")

    raise ValueError(f"device: {device} is not supported")


def is_gpu(device: torch.device) -> bool:
    return "cpu" != device.type.lower()


def get_workers(num_data: int, batch_size: int, train: bool = True) -> int:
    cpu_count = os.cpu_count()
    half_steps = round(num_data / batch_size / 2)
    if train:
        return max(2, min(8, half_steps, cpu_count // 2))  # 2 ~ 8
    return min(4, half_steps, cpu_count // 4)  # 0 ~ 4


def is_float(x) -> bool:
    if isinstance(x, (Collection, np.ndarray)):
        return is_float(x[0])
    return isinstance(
        x,
        (
            float,
            # np.float_, # 'np.float_' was removed in the NumPy 2.0 release. Use 'np.float64` instead.
            np.float16,
            np.float32,
            np.float64,
            # np.float128, # numpy 1.25.0 后不支持
            np.half,
            np.single,
            np.double,
            np.longdouble,
            np.csingle,
            np.cdouble,
            np.clongdouble,
        ),
    )


def convert_to_tensor(x, start_dim=1) -> torch.Tensor:
    if 1 == start_dim:
        return (
            torch.from_numpy(x.astype(np.float32) if isinstance(x, np.ndarray) else np.array(x, np.float32))
            if is_float(x[0])
            else torch.from_numpy(x if isinstance(x, np.ndarray) else np.array(x, np.int64))
        )
    
    return (
        torch.from_numpy(x.astype(np.float32) if isinstance(x, np.ndarray) else np.array(x, np.float32))
        if is_float(x[0][0])
        else torch.from_numpy(x if isinstance(x, np.ndarray) else np.array(x, np.int64))
    )


def convert_to_long_tensor(y: Union[torch.Tensor, np.ndarray, List]) -> torch.LongTensor:
    if isinstance(y, torch.Tensor):
        return y.long()
    
    if isinstance(y, np.ndarray):
        return torch.from_numpy(y.astype(np.int64))
    
    return torch.from_numpy(np.array(y, np.int64))


def convert_data(X, y) -> Tuple[torch.Tensor, torch.Tensor]:
    if isinstance(X, (List, np.ndarray)):
        X = convert_to_tensor(X, 2)
    if isinstance(y, (List, np.ndarray)):
        y = convert_to_tensor(y)
    return X, y


def cal_count(y) -> int:
    shape = y.shape
    if len(shape) == 1:
        return shape[0]
    return reduce(lambda x1, x2: x1 * x2, shape)


def acc_predict(logits: torch.Tensor, threshold: float = 0.5) -> np.ndarray:
    logits = logits.numpy()
    shape = logits.shape
    shape_len = len(shape)
    if (shape_len == 2 and shape[1] > 1) or shape_len > 2:
        # 多分类 logits：(N, num_classes) 或 (N, K, num_classes)
        return logits.argmax(-1)
    else:
        # 二分类
        if shape_len == 2:
            # (N, 1)
            logits = logits.ravel()  # (N,) 一维
        return np.where(logits >= threshold, 1, 0).astype(np.int64)


def cal_correct(
    logits: torch.Tensor, y: torch.Tensor, threshold: float = 0.5
) -> np.int64:
    # logits 与 y 的形状必须相同，且大于1个维度（因为一个维度时可能是二分类概率），直接判断相等为正确的
    if (logits.shape == y.shape or len(logits.shape) == len(y.shape)) and len(y.shape) > 1:
        return (logits.cpu().numpy() == y[:, :logits.shape[1]].cpu().numpy()).sum()
    return (acc_predict(logits.cpu(), threshold).reshape(y.shape) == y.cpu().numpy()).sum()


def get_early_stopping_rounds(epochs):
    if epochs <= 10:
        return max(2, int(0.2 * epochs))
    if epochs <= 50:
        return min(10, int(0.2 * epochs))
    return max(10, int(0.1 * epochs))


def is_improve(best_score, score, min_loss, loss, eps):
    return score > best_score or (score == best_score and min_loss - loss > eps)

def is_improve_loss(best_score, score, min_loss, loss, eps):
    return loss < min_loss or (loss == min_loss and score - best_score > eps)

def is_early_stopping(epoch, cnt, early_stopping_rounds, min_rounds=3):
    return cnt >= early_stopping_rounds and epoch >= min(min_rounds, early_stopping_rounds)
