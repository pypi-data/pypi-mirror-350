import numpy as np
import torch
from torch import nn
from torch import optim
from pathlib import Path
from typing import Union, List, Tuple, Collection, Optional, Callable
from sklearn.model_selection import train_test_split
from torch.nn import functional as F
from torch.optim.lr_scheduler import LRScheduler
from torch.utils.data import DataLoader, Dataset, TensorDataset, Sampler, WeightedRandomSampler
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    classification_report,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    mean_absolute_percentage_error
)

from model_wrapper import log_utils
from model_wrapper.utils import convert_to_tensor, convert_data, acc_predict, get_device, convert_to_long_tensor
from model_wrapper.training import (
    predict_dataset,
    acc_predict_dataset,
    evaluate,
    Trainer,
    EvalTrainer,
    acc_evaluate,
    ClassTrainer,
    EvalClassTrainer,
    r2_evaluate,
    RegressTrainer,
    EvalRegressTrainer,
)
from model_wrapper.dataset import ListDataset
from model_wrapper.collator  import ListTensorCollator

class ModelWrapper:
    """
    Examples
    --------
    >>> model_wrapper = ModelWrapper(model)
    >>> model_wrapper.train(train_set, val_set, collate_fn)
    >>> model_wrapper.logits(X_test)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        device: Union[str, int, torch.device] = "auto",
    ):
        self.device = get_device(device)
        if isinstance(model_or_path, nn.Module):
            model_or_path = model_or_path.to(self.device)
            self.model, self.best_model = model_or_path, model_or_path
        elif isinstance(model_or_path, (str, Path)):
            self.model = torch.load(model_or_path, map_location=self.device, weights_only=False)
            self.best_model = self.model

    def train(
        self,
        train_set: Dataset,
        val_set: Dataset = None,
        collate_fn: Callable = None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        sampler: Sampler = None,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
    ) -> dict:
        if val_set:
            trainer = EvalTrainer(
                epochs,
                optimizer,
                scheduler,
                lr,
                T_max,
                batch_size,
                eval_batch_size,
                num_workers,
                num_eval_workers,
                pin_memory,
                pin_memory_device,
                persistent_workers,
                early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
                print_per_rounds,
                drop_last,
                checkpoint_per_rounds,
                checkpoint_name,
                self.device,
            )
            self.best_model, histories = trainer.train(
                self.model, train_set, val_set, collate_fn, sampler, show_progress, eps
            )
        else:
            trainer = Trainer(
                epochs,
                optimizer,
                scheduler,
                lr,
                T_max,
                batch_size,
                num_workers,
                pin_memory,
                pin_memory_device,
                persistent_workers,
                early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
                print_per_rounds,
                drop_last,
                checkpoint_per_rounds,
                checkpoint_name,
                self.device,
            )
            self.best_model, histories = trainer.train(
                self.model, train_set, collate_fn, show_progress, eps
            )
        return histories

    def logits(self, X: Union[torch.Tensor, np.ndarray, List, Tuple], batch_size=128) -> torch.Tensor:
        self.best_model.eval()
        # 多个 X 值，用tuple、set或list封装, 如果是list, 其元素是torch.Tensor或numpy.ndarray
        if is_multi_value(X):
            size = len(X[0])
            X = tuple((x if torch.is_tensor(x) else convert_to_tensor(x)).to(self.device) for x in X)
            if size >= (batch_size << 1):
                chunks = size // batch_size if size % batch_size == 0 else size // batch_size + 1
                X = [torch.chunk(x, chunks, dim=0) for x in X]
                with torch.inference_mode():
                    preds = [self.best_model(*x) for x in zip(*X)]
                return torch.cat(preds, dim=0)
            
            with torch.inference_mode():
                return self.best_model(*X)

        # 只有一个 X 值
        size = len(X)
        if isinstance(X, (List, np.ndarray)):
            X = convert_to_tensor(X, 2).to(self.device)
        
        if size >= (batch_size << 1):
            chunks = size // batch_size if size % batch_size == 0 else size // batch_size + 1
            with torch.inference_mode():
                preds = [self.best_model(x) for x in torch.chunk(X, chunks, dim=0)]
            return torch.cat(preds, dim=0)

        with torch.inference_mode():
            return self.best_model(X.to(self.device))

    def evaluate(
        self, dataset: Dataset, batch_size=128, num_workers: int = 0, collate_fn: Callable = None
    ) -> float:
        """
        This method is used to evaluate the model's performance on a validation dataset.
        It returns the loss value as a metric of performance.

        Parameters:
        - dataset: Dataset, the validation dataset, which is an instance of the Dataset class.
        - batch_size: int, default 128, the number of samples per batch during evaluation.
        - num_workers: int, default 0, the number of subprocesses to use for data loading.
        - collate_fn: function, default None, a function to merge samples into a batch.

        Returns:
        - float: The loss value representing the model's performance on the validation dataset.
        """
        # Initialize the DataLoader for the validation dataset
        val_loader = DataLoader(
            dataset=dataset,
            batch_size=batch_size,
            num_workers=num_workers,
            collate_fn=collate_fn,
        )
        # Call the evaluate function to calculate and return the loss
        return evaluate(self.best_model, val_loader, self.device, is_parallel=isinstance(self.best_model, nn.DataParallel))

    def save(
        self,
        best_model_path: Union[str, Path] = "./best_model.pt",
        last_model_path: Union[str, Path] = "./last_model.pt",
        mode: str = "both",
    ):
        """
        Saves the model based on the specified mode.

        This function saves the model to the specified path(s) according to the `mode` parameter.
        It supports saving either the best model, the last model, or both, providing flexibility
        in model management during training or evaluation processes.

        :param best_model_path: The file path for saving the best model. Defaults to "./best_model.pt".
        :param last_model_path: The file path for saving the last model. Defaults to "./last_model.pt".
        :param mode: The mode for saving the model. Can be "both", "best", or "last". Defaults to "both".
        :return: None
        """
        # Ensure the mode parameter is valid
        assert mode in ("both", "best", "last")

        # Save the model(s) according to the specified mode
        if mode == "both":
            torch.save(self.model, last_model_path)
            torch.save(self.best_model, best_model_path)
        elif mode == "best":
            torch.save(self.best_model, best_model_path)
        elif mode == "last":
            torch.save(self.model, last_model_path)

    def save_state_dict(
        self,
        best_model_path: Union[str, Path] = "./best_model.pth",
        last_model_path: Union[str, Path] = "./last_model.pth",
        mode: str = "both",
    ):
        """
        Saves the model based on the specified mode.

        This function saves the model to the specified path(s) according to the `mode` parameter.
        It supports saving either the best model, the last model, or both, providing flexibility
        in model management during training or evaluation processes.

        :param best_model_path: The file path for saving the best model. Defaults to "./best_model.pth".
        :param last_model_path: The file path for saving the last model. Defaults to "./last_model.pth".
        :param mode: The mode for saving the model. Can be "both", "best", or "last". Defaults to "both".
        :return: None
        """
        # Ensure the mode parameter is valid
        assert mode in ("both", "best", "last")

        # Save the model(s) according to the specified mode
        if mode == "both":
            torch.save(self.model.state_dict(), last_model_path)
            torch.save(self.best_model.state_dict(), best_model_path)
        elif mode == "best":
            torch.save(self.best_model.state_dict(), best_model_path)
        elif mode == "last":
            torch.save(self.model.state_dict(), last_model_path)

    def load(self, model_path: Union[str, Path] = "./best_model.pt"):
        self.model = torch.load(model_path, map_location=self.device)
        self.best_model = self.model

    def load_state_dict(self, model_path: Union[str, Path] = "./best_model.pth"):
        state_dict = torch.load(model_path, map_location=self.device, weights_only=True)
        self.model.load_state_dict(state_dict)
        self.best_model.load_state_dict(state_dict)


class FastModelWrapper(ModelWrapper):
    """
    Examples
    --------
    >>> model_wrapper = FastModelWrapper(model)
    >>> model_wrapper.train(X, y, val_data, collate_fn)
    >>> model_wrapper.logits(X_test)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(model_or_path, device)

    def train(
        self,
        X: Union[torch.Tensor, np.ndarray, List, Tuple],
        y: Union[torch.Tensor, np.ndarray, List],
        val_data: Tuple[
            Union[torch.Tensor, np.ndarray, List], Union[torch.Tensor, np.ndarray, List]
        ] = None,
        collate_fn: Callable = None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        sampler: Sampler = None,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
    ) -> dict:
        if val_data:
            train_set, val_set, collate_fn = get_dataset2_collate_fn(X, y, val_data)
        else:
            val_set = None
            train_set, collate_fn = get_dataset_collate_fn(X, y)

        return super().train(train_set, val_set, collate_fn, epochs, optimizer, scheduler, lr, T_max,
                                batch_size, eval_batch_size, sampler, num_workers, num_eval_workers, pin_memory,
                                pin_memory_device, persistent_workers, early_stopping_rounds, print_per_rounds, 
                                drop_last, checkpoint_per_rounds, checkpoint_name, show_progress, eps=eps)

    def evaluate(
        self,
        X: Union[torch.Tensor, np.ndarray, List, Tuple],
        y: Union[torch.LongTensor, np.ndarray, List],
        batch_size=128,
        num_workers: int = 0,
        collate_fn: Callable = None,
    ) -> float:
        """Return loss"""
        X, y = convert_data(X, y)
        val_set = TensorDataset(X, y)
        return super().evaluate(val_set, batch_size, num_workers, collate_fn)


class SplitModelWrapper(FastModelWrapper):
    """
    Examples
    --------
    >>> model_wrapper = SplitModelWrapper(model, classes=classes)
    >>> model_wrapper.train(X, y, val_size=0.2, collate_fn)
    >>> model_wrapper.predict(X_test)
    >>> model_wrapper.evaluate(X_test, y_test)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(model_or_path, device)

    def train(
        self,
        X: Union[torch.Tensor, np.ndarray, List, Tuple],
        y: Union[torch.LongTensor, np.ndarray, List],
        val_size=0.2,
        random_state=None,
        collate_fn: Callable = None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        sampler: Sampler = None,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
    ) -> dict:
        if 0.0 < val_size < 1.0:
            X_train, X_test, y_train, y_test = split_fn(X, y, test_size=val_size, random_state=random_state)
            val_data = (X_test, y_test)
        else:
            val_data = None
            X_train, y_train = X, y

        return super().train(X_train, y_train, val_data, collate_fn, epochs, optimizer, scheduler, lr, T_max,
                            batch_size, eval_batch_size, sampler, num_workers, num_eval_workers, pin_memory,
                            pin_memory_device, persistent_workers, early_stopping_rounds, print_per_rounds, 
                            drop_last, checkpoint_per_rounds, checkpoint_name, show_progress, eps)
    

class ClassifyModelWrapper(ModelWrapper):
    """
    Examples
    --------
    >>> model_wrapper = ClassifyModelWrapper(model, classes=classes)
    >>> model_wrapper.train(train_set, val_set, collate_fn)
    >>> model_wrapper.predict(X_test)
    >>> model_wrapper.evaluate(test_set, collate_fn=collate_fn)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        classes: Collection[str] = None,
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(model_or_path, device)
        self.classes = classes

    def train(
        self,
        train_set: Dataset,
        val_set: Dataset = None,
        collate_fn: Callable = None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        sampler: Sampler = None,
        weight: Union[torch.Tensor, np.ndarray, List] = None,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
        monitor: str = "accuracy"
    ) -> dict:
        if weight is not None:
            if isinstance(weight, list):
                weight = torch.from_numpy(np.array(weight, dtype=np.float32))
            elif isinstance(weight, np.ndarray):
                weight = torch.from_numpy(weight).float()

        if val_set:
            trainer = EvalClassTrainer(
                epochs,
                optimizer,
                scheduler,
                lr,
                T_max,
                batch_size,
                eval_batch_size,
                num_workers,
                num_eval_workers,
                pin_memory,
                pin_memory_device,
                persistent_workers,
                early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
                print_per_rounds,
                drop_last,
                checkpoint_per_rounds,
                checkpoint_name,
                self.device,
            )
            self.best_model, histories = trainer.train(
                self.model, train_set, val_set, collate_fn, show_progress, sampler, weight, eps, monitor
            )
        else:
            trainer = ClassTrainer(
                epochs,
                optimizer,
                scheduler,
                lr,
                T_max,
                batch_size,
                num_workers,
                pin_memory,
                pin_memory_device,
                persistent_workers,
                early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
                print_per_rounds,
                drop_last,
                checkpoint_per_rounds,
                checkpoint_name,
                self.device,
            )
            self.best_model, histories = trainer.train(
                self.model, train_set, collate_fn, show_progress, sampler, weight, eps, monitor
            )
        return histories

    def train_evaluate(
        self,
        train_set: Dataset,
        val_set: Dataset,
        collate_fn: Callable = None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        sampler: Sampler = None,
        weight: Union[torch.Tensor, np.ndarray, List] = None,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
        monitor: str = "accuracy",
        verbose=True,
        threshold: float = 0.5,
        target_names: List[str] = None,
        num_classes: int = None,
    ) -> Tuple[dict, dict]:
        """
        训练并评估模型。
    
        该方法首先对模型进行训练，然后使用训练好的模型对验证集进行预测，并计算预测结果的性能指标。
    
        参数:
        - self: 模型实例。
        - train_set: 训练数据集。
        - val_set: 验证数据集。
        - collate_fn: 如何合并样本的函数。
        - epochs: 训练的轮数。
        - optimizer: 优化器类型或实例。
        - scheduler: 学习率调度器。
        - lr: 初始学习率。
        - T_max: 学习率余弦退火周期的上限。
        - batch_size: 训练时的批次大小。
        - eval_batch_size: 验证时的批次大小。
        - num_workers: 数据加载时使用的子进程数。
        - num_eval_workers: 验证时数据加载使用的子进程数。
        - pin_memory: 是否使用固定显存。
        - pin_memory_device: 固定显存的设备。
        - persistent_workers: 是否让数据加载子进程在整个训练过程中保持存活。
        - early_stopping_rounds: 如果在指定轮数内验证集性能没有提升则提前终止训练。
        - print_per_rounds: 每隔多少轮打印一次训练信息。
        - drop_last: 是否在数据集大小不能被批次大小整除时丢弃最后一个不完整的批次。
        - checkpoint_per_rounds: 每隔多少轮保存一次模型检查点。
        - checkpoint_name: 模型检查点的文件名。
        - show_progress: 是否显示训练进度。
        - eps: 用于避免除零错误的小量。
        - monitor: 监控的性能指标。
        - verbose: 是否详细打印评估信息。
        - threshold: 预测概率的阈值。
        - target_names: 目标变量的名称列表。
        - num_classes: 类别数量。
    
        返回:
        - histories: 训练历史记录。
        - metrics: 验证集上的性能指标。
        """
        # 训练模型并获取训练历史记录
        histories = ClassifyModelWrapper.train(
            self,
            train_set,
            val_set,
            collate_fn,
            epochs,
            optimizer,
            scheduler,
            lr,
            T_max,
            batch_size,
            eval_batch_size,
            sampler,
            weight,
            num_workers,
            num_eval_workers,
            pin_memory,
            pin_memory_device,
            persistent_workers,
            early_stopping_rounds,
            print_per_rounds,
            drop_last,
            checkpoint_per_rounds,
            checkpoint_name,
            show_progress,
            eps,
            monitor,
        )
    
        # 使用训练好的模型对验证集进行预测
        preds, labels = acc_predict_dataset(self.best_model, val_set, batch_size, threshold, num_workers, collate_fn, self.device)
        preds, labels = preds.ravel(), labels.ravel()
    
        # 计算类别数量
        num_classes = num_classes or self._cal_num_classes(target_names) or len(np.unique(labels))
    
        # 计算性能指标
        metrics = self._cal_metrics(labels, preds, num_classes)
    
        # 打印性能指标
        if verbose:
            self._print_metrics(metrics, labels, preds, target_names)
    
        return histories, metrics

    def predict(
        self, X: Union[torch.Tensor, np.ndarray, List, Tuple], batch_size=128, threshold: float = 0.5
    ) -> np.ndarray:
        """
        :param X:
        :param batch_size:
        :param threshold: 二分类且模型输出为一维概率时生效
        """
        logits = self.logits(X, batch_size)
        return acc_predict(logits.cpu(), threshold)

    def predict_classes(
        self, X: Union[torch.Tensor, np.ndarray, List, Tuple], batch_size=128, threshold: float = 0.5
    ) -> list:
        """
        :param X:
        :param threshold: 二分类且模型输出为一维概率时生效
        """
        pred = self.predict(X, batch_size, threshold)
        return self._predict_classes(pred.ravel())

    def _predict_classes(self, pred: np.ndarray) -> np.ndarray:
        if self.classes:
            return [self.classes[i] for i in pred]
        else:
            log_utils.warn("Warning: classes not be specified")
            return pred

    def predict_proba(
        self, X: Union[torch.Tensor, np.ndarray, List, Tuple], batch_size=128, threshold: float = 0.5
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        :param X:
        :param threshold: 二分类且模型输出为一维概率时生效
        """
        logits = self.logits(X, batch_size)
        return self._proba(logits, threshold)

    @staticmethod
    def _proba(
        logits: torch.Tensor, threshold: float = 0.5
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        :param logits:
        :param threshold: 二分类且模型输出为一维概率时生效
        """
        shape = logits.shape
        shape_len = len(shape)
        if (shape_len == 2 and shape[1] > 1) or shape_len > 2:
            # 多分类
            result = F.softmax(logits, dim=-1).max(-1)
            return result.indices.numpy(), result.values.numpy()
        else:
            # 二分类
            logits = logits.numpy()
            if shape_len == 2:
                logits = logits.ravel()
            return (np.where(logits >= threshold, 1, 0).astype(np.int64), 
                    np.where(logits >= 0.5, logits, 1 - logits))

    def predict_classes_proba(
        self, X: Union[torch.Tensor, np.ndarray, List, Tuple], batch_size=128, threshold: float = 0.5
    ) -> Tuple[list, np.ndarray]:
        """
        :param X:
        :param threshold: 二分类且模型输出为一维概率时生效
        """
        indices, values = self.predict_proba(X, batch_size, threshold)
        return self._predict_classes(indices.ravel()), values

    def acc(
        self,
        dataset: Dataset,
        batch_size=128,
        num_workers: int = 0,
        collate_fn: Callable = None,
        threshold: float = 0.5,
    ) -> float:
        """
        :param dataset:
        :param threshold: 二分类且模型输出为一维概率时生效
        :return accuracy
        """
        val_loader = DataLoader(
            dataset=dataset,
            batch_size=batch_size,
            num_workers=num_workers,
            collate_fn=collate_fn,
        )
        _, acc = acc_evaluate(self.best_model, val_loader, self.device, None, threshold, is_parallel=isinstance(self.best_model, nn.DataParallel))
        return acc
    
    def confusion_matrix(
        self,
        dataset: Dataset,
        batch_size=128,
        num_workers: int = 0,
        collate_fn: Callable = None,
        threshold: float = 0.5,
        verbose: bool = True,
    ) -> np.ndarray:
        """返回混淆矩阵"""
        preds, labels = acc_predict_dataset(self.best_model, dataset, batch_size, threshold, num_workers, collate_fn, self.device)
        preds, labels = preds.ravel(), labels.ravel()
        cm = confusion_matrix(labels, preds)
        if verbose:
            self._print_confusion_matrix(cm)
        return cm
    
    def evaluate(
        self,
        dataset: Dataset,
        batch_size=128,
        num_workers: int = 0,
        collate_fn: Callable = None,
        threshold: float = 0.5,
        num_classes: int = None,
        verbose: bool = True,
    ) -> dict[str, float]:
        """
        :param dataset:
        :param threshold: 二分类且模型输出为一维概率时生效
        :return metrics(dict)
        """
        preds, labels = acc_predict_dataset(self.best_model, dataset, batch_size, threshold, num_workers, collate_fn, self.device)
        preds, labels = preds.ravel(), labels.ravel()
        num_classes = num_classes or self._cal_num_classes(None) or len(np.unique(labels))
        metrics = self._cal_metrics(labels, preds, num_classes)
        if verbose:
            self._print_evaluate(metrics)
            report = classification_report(labels.ravel(), preds.ravel(), target_names=self.classes)
            self._print_classification_report(report)
        return metrics

    def classification_report(
        self, 
        dataset: Dataset, 
        batch_size=128,
        num_workers: int = 0,
        collate_fn: Callable = None,
        threshold: float = 0.5,
        target_names: List[str] = None,
        verbose: bool = True,
    ) -> Union[str, dict]:
        preds, labels = acc_predict_dataset(self.best_model, dataset, batch_size, threshold, num_workers, collate_fn, self.device)
        report = classification_report(labels.ravel(), preds.ravel(), target_names=target_names or self.classes)
        if verbose:
            self._print_classification_report(report)
        return report
    
    @staticmethod
    def _cal_metrics(labels: np.ndarray, preds: np.ndarray, num_classes: int) -> dict[str, float]:
        # 如果是二分类，'binary', 否则为 'micro'
        if 2 == num_classes:
            return {
                "accuracy": accuracy_score(labels, preds),
                "precision": precision_score(labels, preds),
                "recall": recall_score(labels, preds),
                "f1": f1_score(labels, preds),
                "auc": roc_auc_score(labels, preds),
                "cm": confusion_matrix(labels, preds),
            }
        
        eye = np.eye(num_classes)
        return {
            "accuracy": accuracy_score(labels, preds),
            "precision": precision_score(labels, preds, average='micro'),
            "recall": recall_score(labels, preds, average='micro'),
            "f1": f1_score(labels, preds, average='micro'),
            "auc": roc_auc_score(eye[labels], eye[preds], multi_class='ovr'),
            "cm": confusion_matrix(labels, preds),
        }
    
    @staticmethod
    def _print_evaluate(metrics: dict[str, float]):
        print()
        print("="*4, "Metrics", "="*4)
        print(f"Accuracy: {metrics['accuracy']:.2%}")
        print(f"Precision: {metrics['precision']:.2%}")
        print(f"Recall: {metrics['recall']:.2%}")
        print(f"F1: {metrics['f1']:.2%}")
        print(f"AUC: {metrics['auc']:.2%}\n")

        ClassifyModelWrapper._print_confusion_matrix(metrics['cm'])

    @staticmethod
    def _print_classification_report(report):
        print("="*54)
        print("\t\tClassification Report")
        print("="*54)
        print(report)

    @staticmethod
    def _print_confusion_matrix(confusion_mat: np.ndarray) -> None:
        print("="*54)
        print("\t\t  Confusion Matrix")
        print("="*54)
        print(confusion_mat, "\n")
    
    def _print_metrics(self, metrics: dict[str, float], labels: np.ndarray, preds: np.ndarray, target_names: List[str]) -> None:
        self._print_evaluate(metrics)
        self._print_classification_report(classification_report(labels, preds, target_names=target_names or self.classes))

    def _cal_num_classes(self, target_names: List[str]) -> int:
        if target_names is not None:
            return len(target_names)
        elif self.classes is not None:
            return len(self.classes)
        else:
            return None

    @staticmethod
    def get_class_weights(labels: Union[torch.Tensor, np.ndarray, List]) -> np.ndarray:
        labels = _to_numpy(labels)
        return (1.0 / np.bincount(labels)).astype(np.float32)

    @staticmethod
    def get_balance_sampler(labels: Union[torch.Tensor, np.ndarray, List], return_weights: bool = False) -> Union[Sampler, Tuple[Sampler, np.ndarray]]:
        labels = _to_numpy(labels)
        weights = 1.0 / np.bincount(labels)
        sample_weights = [weights[label] for label in labels]
        sampler = WeightedRandomSampler(sample_weights, num_samples=len(sample_weights), replacement=True)
        if return_weights:
            return sampler, weights.astype(np.float32)
        return sampler
    
    @staticmethod
    def get_balance_sampler_from_weights(labels: Union[torch.Tensor, np.ndarray, List], weights: np.ndarray) -> Sampler:
        labels = _to_numpy(labels)
        sample_weights = [weights[label] for label in labels]
        return WeightedRandomSampler(sample_weights, num_samples=len(sample_weights), replacement=True)
    

class FastClassifyModelWrapper(ClassifyModelWrapper):
    """
    Examples
    --------
    >>> model_wrapper = FastClassifyModelWrapper(model, classes=classes)
    >>> model_wrapper.train(X, y val_data, collate_fn)
    >>> model_wrapper.predict(X_test)
    >>> model_wrapper.evaluate(X_test, y_test)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        classes: Collection[str] = None,
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(model_or_path, classes, device)

    def train(
        self,
        X: Union[torch.Tensor, np.ndarray, List, Tuple],
        y: Union[torch.LongTensor, np.ndarray, List],
        val_data: Tuple[
            Union[torch.Tensor, np.ndarray, List],
            Union[torch.LongTensor, np.ndarray, List],
        ] = None,
        collate_fn: Callable = None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        sampler: Union[Sampler, bool] = None,
        weight: Union[torch.Tensor, np.ndarray, List] = None,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
        monitor: str = "accuracy"
    ) -> dict:
        if isinstance(y, List):
            y = np.array(y, dtype=np.int64)

        if sampler is not None and isinstance(sampler, bool):
            if sampler:
                if weight is None:
                    sampler, weight = self.get_balance_sampler(y, return_weights=True)
                else:
                    sampler = self.get_balance_sampler_from_weights(y, weight)
            else:
                sampler = None

        if isinstance(y, np.ndarray) and y.dtype == np.int32:
            y = convert_to_long_tensor(y)

        if val_data:
            train_set, val_set, collate_fn = get_dataset2_collate_fn(X, y, val_data)
        else:
            val_set = None
            train_set, collate_fn = get_dataset_collate_fn(X, y)
        
        return super().train(train_set, val_set, collate_fn, epochs, optimizer, scheduler, lr, T_max,
                                 batch_size, eval_batch_size, sampler, weight, num_workers, num_eval_workers, pin_memory,
                                 pin_memory_device, persistent_workers, early_stopping_rounds, print_per_rounds, 
                                 drop_last, checkpoint_per_rounds, checkpoint_name, show_progress, eps, monitor)

    def train_evaluate(
        self,
        X: Union[torch.Tensor, np.ndarray, List, Tuple],
        y: Union[torch.LongTensor, np.ndarray, List],
        val_data: Tuple[
            Union[torch.Tensor, np.ndarray, List],
            Union[torch.LongTensor, np.ndarray, List],
        ],
        collate_fn: Callable = None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        sampler: Union[Sampler, bool] = None,
        weight: Union[torch.Tensor, np.ndarray, List] = None,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
        monitor: str = "accuracy",
        verbose=True,
        threshold: float = 0.5,
        target_names: List[str] = None,
        num_classes: int = None,
    ) -> Tuple[dict, dict]:
        """
        训练并评估模型。

        参数:
        - X: 训练数据的特征，可以是torch.Tensor、np.ndarray、List或Tuple。
        - y: 训练数据的标签，可以是torch.LongTensor、np.ndarray或List。
        - val_data: 验证数据的特征和标签，格式与X和y相同。
        - collate_fn: 数据加载时的批处理函数，默认为None。
        - epochs: 训练的轮数，默认为100。
        - optimizer: 优化器类型或实例，默认为None。
        - scheduler: 学习率调度器，默认为None。
        - lr: 学习率，默认为0.001。
        - T_max: 学习率调度器的最大周期数，默认为0。
        - batch_size: 训练时的批大小，默认为64。
        - eval_batch_size: 评估时的批大小，默认为128。
        - num_workers: 训练时数据加载的线程数，默认为0。
        - num_eval_workers: 评估时数据加载的线程数，默认为0。
        - pin_memory: 是否将数据加载到固定内存中，默认为False。
        - pin_memory_device: 固定内存的设备名称，默认为空字符串。
        - persistent_workers: 是否保持数据加载线程的持久性，默认为False。
        - early_stopping_rounds: 早停的轮数，默认为None。
        - print_per_rounds: 每多少轮打印一次训练信息，默认为1。
        - drop_last: 是否丢弃最后一个不完整的批次，默认为False。
        - checkpoint_per_rounds: 每多少轮保存一次模型检查点，默认为0。
        - checkpoint_name: 模型检查点的文件名，默认为"model.pt"。
        - show_progress: 是否显示训练进度，默认为True。
        - eps: 数值稳定性的小值，默认为1e-5。
        - monitor: 监控的指标，默认为"accuracy"。
        - verbose: 是否输出详细信息，默认为True。
        - threshold: 分类阈值，默认为0.5。
        - target_names: 目标类别的名称列表，默认为None。
        - num_classes: 类别数量，默认为None。

        返回:
        - histories: 训练历史记录。
        - metrics: 验证集上的性能指标。
        """
        if isinstance(y, List):
            y = np.array(y, dtype=np.int64)

        if sampler is not None and isinstance(sampler, bool):
            if sampler:
                if weight is None:
                    sampler, weight = self.get_balance_sampler(y, return_weights=True)
                else:
                    sampler = self.get_balance_sampler_from_weights(y, weight)
            else:
                sampler = None

        # 根据目标类别名称或标签数据计算类别数量
        num_classes = num_classes or self._cal_num_classes(target_names)
        
        # 根据类别数量或标签类型选择合适的数据集和批处理函数
        if (num_classes and num_classes > 2) or (isinstance(y, np.ndarray) and y.dtype in (np.int32, np.int64)):
            train_set, val_set, collate_fn = get_acc_dataset2_collate_fn(X, y, val_data)
        else:
            train_set, val_set, collate_fn = get_dataset2_collate_fn(X, y, val_data)
        
        # 调用父类的train_evaluate方法进行训练和评估
        return super().train_evaluate(
            train_set,
            val_set,
            collate_fn,
            epochs=epochs,
            optimizer=optimizer,
            scheduler=scheduler,
            lr=lr,
            T_max=T_max,
            batch_size=batch_size,
            eval_batch_size=eval_batch_size,
            sampler=sampler,
            weight=weight,
            num_workers=num_workers,
            num_eval_workers=num_eval_workers,
            pin_memory=pin_memory,
            pin_memory_device=pin_memory_device,
            persistent_workers=persistent_workers,
            early_stopping_rounds=early_stopping_rounds,
            print_per_rounds=print_per_rounds,
            drop_last=drop_last,
            checkpoint_per_rounds=checkpoint_per_rounds,
            checkpoint_name=checkpoint_name,
            show_progress=show_progress,
            eps=eps,
            monitor=monitor,
            verbose=verbose,
            threshold=threshold,
            target_names=target_names,
            num_classes=num_classes
        )
    
    def acc(
        self,
        X: Union[torch.Tensor, np.ndarray, List, Tuple],
        y: Union[torch.LongTensor, np.ndarray, List],
        batch_size=128,
        num_workers: int = 0,
        collate_fn: Callable = None,
        threshold: float = 0.5,
    ):
        """return accuracy"""
        X, y = convert_data(X, y)
        data_set = TensorDataset(X, y)
        return super().acc(
            data_set, batch_size, num_workers, collate_fn, threshold
        )   
    
    def confusion_matrix(
        self,
        X: Union[torch.Tensor, np.ndarray, List, Tuple],
        y: Union[torch.LongTensor, np.ndarray, List],
        batch_size=128,
        num_workers: int = 0,
        collate_fn: Callable = None,
        threshold: float = 0.5,
        verbose: bool = True,
    ):
        """return confusion matrix"""
        X, y = convert_data(X, y)
        data_set = TensorDataset(X, y)
        return super().confusion_matrix(
            data_set, batch_size, num_workers, collate_fn, threshold, verbose
        )
    
    def evaluate(
        self,
        X: Union[torch.Tensor, np.ndarray, List, Tuple],
        y: Union[torch.LongTensor, np.ndarray, List],
        batch_size=128,
        num_workers: int = 0,
        collate_fn: Callable = None,
        threshold: float = 0.5,
        num_classes: int = None,
        verbose: bool = True,
    ):
        """return metrics"""
        X, y = convert_data(X, y)
        data_set = TensorDataset(X, y)
        return super().evaluate(
            data_set, batch_size, num_workers, collate_fn, threshold, num_classes, verbose
        )

    def classification_report(
            self, 
            X: Union[torch.Tensor, np.ndarray, List, Tuple], 
            y: Union[torch.LongTensor, np.ndarray, List], 
            batch_size=128,
            threshold: float = 0.5,
            target_names: Optional[List] = None,
            verbose: bool = False,
    ) -> Union[str, dict]:
        y = _to_numpy(y)
        pred = self.predict(X, batch_size, threshold)
        report = classification_report(y, pred, target_names=target_names or self.classes)
        if verbose:
            self._print_classification_report(report)
        return report

        
class SplitClassifyModelWrapper(FastClassifyModelWrapper):
    """
    Examples
    --------
    >>> model_wrapper = SplitClassifyModelWrapper(model, classes=classes)
    >>> model_wrapper.train(X, y val_data, collate_fn)
    >>> model_wrapper.predict(X_test)
    >>> model_wrapper.evaluate(X_test, y_test)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        classes: Collection[str] = None,
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(model_or_path, classes, device)

    def train(
        self,
        X: Union[torch.Tensor, np.ndarray, List, Tuple],
        y: Union[torch.LongTensor, np.ndarray, List],
        val_size=0.2,
        random_state=None,
        collate_fn: Callable = None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        sampler: Union[Sampler, bool] = None,
        weight: Union[torch.Tensor, np.ndarray, List] = None,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
        monitor: str = "accuracy"
    ) -> dict:
        if 0.0 < val_size < 1.0:
            X_train, X_test, y_train, y_test = split_fn(X, y, test_size=val_size, random_state=random_state)
            val_data = (X_test, y_test)
        else:
            val_data = None
            X_train, y_train = X, y

        return super().train(X_train, y_train, val_data, collate_fn, epochs, optimizer, scheduler, lr, T_max,
                            batch_size, eval_batch_size, sampler, weight, num_workers, num_eval_workers, pin_memory,
                            pin_memory_device, persistent_workers, early_stopping_rounds, print_per_rounds, 
                            drop_last, checkpoint_per_rounds, checkpoint_name, show_progress, eps, monitor)
        
    def train_evaluate(
        self,
        X: Union[torch.Tensor, np.ndarray, List, Tuple],
        y: Union[torch.LongTensor, np.ndarray, List],
        val_size=0.2,
        random_state=None,
        collate_fn: Callable = None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        sampler: Union[Sampler, bool] = None,
        weight: Union[torch.Tensor, np.ndarray, List] = None,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
        monitor: str = "accuracy",
        verbose=True,
        threshold: float = 0.5,
        target_names: List[str] = None,
        num_classes: int = None,
    ) -> Tuple[dict, dict]:
        """
        训练并评估模型。
    
        参数:
        - X: 输入数据，可以是torch.Tensor、np.ndarray、List或Tuple类型。
        - y: 标签数据，可以是torch.LongTensor、np.ndarray或List类型。
        - val_size: 验证集的比例，默认为0.2。
        - random_state: 随机种子，用于数据分割的随机性控制。
        - collate_fn: 数据加载时的批处理函数，默认为None。
        - epochs: 训练的轮数，默认为100。
        - optimizer: 优化器类型或实例，默认为None。
        - scheduler: 学习率调度器，默认为None。
        - lr: 学习率，默认为0.001。
        - T_max: 学习率调度器的最大周期数，默认为0。
        - batch_size: 训练时的批大小，默认为64。
        - eval_batch_size: 评估时的批大小，默认为128。
        - num_workers: 训练时数据加载的线程数，默认为0。
        - num_eval_workers: 评估时数据加载的线程数，默认为0。
        - pin_memory: 是否将数据加载到固定内存中，默认为False。
        - pin_memory_device: 固定内存的设备名称，默认为空字符串。
        - persistent_workers: 是否保持数据加载的线程，默认为False。
        - early_stopping_rounds: 早停的轮数，默认为None。
        - print_per_rounds: 每隔多少轮打印一次训练信息，默认为1。
        - drop_last: 是否丢弃最后一个不完整的批次，默认为False。
        - checkpoint_per_rounds: 每隔多少轮保存一次模型，默认为0。
        - checkpoint_name: 模型保存的文件名，默认为"model.pt"。
        - show_progress: 是否显示训练进度，默认为True。
        - eps: 数值稳定性的小常数，默认为1e-5。
        - monitor: 监控的指标，默认为"accuracy"。
        - verbose: 是否打印详细信息，默认为True。
        - threshold: 分类阈值，默认为0.5。
        - target_names: 目标类别的名称列表，默认为None。
        - num_classes: 类别数量，默认为None。
    
        返回:
        - histories: 训练历史记录。
        - metrics: 验证集上的性能指标。
        """
        # 确保验证集比例在0到1之间
        assert 0.0 < val_size < 1.0
    
        # 将数据集分割为训练集和验证集
        X_train, X_test, y_train, y_test = split_fn(X, y, test_size=val_size, random_state=random_state)
    
        # 调用父类的train_evaluate方法进行训练和评估
        return super().train_evaluate(
            X_train, 
            y_train,
            (X_test, y_test),
            collate_fn,
            epochs=epochs,
            optimizer=optimizer,
            scheduler=scheduler,
            lr=lr,
            T_max=T_max,
            batch_size=batch_size,
            eval_batch_size=eval_batch_size,
            sampler=sampler,
            weight=weight,
            num_workers=num_workers,
            num_eval_workers=num_eval_workers,
            pin_memory=pin_memory,
            pin_memory_device=pin_memory_device,
            persistent_workers=persistent_workers,
            early_stopping_rounds=early_stopping_rounds,
            print_per_rounds=print_per_rounds,
            drop_last=drop_last,
            checkpoint_per_rounds=checkpoint_per_rounds,
            checkpoint_name=checkpoint_name,
            show_progress=show_progress,
            eps=eps,
            monitor=monitor,
            verbose=verbose,
            threshold=threshold,
            target_names=target_names,
            num_classes=num_classes
        )
        

class RegressModelWrapper(ModelWrapper):
    """
    Examples
    --------
    >>> model_wrapper = RegressModelWrapper(model)
    >>> model_wrapper.train(train_set, val_set, collate_fn)
    >>> model_wrapper.predict(X_test)
    >>> model_wrapper.evaluate(test_set, collate_fn=collate_fn)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(model_or_path, device)

    def train(
        self,
        train_set: Dataset,
        val_set: Dataset = None,
        collate_fn: Callable = None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        sampler: Sampler = None,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
        monitor="r2_score"
    ) -> dict:
        if val_set:
            trainer = EvalRegressTrainer(
                epochs,
                optimizer,
                scheduler,
                lr,
                T_max,
                batch_size,
                eval_batch_size,
                num_workers,
                num_eval_workers,
                pin_memory,
                pin_memory_device,
                persistent_workers,
                early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
                print_per_rounds,
                drop_last,
                checkpoint_per_rounds,
                checkpoint_name,
                self.device,
            )
            self.best_model, histories = trainer.train(
                self.model, train_set, val_set, collate_fn, sampler, show_progress, eps, monitor
            )
        else:
            trainer = RegressTrainer(
                epochs,
                optimizer,
                scheduler,
                lr,
                T_max,
                batch_size,
                num_workers,
                pin_memory,
                pin_memory_device,
                persistent_workers,
                early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
                print_per_rounds,
                drop_last,
                checkpoint_per_rounds,
                checkpoint_name,
                self.device,
            )
            self.best_model, histories = trainer.train(
                self.model, train_set, collate_fn, sampler, show_progress, eps, monitor
            )
        return histories
    
    def train_evaluate(
        self,
        train_set: Dataset,
        val_set: Dataset,
        collate_fn: Callable = None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        sampler: Sampler = None,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
        monitor="r2_score",
        verbose=True
    ) -> Tuple[dict, dict]:
        """
        训练并评估模型。

        参数:
        - train_set: 训练数据集。
        - val_set: 验证数据集。
        - collate_fn: 数据整理函数，默认为None。
        - epochs: 训练轮数，默认为100。
        - optimizer: 优化器类型或实例，默认为None。
        - scheduler: 学习率调度器，默认为None。
        - lr: 学习率，默认为0.001。
        - T_max: 学习率调度器的最大周期数，默认为0。
        - batch_size: 训练批次大小，默认为64。
        - eval_batch_size: 评估批次大小，默认为128。
        - num_workers: 训练数据加载的线程数，默认为0。
        - num_eval_workers: 评估数据加载的线程数，默认为0。
        - pin_memory: 是否将数据固定在内存中，默认为False。
        - pin_memory_device: 固定内存的设备，默认为空字符串。
        - persistent_workers: 是否保持数据加载器的线程，默认为False。
        - early_stopping_rounds: 早停轮数，默认为None。
        - print_per_rounds: 每多少轮打印一次信息，默认为1。
        - drop_last: 是否丢弃最后一个不完整的批次，默认为False。
        - checkpoint_per_rounds: 每多少轮保存一次模型，默认为0。
        - checkpoint_name: 模型保存的文件名，默认为"model.pt"。
        - show_progress: 是否显示进度条，默认为True。
        - eps: 数值稳定性参数，默认为1e-5。
        - monitor: 监控指标，默认为"r2_score"。
        - verbose: 是否打印评估结果，默认为True。

        返回值:
        - histories: 训练过程中的历史记录。
        - metrics: 评估结果。
        """
        # 调用RegressModelWrapper的train方法进行模型训练
        histories = RegressModelWrapper.train(self, train_set, val_set, collate_fn, epochs, optimizer, scheduler,
                                            lr, T_max,batch_size, eval_batch_size, sampler, num_workers, num_eval_workers, pin_memory,
                                            pin_memory_device, persistent_workers, early_stopping_rounds, print_per_rounds, 
                                            drop_last, checkpoint_per_rounds, checkpoint_name, show_progress, eps, monitor
        )
        # 调用RegressModelWrapper的evaluate方法进行模型评估
        metrics = RegressModelWrapper.evaluate(self, train_set, eval_batch_size, num_eval_workers, collate_fn, False)

        # 如果verbose为True，打印评估结果
        if verbose:
            self._print_metrics(metrics)

        return histories, metrics
    
    def predict(self, X: Union[torch.Tensor, np.ndarray, List[float], Tuple], batch_size=128) -> np.ndarray:
        return self.logits(X, batch_size).cpu().numpy()

    def mae(
        self,
        dataset: Dataset, 
        batch_size=128,
        num_workers: int = 0,
        collate_fn: Callable = None,
    ) -> Union[str, dict]:
        preds, targets = predict_dataset(self.best_model, dataset, batch_size, num_workers, collate_fn, self.device)
        return mean_absolute_error(targets.ravel(), preds.ravel())

    def mse(
        self,
        dataset: Dataset, 
        batch_size=128,
        num_workers: int = 0,
        collate_fn: Callable = None,
    ) -> Union[str, dict]:
        preds, targets = predict_dataset(self.best_model, dataset, batch_size, num_workers, collate_fn, self.device)
        return mean_squared_error(targets.ravel(), preds.ravel())

    def rmse(
        self,
        dataset: Dataset, 
        batch_size=128,
        num_workers: int = 0,
        collate_fn: Callable = None,
    ) -> float:
        return np.sqrt(self.mse(dataset, batch_size, num_workers, collate_fn))

    def mape(
        self,
        dataset: Dataset, 
        batch_size=128,
        num_workers: int = 0,
        collate_fn: Callable = None,
    ) -> Union[str, dict]:
        preds, targets = predict_dataset(self.best_model, dataset, batch_size, num_workers, collate_fn, self.device)
        return mean_absolute_percentage_error(targets.ravel(), preds.ravel())
    def r2_score(
        self, dataset: Dataset, batch_size=128, num_workers: int = 0, collate_fn: Callable = None
    ) -> float:
        """Return R2 score"""
        val_loader = DataLoader(
            dataset=dataset,
            batch_size=batch_size,
            num_workers=num_workers,
            collate_fn=collate_fn,
        )
        _, r2 = r2_evaluate(self.best_model, val_loader, self.device, is_parallel=isinstance(self.best_model, nn.DataParallel))
        return r2
    
    def evaluate(
        self, 
        dataset: Dataset, 
        batch_size=128,
        num_workers: int = 0,
        collate_fn: Callable = None,
        verbose: bool = True,
    ) -> dict[str, dict]:
        preds, targets = predict_dataset(self.best_model, dataset, batch_size, num_workers, collate_fn, self.device)
        preds = preds.ravel()
        targets = targets.ravel()
        mse = mean_squared_error(targets, preds)
        metrics = {
            "MAE": mean_absolute_error(targets, preds),
            "MSE": mse,
            "RMSE": np.sqrt(mse),
            "MAPE": mean_absolute_percentage_error(targets, preds),
            "R2": r2_score(targets, preds),
        }

        if verbose:
            self._print_metrics(metrics)
        return metrics


    @staticmethod
    def _print_metrics(metrics):
        print()
        print("="*4, "Metrics", "="*4)
        print(f'MAE: {metrics["MAE"]:.2f}')
        print(f'MSE: {metrics["MSE"]:.2f}')
        print(f'RMSE: {metrics["RMSE"]:.2f}')
        print(f'MAPE: {metrics["MAPE"]:.2f}%')
        print(f'R2: {metrics["R2"]:.2f}\n')


class FastRegressModelWrapper(RegressModelWrapper):
    """
    Examples
    --------
    >>> model_wrapper = FastRegressModelWrapper(model)
    >>> model_wrapper.train(train_set, val_set, collate_fn)
    >>> model_wrapper.predict(X_test)
    >>> model_wrapper.evaluate(test_set, collate_fn=collate_fn)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(model_or_path, device)

    def train(
        self,
        X: Union[torch.Tensor, np.ndarray, List, Tuple],
        y: Union[torch.Tensor, np.ndarray, List],
        val_data: Tuple[
            Union[torch.Tensor, np.ndarray, List], Union[torch.Tensor, np.ndarray, List]
        ] = None,
        collate_fn: Callable = None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        sampler: Sampler = None,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
        monitor="r2_score"
    ) -> dict:
        if val_data:
            train_set, val_set, collate_fn = get_dataset2_collate_fn(X, y, val_data)
        else:
            val_set = None
            train_set, collate_fn = get_dataset_collate_fn(X, y)
            
        return super().train(train_set, val_set, collate_fn, epochs, optimizer, scheduler, lr, T_max,
                            batch_size, eval_batch_size, sampler,num_workers, num_eval_workers, pin_memory,
                            pin_memory_device, persistent_workers, early_stopping_rounds, print_per_rounds, 
                            drop_last, checkpoint_per_rounds, checkpoint_name, show_progress, eps, monitor)

    def train_evaluate(
        self,
        X: Union[torch.Tensor, np.ndarray, List, Tuple],
        y: Union[torch.Tensor, np.ndarray, List],
        val_data: Tuple[Union[torch.Tensor, np.ndarray, List], Union[torch.Tensor, np.ndarray, List]],
        collate_fn: Callable = None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        sampler: Sampler = None,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
        monitor="r2_score",
        verbose=True
    ) -> Tuple[dict, dict]:
        """
        训练并评估模型。

        参数:
        - X: 训练数据的输入，可以是 torch.Tensor、np.ndarray、List 或 Tuple。
        - y: 训练数据的标签，可以是 torch.Tensor、np.ndarray 或 List。
        - val_data: 验证数据的元组，包含输入和标签，格式与 X 和 y 相同。
        - collate_fn: 数据加载时的批处理函数，默认为 None。
        - epochs: 训练的轮数，默认为 100。
        - optimizer: 优化器类型或实例，默认为 None。
        - scheduler: 学习率调度器，默认为 None。
        - lr: 学习率，默认为 0.001。
        - T_max: 学习率调度器的最大周期数，默认为 0。
        - batch_size: 训练时的批大小，默认为 64。
        - eval_batch_size: 评估时的批大小，默认为 128。
        - num_workers: 训练时数据加载的线程数，默认为 0。
        - num_eval_workers: 评估时数据加载的线程数，默认为 0。
        - pin_memory: 是否将数据加载到固定内存中，默认为 False。
        - pin_memory_device: 固定内存的设备名称，默认为空字符串。
        - persistent_workers: 是否保持数据加载线程的持久性，默认为 False。
        - early_stopping_rounds: 早停的轮数，默认为 None。
        - print_per_rounds: 每多少轮打印一次训练信息，默认为 1。
        - drop_last: 是否丢弃最后一个不完整的批次，默认为 False。
        - checkpoint_per_rounds: 每多少轮保存一次模型检查点，默认为 0。
        - checkpoint_name: 模型检查点的文件名，默认为 "model.pt"。
        - show_progress: 是否显示训练进度条，默认为 True。
        - eps: 用于数值稳定性的小值，默认为 1e-5。
        - monitor: 监控的指标，默认为 "r2_score"。
        - verbose: 是否打印详细信息，默认为 True。

        返回:
        - histories: 训练历史记录。
        - metrics: 验证集上的性能指标。
        """
        # 获取训练集、验证集和批处理函数
        train_set, val_set, collate_fn = get_dataset2_collate_fn(X, y, val_data)
        
        # 调用父类的 train_evaluate 方法进行训练和评估
        return super().train_evaluate(train_set, val_set, collate_fn, epochs, optimizer, scheduler, lr, T_max,
                            batch_size, eval_batch_size, sampler, num_workers, num_eval_workers, pin_memory,
                            pin_memory_device, persistent_workers, early_stopping_rounds, print_per_rounds, 
                            drop_last, checkpoint_per_rounds, checkpoint_name, show_progress, eps, monitor, verbose)

    def mae(
        self,
        X: Union[torch.Tensor, np.ndarray, List[float]],
        y: Union[torch.Tensor, np.ndarray, List[float]],
        batch_size=128
    ) -> float:
        y = _to_numpy(y)
        pred = self.predict(X, batch_size)
        return mean_absolute_error(y.ravel(), pred.ravel())

    def mse(
        self,
        X: Union[torch.Tensor, np.ndarray, List[float]],
        y: Union[torch.Tensor, np.ndarray, List[float]],
        batch_size=128
    ) -> float:
        y = _to_numpy(y)
        pred = self.predict(X, batch_size)
        return mean_squared_error(y.ravel(), pred.ravel())

    def rmse(
        self,
        X: Union[torch.Tensor, np.ndarray, List[float]],
        y: Union[torch.Tensor, np.ndarray, List[float]],
        batch_size=128
    ) -> float:
        return np.sqrt(self.mse(X, y, batch_size))
    
    def mape(
        self,
        X: Union[torch.Tensor, np.ndarray, List[float]],
        y: Union[torch.Tensor, np.ndarray, List[float]],
        batch_size=128
    ) -> float:
        y = _to_numpy(y)
        pred = self.predict(X, batch_size)
        return mean_absolute_percentage_error(y.ravel(), pred.ravel())
    
    def r2_score(
        self,
        X: Union[torch.Tensor, np.ndarray, List, Tuple],
        y: Union[torch.Tensor, np.ndarray, List],
        batch_size=128,
    ) -> float:
        """Return R2 score"""
        y = _to_numpy(y)
        pred = self.predict(X, batch_size)
        return r2_score(y.ravel(), pred.ravel())
    
    def evaluate(
        self,
        X: Union[torch.Tensor, np.ndarray, List[float]],
        y: Union[torch.Tensor, np.ndarray, List[float]],
        batch_size: int = 128,
        verbose: bool = True,
    ) -> dict:
        y = _to_numpy(y)
        pred = self.predict(X, batch_size).ravel()
        mse = mean_squared_error(y, pred)
        metrics = {
            "MAE": mean_absolute_error(y, pred),
            "MSE": mse,
            "RMSE": np.sqrt(mse),
            "MAPE": mean_absolute_percentage_error(y, pred),
            "R2": r2_score(y, pred),
        }

        if verbose:
            self._print_metrics(metrics)
        return metrics


class SplitRegressModelWrapper(FastRegressModelWrapper):
    """
    Examples
    --------
    >>> model_wrapper = SplitRegressModelWrapper(model)
    >>> model_wrapper.train(X, y, collate_fn)
    >>> model_wrapper.predict(X_test)
    >>> model_wrapper.evaluate(X_test, y_test)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(model_or_path, device)

    def train(
        self,
        X: Union[torch.Tensor, np.ndarray, List, Tuple],
        y: Union[torch.Tensor, np.ndarray, List],
        val_size=0.2,
        random_state=None,
        collate_fn: Callable = None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        sampler: Sampler = None,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
        monitor="r2_score"
    ) -> dict:
        if 0.0 < val_size < 1.0:
            X_train, X_test, y_train, y_test = split_fn(X, y, test_size=val_size, random_state=random_state)
            val_data = (X_test, y_test)
        else:
            val_data = None
            X_train, y_train = X, y

        return super().train(
            X_train,
            y_train,
            val_data,
            collate_fn,
            epochs,
            optimizer,
            scheduler,
            lr,
            T_max,
            batch_size,
            eval_batch_size,
            sampler,
            num_workers,
            num_eval_workers,
            pin_memory,
            pin_memory_device,
            persistent_workers,
            early_stopping_rounds,
            print_per_rounds,
            drop_last,
            checkpoint_per_rounds,
            checkpoint_name,
            show_progress,
            eps,
            monitor
        )
        
    def train_evaluate(
        self,
        X: Union[torch.Tensor, np.ndarray, List, Tuple],
        y: Union[torch.Tensor, np.ndarray, List],
        val_size=0.2,
        random_state=None,
        collate_fn: Callable = None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        sampler: Sampler = None,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
        monitor="r2_score",
        verbose=True
    ) -> Tuple[dict, dict]:
        """
        训练并评估模型。

        参数:
        - X: 输入数据，可以是torch.Tensor、np.ndarray、List或Tuple类型。
        - y: 目标数据，可以是torch.Tensor、np.ndarray或List类型。
        - val_size: 验证集的比例，默认为0.2。
        - random_state: 随机种子，用于数据分割的随机性控制。
        - collate_fn: 数据加载时的批处理函数，默认为None。
        - epochs: 训练的轮数，默认为100。
        - optimizer: 优化器类型或实例，默认为None。
        - scheduler: 学习率调度器，默认为None。
        - lr: 学习率，默认为0.001。
        - T_max: 学习率调度器的最大周期数，默认为0。
        - batch_size: 训练时的批大小，默认为64。
        - eval_batch_size: 评估时的批大小，默认为128。
        - num_workers: 训练时数据加载的线程数，默认为0。
        - num_eval_workers: 评估时数据加载的线程数，默认为0。
        - pin_memory: 是否将数据加载到固定内存中，默认为False。
        - pin_memory_device: 固定内存的设备名称，默认为空字符串。
        - persistent_workers: 是否保持数据加载器的持久性，默认为False。
        - early_stopping_rounds: 早停的轮数，默认为None。
        - print_per_rounds: 每多少轮打印一次训练信息，默认为1。
        - drop_last: 是否丢弃最后一个不完整的批次，默认为False。
        - checkpoint_per_rounds: 每多少轮保存一次模型检查点，默认为0。
        - checkpoint_name: 模型检查点的文件名，默认为"model.pt"。
        - show_progress: 是否显示训练进度条，默认为True。
        - eps: 数值稳定性的小常数，默认为1e-5。
        - monitor: 监控的指标，默认为"r2_score"。
        - verbose: 是否打印详细信息，默认为True。

        返回:
        - histories: 训练历史记录。
        - metrics: 验证集上的性能指标。
        """
        # 确保验证集比例在合理范围内
        assert 0.0 < val_size < 1.0

        # 将数据集分割为训练集和验证集
        X_train, X_test, y_train, y_test = split_fn(X, y, test_size=val_size, random_state=random_state)

        # 调用父类的train_evaluate方法进行训练和评估
        return super().train_evaluate(
            X_train,
            y_train,
            (X_test, y_test),
            collate_fn,
            epochs,
            optimizer,
            scheduler,
            lr,
            T_max,
            batch_size,
            eval_batch_size,
            sampler,
            num_workers,
            num_eval_workers,
            pin_memory,
            pin_memory_device,
            persistent_workers,
            early_stopping_rounds,
            print_per_rounds,
            drop_last,
            checkpoint_per_rounds,
            checkpoint_name,
            show_progress,
            eps,
            monitor,
            verbose
        )


def split_fn(
    X: Union[torch.Tensor, np.ndarray, List, Tuple],
    y: Union[torch.Tensor, np.ndarray, List],
    test_size: float,
    random_state: int,
) -> Tuple[Union[torch.Tensor, np.ndarray, List, Tuple], Union[torch.LongTensor, np.ndarray, List]]:
    # 多个 X 值，用tuple、set或list封装, 如果是list, 其元素是torch.Tensor或numpy.ndarray
    if is_multi_value(X):
        X = tuple((x if torch.is_tensor(x) else convert_to_tensor(x)) for x in X)
        split_data = train_test_split(*X, y, test_size=test_size, random_state=random_state)
        
        X = split_data[:-2]
        X_train, X_test = X[::2], X[1::2]

        y_train, y_test = split_data[-2:]
        return tuple(X_train), tuple(X_test), y_train, y_test
    else:
        return train_test_split(X, y, test_size=test_size, random_state=random_state)
    
def is_multi_value(X: Union[torch.Tensor, np.ndarray, List, Tuple]):
    # 用tuple、或list封装, 其元素是torch.Tensor或numpy.ndarray 或者 长度小于8的tuple、list
    return isinstance(X, (Tuple, List)) \
        and (isinstance(X[0], (torch.Tensor, np.ndarray)) or (len(X) < 8 and isinstance(X[0], (Tuple, List))))


def get_dataset_collate_fn(
    X: Union[torch.Tensor, np.ndarray, List, Tuple],
    y: Union[torch.Tensor, np.ndarray, List],
    collate_fn: Callable = None,
) -> Tuple[Dataset, Callable]:
    if isinstance(X, Tuple):
        if all([torch.is_tensor(x) for x in X]):
            if isinstance(y, (List, np.ndarray)):
                y = convert_to_tensor(y)
            return TensorDataset(*X, y), collate_fn
        else:
            return ListDataset(*X, y), collate_fn if collate_fn else ListTensorCollator()

    else:
        X, y = convert_data(X, y)
        return TensorDataset(X, y), collate_fn
    

def get_acc_dataset_collate_fn(
    X: Union[torch.Tensor, np.ndarray, List, Tuple],
    y: Union[torch.Tensor, np.ndarray, List],
    collate_fn: Callable = None,
) -> Tuple[Dataset, Callable]:
    if isinstance(X, Tuple):
        if all([torch.is_tensor(x) for x in X]):
            if isinstance(y, (List, np.ndarray)):
                y = convert_to_long_tensor(y)
            return TensorDataset(*X, y), collate_fn
        else:
            return ListDataset(*X, y), collate_fn if collate_fn else ListTensorCollator()

    else:
        X = convert_to_tensor(X, 2)
        y = convert_to_long_tensor(y)
        return TensorDataset(X, y), collate_fn
    

def get_dataset2_collate_fn(
    X: Union[torch.Tensor, np.ndarray, List, Tuple],
    y: Union[torch.Tensor, np.ndarray, List],
    val_data: Tuple,
    collate_fn: Callable = None,
) -> Tuple[Dataset, Dataset, Callable]:
    if isinstance(X, Tuple):
        if all([torch.is_tensor(x) for x in X]):
            y_val = val_data[1]
            if isinstance(y, (List, np.ndarray)):
                y = convert_to_tensor(y)
                y_val = convert_to_tensor(y_val)
            return TensorDataset(*X, y), TensorDataset(*val_data[0], y_val), collate_fn
        else:
            return ListDataset(*X, y), ListDataset(*val_data[0], val_data[1]), collate_fn if collate_fn else ListTensorCollator()
    else:
        X, y = convert_data(X, y)
        X_val, y_val = convert_data(val_data[0], val_data[1])
        return TensorDataset(X, y), TensorDataset(X_val, y_val), collate_fn
    

def get_acc_dataset2_collate_fn(
    X: Union[torch.Tensor, np.ndarray, List, Tuple],
    y: Union[torch.Tensor, np.ndarray, List],
    val_data: Tuple,
    collate_fn: Callable = None,
) -> Tuple[Dataset, Dataset, Callable]:
    if isinstance(X, Tuple):
        if all([torch.is_tensor(x) for x in X]):
            y = convert_to_long_tensor(y)
            y_val = convert_to_long_tensor(val_data[1])
            return TensorDataset(*X, y), TensorDataset(*val_data[0], y_val), collate_fn
        else:
            return ListDataset(*X, y), ListDataset(*val_data[0], val_data[1]), collate_fn if collate_fn else ListTensorCollator()
    else:
        if isinstance(X, (List, np.ndarray)):
            X = convert_to_tensor(X, 2)

        X_val = val_data[0]
        if isinstance(X_val, (List, np.ndarray)):
            X_val = convert_to_tensor(X_val, 2)
            
        y = convert_to_long_tensor(y)
        y_val = convert_to_long_tensor(val_data[1])
        return TensorDataset(X, y), TensorDataset(X_val, y_val), collate_fn 
    

def _to_numpy(X):
    if torch.is_tensor(X):
        X = X.numpy()
    elif isinstance(X, list):
        X = np.array(X)
    return X