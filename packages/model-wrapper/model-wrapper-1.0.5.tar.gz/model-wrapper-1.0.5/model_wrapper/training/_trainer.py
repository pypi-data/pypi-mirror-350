from copy import deepcopy
from typing import List, Tuple, Union, Callable
import torch
from torch import nn
from torch import optim
from torch.utils.data import DataLoader, Dataset
from torch.utils.data.sampler import Sampler
from torch.optim.lr_scheduler import LRScheduler, CosineAnnealingLR

from model_wrapper import log_utils
from model_wrapper.utils import (
    get_device,
    is_improve,
    is_improve_loss,
    is_early_stopping,
    is_gpu,
    get_workers,
    get_early_stopping_rounds,
)
from ._support import (
    evaluate_epoch,
    acc_evaluate_epoch,
    r2_evaluate_epoch,
    train_epoch,
    train_epoch_acc,
    train_epoch_r2,
)

TRAIN_LOSS = 'train_loss'
VAL_LOSS = 'val_loss'
TRAIN_ACC = 'train_acc'
VAL_ACC = 'val_acc'
TRAIN_R2 = 'train_r2'
VAL_R2 = 'val_r2'


class Trainer:
    
    def __init__(
        self,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size=32,
        num_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,  # 早停，等10轮决策，评价指标不在变化，停止
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        device: Union[str, int, torch.device] = "auto",
    ):
        self.epochs = epochs
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.lr = lr
        self.T_max = T_max
        self.batch_size = batch_size
        self.device = get_device(device)
        self.num_workers = num_workers
        self.pin_memory = pin_memory
        self.pin_memory_device = pin_memory_device
        self.persistent_workers = persistent_workers
        self.early_stopping_rounds = early_stopping_rounds or get_early_stopping_rounds(
            epochs
        )
        self.print_per_rounds = print_per_rounds
        self.drop_last = drop_last
        self.checkpoint_per_rounds = checkpoint_per_rounds
        self.checkpoint_name = checkpoint_name

    def _begin_train(self, model):
        total_parameters, train_parameters = 0, 0
        for param in model.parameters():
            total_parameters += param.numel()
            if param.requires_grad:
                train_parameters += param.numel()
        log_utils.info(f'Model parameters(trainable / total): {train_parameters} / {total_parameters}. Use {self.device.type.upper()} training......\n')

        is_parallel = isinstance(model, nn.DataParallel)
        if is_parallel and hasattr(model.module, "fit"):
            model = model.module

        model = self._check_device(model)
        return model, is_parallel

    def _get_workers(
        self, num_workers: int, dataset: Dataset, batch_size: int, train: bool = True
    ) -> int:
        if is_gpu(self.device):
            return (
                num_workers
                if num_workers > 0
                else get_workers(len(dataset), batch_size, train)
            )
        else:
            return (
                num_workers
                if num_workers >= 0
                else get_workers(len(dataset), batch_size, train)
            )

    def _get_pin_persistent(self, num_workers: int) -> Tuple[bool, bool]:
        pin_memory = self.pin_memory or (num_workers > 0 and is_gpu(self.device))
        persistent_workers = self.persistent_workers or (
            num_workers > 0 and is_gpu(self.device)
        )
        return pin_memory, persistent_workers

    def _build_train_loader(self, train_set: Dataset, collate_fn: Callable, sampler: Sampler = None) -> DataLoader:
        num_workers = self._get_workers(self.num_workers, train_set, self.batch_size)
        pin_memory, persistent_workers = self._get_pin_persistent(num_workers)
   
        return DataLoader(
            dataset=train_set,
            batch_size=self.batch_size,
            shuffle=True if sampler is None else False,
            sampler=sampler,
            pin_memory=pin_memory,
            pin_memory_device=self.pin_memory_device,
            persistent_workers=persistent_workers,
            num_workers=num_workers,
            collate_fn=collate_fn,
            drop_last=self.drop_last
        )

    def _build_val_loader(
        self,
        val_set: Dataset,
        eval_batch_size: int,
        num_eval_workers: int,
        collate_fn: Callable = None,
    ):
        num_eval_workers = self._get_workers(
            num_eval_workers, val_set, eval_batch_size, False
        )
        return DataLoader(
            dataset=val_set,
            batch_size=eval_batch_size,
            num_workers=num_eval_workers,
            collate_fn=collate_fn,
        )
    
    def _check_device(self, model):
        if next(model.parameters()).device != self.device:
            model = model.to(self.device)
        return model

    def train(
        self, model, train_set: Dataset, collate_fn: Callable = None, sampler: Sampler = None, show_progress=False, eps=1e-5
    ) -> Tuple[nn.Module, dict]:
        cnt = 0
        min_loss = float("inf")
        best_model = None
        train_losses = []
        model, is_parallel = self._begin_train(model)
        train_loader = self._build_train_loader(train_set, collate_fn, sampler)
        optimizer, scheduler = self.get_optimizer_scheduler(model)
        is_tuple_params = isinstance(next(iter(train_loader)), (tuple, list))

        model.train()
        for epoch in range(1, self.epochs + 1):
            avg_loss = train_epoch(
                model,
                train_loader,
                optimizer,
                self.device,
                scheduler,
                epoch,
                self.epochs,
                show_progress,
                is_tuple_params,
                is_parallel
            )
            train_losses.append(avg_loss)
            self.try_print(
                self.print,
                show_progress,
                epoch,
                optimizer.param_groups[0]["lr"],
                avg_loss,
            )
            self.try_checkpoint(model, epoch)

            if min_loss - avg_loss > eps:
                cnt = 0
                best_model = deepcopy(model)
                min_loss = avg_loss
                continue

            cnt += 1
            if is_early_stopping(epoch, cnt, self.early_stopping_rounds):
                log_utils.info(f"Early stopping at Epoch-{epoch}")
                break

        log_utils.info(f"Min Loss: {min_loss:.4f}\n")
        return best_model, {TRAIN_LOSS: train_losses}

    def get_optimizer_scheduler(self, model):
        scheduler = None
        if self.scheduler is not None:
            scheduler = self.scheduler
            optimizer = scheduler.optimizer
        elif self.optimizer is None:
            optimizer = optim.AdamW(filter(lambda p: p.requires_grad, model.parameters()), lr=self.lr)
        elif isinstance(self.optimizer, type):
            optimizer = self.optimizer(filter(lambda p: p.requires_grad, model.parameters()), lr=self.lr)
        else:
            optimizer = self.optimizer

        if scheduler is None and self.T_max and self.T_max > 0:
            scheduler = CosineAnnealingLR(optimizer, T_max=self.T_max)

        return optimizer, scheduler

    def try_checkpoint(self, model, epoch):
        if self.checkpoint_per_rounds <= 0:
            return

        if self.checkpoint_per_rounds == 1 or epoch % self.checkpoint_per_rounds == 0:
            torch.save(model, self.checkpoint_name)

    def try_print(self, do_print, show_progress, epoch, lr, loss, **kwargs):
        if self.print_per_rounds == 1 or epoch % self.print_per_rounds == 0:
            do_print(show_progress, epoch, lr, loss, **kwargs)

    def print(self, show_progress, epoch, lr, loss):
        if not show_progress:
            log_utils.info(
                f"Epoch-{epoch}/{self.epochs}  lr: {lr:.6f}, train_loss: {loss:.4f}"
            )


class EvalTrainer(Trainer):

    def __init__(
        self,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size=32,
        eval_batch_size: int = 64,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,  # 早停，等10轮决策，评价指标不在变化，停止
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(
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
            early_stopping_rounds,
            print_per_rounds,
            drop_last,
            checkpoint_per_rounds,
            checkpoint_name,
            device,
        )
        self.eval_batch_size = eval_batch_size
        self.num_eval_workers = num_eval_workers

    def train(
        self,
        model,
        train_set: Dataset,
        val_set: Dataset,
        collate_fn: Callable = None,
        sampler: Sampler = None,
        show_progress=False,
        eps=1e-5,
    ) -> Tuple[nn.Module, dict]:
        cnt = 0
        best_model = None
        min_loss = float("inf")
        train_losses, val_losses = [], []
        model, is_parallel = self._begin_train(model)
        train_loader = self._build_train_loader(train_set, collate_fn, sampler)
        val_loader = self._build_val_loader(
            val_set, self.eval_batch_size, self.num_eval_workers, collate_fn
        )
        optimizer, scheduler = self.get_optimizer_scheduler(model)
        is_tuple_params = isinstance(next(iter(train_loader)), (tuple, list))

        for epoch in range(1, self.epochs + 1):
            model.train()
            avg_loss = train_epoch(
                model,
                train_loader,
                optimizer,
                self.device,
                scheduler,
                epoch,
                self.epochs,
                show_progress,
                is_tuple_params,
                is_parallel,
            )
            val_loss = evaluate_epoch(
                model,
                val_loader,
                self.device,
                epoch,
                self.epochs,
                show_progress,
                is_tuple_params,
                is_parallel,
            )
            train_losses.append(avg_loss)
            val_losses.append(val_loss)
            self.try_print(
                self.print,
                show_progress,
                epoch,
                optimizer.param_groups[0]["lr"],
                avg_loss,
                val_loss=val_loss,
            )
            self.try_checkpoint(model, epoch)

            if min_loss - val_loss > eps:
                cnt = 0
                best_model = deepcopy(model)
                min_loss = val_loss
                continue

            cnt += 1
            # x次epoch的val_acc不提升或x次epoch的val_acc不变化
            if is_early_stopping(epoch, cnt, self.early_stopping_rounds):
                log_utils.info(f"Early stopping at Epoch-{epoch}")
                break


        log_utils.info(f"Min Loss: {min_loss:.4f}\n")
        return best_model, {TRAIN_LOSS: train_losses, VAL_LOSS: val_losses}

    def print(self, show_progress, epoch, lr, loss, val_loss):
        if not show_progress:
            log_utils.info(
                f"Epoch-{epoch}/{self.epochs}  lr: {lr:.6f}, train_loss: {loss:.4f}, val_loss: {val_loss:.4f}"
            )


class ClassTrainer(Trainer):

    def __init__(
        self,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size=32,
        num_workers=1,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,  # 早停，等10轮决策，评价指标不在变化，停止
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(
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
            early_stopping_rounds,
            print_per_rounds,
            drop_last,
            checkpoint_per_rounds,
            checkpoint_name,
            device,
        )

    def train(
        self,
        model,
        train_set: Dataset,
        collate_fn: Callable = None,
        show_progress=False,
        sampler: Sampler = None,
        weight: torch.Tensor = None,
        eps=1e-5,
        monitor="accuracy",
    ):
        best_model = None
        min_loss = float("inf")
        cnt, cnt2, best_acc, last_acc = 0, 0, 0.0, 0.0
        train_losses, train_accs = [], []
        model, is_parallel = self._begin_train(model)
        train_loader = self._build_train_loader(train_set, collate_fn, sampler)
        optimizer, scheduler = self.get_optimizer_scheduler(model)
        is_tuple_params = isinstance(next(iter(train_loader)), (tuple, list))
        monitor = monitor.lower() in {"accuracy", "acc"}
        model.train()
        for epoch in range(1, self.epochs + 1):
            acc, avg_loss = train_epoch_acc(
                model,
                train_loader,
                optimizer,
                self.device,
                scheduler,
                epoch,
                weight,
                self.epochs,
                show_progress,
                is_tuple_params,
                is_parallel,
            )
            train_accs.append(acc)
            train_losses.append(avg_loss)
            self.try_print(
                self.print,
                show_progress,
                epoch,
                optimizer.param_groups[0]["lr"],
                avg_loss,
                acc=acc,
            )
            self.try_checkpoint(model, epoch)

            if monitor:
                if is_improve(best_acc, acc, min_loss, avg_loss, eps):
                    cnt, cnt2 = 0, 0
                    best_acc, best_model = acc, deepcopy(model)
                    last_acc, min_loss = acc, min(min_loss, avg_loss)
                    continue
            elif is_improve_loss(best_acc, acc, min_loss, avg_loss, eps):
                cnt, cnt2 = 0, 0
                min_loss, best_model = avg_loss, deepcopy(model)
                last_acc, best_acc = acc, max(best_acc, acc)
                continue

            cnt += 1
            if abs(last_acc - acc) < eps:  # val_acc不在变化
                cnt2 += 1
            else:
                cnt2 = 0
                
            # x次epoch的val_acc不提升或x次epoch的val_acc不变化
            if is_early_stopping(epoch, max(cnt, cnt2), self.early_stopping_rounds):
                log_utils.info(f"Early stopping at Epoch-{epoch}")
                break

            last_acc = acc
            best_acc = max(best_acc, acc)
            min_loss = min(min_loss, avg_loss)

        log_utils.info(f"Best Accuracy: {best_acc:.2%}, Min Loss: {min_loss:.4f}\n")
        return best_model, {TRAIN_LOSS: train_losses, TRAIN_ACC: train_accs}

    def print(self, show_progress, epoch, lr, loss, acc):
        if not show_progress:
            log_utils.info(
                f"Epoch-{epoch}/{self.epochs}  lr: {lr:.6f}, train_acc: {acc:.4f}, train_loss: {loss:.4f}"
            )


class EvalClassTrainer(EvalTrainer):

    def __init__(
        self,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size=32,
        eval_batch_size: int = 64,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,  # 早停，等10轮决策，评价指标不在变化，停止
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(
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
            early_stopping_rounds,
            print_per_rounds,
            drop_last,
            checkpoint_per_rounds,
            checkpoint_name,
            device,
        )

    def train(
        self,
        model,
        train_set: Dataset,
        val_set: Dataset,
        collate_fn: Callable = None,
        show_progress=False,
        sampler: Sampler = None,
        weight: torch.Tensor = None,
        eps=1e-5,
        monitor="accuracy",
    ) -> Tuple[nn.Module, dict]:
        best_model = None
        min_loss = float("inf")
        cnt, cnt2, best_acc, last_acc = 0, 0, 0.0, 0.0
        train_losses, train_accs, val_losses, val_accs = [], [], [], []
        model, is_parallel = self._begin_train(model)
        train_loader = self._build_train_loader(train_set, collate_fn, sampler)
        val_loader = self._build_val_loader(
            val_set, self.eval_batch_size, self.num_eval_workers, collate_fn
        )
        optimizer, scheduler = self.get_optimizer_scheduler(model)
        is_tuple_params = isinstance(next(iter(val_loader)), (tuple, list))
        monitor = monitor.lower() in {"accuracy", "acc"}
        for epoch in range(1, self.epochs + 1):
            model.train()
            acc, avg_loss = train_epoch_acc(
                model,
                train_loader,
                optimizer,
                self.device,
                scheduler,
                epoch,
                self.epochs,
                weight,
                show_progress,
                is_tuple_params,
                is_parallel,
            )
            val_loss, val_acc = acc_evaluate_epoch(
                model,
                val_loader,
                self.device,
                epoch,
                self.epochs,
                weight,
                show_progress,
                is_tuple_params,
                is_parallel,
            )
            train_accs.append(acc)
            train_losses.append(avg_loss)
            val_accs.append(val_acc)
            val_losses.append(val_loss)
            self.try_print(
                self.print,
                show_progress,
                epoch,
                optimizer.param_groups[0]["lr"],
                avg_loss,
                acc=acc,
                val_loss=val_loss,
                val_acc=val_acc,
            )
            self.try_checkpoint(model, epoch)

            if monitor:
                if is_improve(best_acc, val_acc, min_loss, val_loss, eps):
                    cnt, cnt2 = 0, 0
                    best_acc, best_model = val_acc, deepcopy(model)
                    last_acc, min_loss = val_acc, min(min_loss, val_loss)
                    continue
            elif is_improve_loss(best_acc, val_acc, min_loss, val_loss, eps):
                cnt, cnt2 = 0, 0
                min_loss, best_model = val_loss, deepcopy(model)
                last_acc, best_acc = val_acc, max(best_acc, val_acc)
                continue

            cnt += 1
            if abs(last_acc - val_acc) < eps:  # val_acc不在变化
                cnt2 += 1
            else:
                cnt2 = 0

            # x次epoch的val_acc不提升或x次epoch的val_acc不变化
            if is_early_stopping(epoch, max(cnt, cnt2), self.early_stopping_rounds):
                log_utils.info(f"Early stopping at Epoch-{epoch}")
                break

            last_acc = val_acc
            best_acc = max(best_acc, val_acc)
            min_loss = min(min_loss, val_loss)

        log_utils.info(f"Best Accuracy: {best_acc:.2%}, Min Loss: {min_loss:.4f}\n")
        return best_model, {
            TRAIN_LOSS: train_losses,
            TRAIN_ACC: train_accs,
            VAL_LOSS: val_losses,
            VAL_ACC: val_accs,
        }

    def print(self, show_progress, epoch, lr, loss, acc, val_loss, val_acc):
        if not show_progress:
            log_utils.info(
                f"Epoch-{epoch}/{self.epochs}  lr: {lr:.6f}, train_acc: {acc:.4f}, train_loss: {loss:.4f}, "
                f"val_acc: {val_acc:.4f}, val_loss: {val_loss:.4f}"
            )


class RegressTrainer(Trainer):

    def __init__(
        self,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size=32,
        num_workers=1,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,  # 早停，等10轮决策，评价指标不在变化，停止
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(
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
            early_stopping_rounds,
            print_per_rounds,
            drop_last,
            checkpoint_per_rounds,
            checkpoint_name,
            device,
        )   

    def train(
        self, model, train_set: Dataset, collate_fn: Callable = None, sampler: Sampler = None, show_progress=False, eps=1e-5, monitor="r2_score"
    ):
        best_model = model
        min_loss = float("inf")
        cnt, cnt2, best_r2, last_r2 = 0, 0, -1.0, -1.0
        train_losses, train_r2s = [], []
        model, is_parallel = self._begin_train(model)
        train_loader = self._build_train_loader(train_set, collate_fn, sampler)
        optimizer, scheduler = self.get_optimizer_scheduler(model)
        is_tuple_params = isinstance(next(iter(train_loader)), (tuple, list))
        monitor = monitor.lower() in {"r2_score", "r2"}

        model.train()
        for epoch in range(1, self.epochs + 1):
            r2, avg_loss = train_epoch_r2(
                model,
                train_loader,
                optimizer,
                self.device,
                scheduler,
                epoch,
                self.epochs,
                show_progress,
                is_tuple_params,
                is_parallel
            )
            train_r2s.append(r2)
            train_losses.append(avg_loss)
            self.try_print(
                self.print,
                show_progress,
                epoch,
                optimizer.param_groups[0]["lr"],
                avg_loss,
                r2=r2,
            )
            self.try_checkpoint(model, epoch)

            if monitor: 
                if is_improve(best_r2, r2, min_loss, avg_loss, eps):
                    cnt, cnt2 = 0, 0
                    best_r2, best_model = r2, deepcopy(model)
                    last_r2, min_loss = r2, min(min_loss, avg_loss)
                    continue
            elif is_improve_loss(best_r2, r2, min_loss, avg_loss, eps):
                cnt, cnt2 = 0, 0
                min_loss, best_model = avg_loss, deepcopy(model)
                last_r2, best_r2 = r2, max(best_r2, r2)
                continue

            cnt += 1
            if abs(last_r2 - r2) < eps:  # val_r2不在变化
                cnt2 += 1
            else:
                cnt2 = 0

            # x次epoch的val_acc不提升或x次epoch的val_acc不变化
            if is_early_stopping(epoch, max(cnt, cnt2), self.early_stopping_rounds):
                log_utils.info(f"Early stopping at Epoch-{epoch}")
                break

            last_r2 = r2
            best_r2 = max(best_r2, r2)
            min_loss = min(min_loss, avg_loss)

        log_utils.info(f"Best R2 Score: {best_r2:.4f}, Min Loss: {min_loss:.4f}\n")
        return best_model, {TRAIN_LOSS: train_losses, TRAIN_R2: train_r2s}

    def print(self, show_progress, epoch, lr, loss, r2):
        if not show_progress:
            log_utils.info(
                f"Epoch-{epoch}/{self.epochs}  lr: {lr:.6f}, train_loss: {loss:.4f}, train_r2: {r2:.4f}"
            )


class EvalRegressTrainer(Trainer):

    def __init__(
        self,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size=32,
        eval_batch_size: int = 64,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,  # 早停，等10轮决策，评价指标不在变化，停止
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(
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
            early_stopping_rounds,
            print_per_rounds,
            drop_last,
            checkpoint_per_rounds,
            checkpoint_name,
            device,
        )
        self.eval_batch_size = eval_batch_size
        self.num_eval_workers = num_eval_workers

    def train(
        self,
        model,
        train_set: Dataset,
        val_set: Dataset,
        collate_fn: Callable = None,
        sampler: Sampler = None,
        show_progress=False,
        eps=1e-5,
        monitor="r2_score",
    ) -> Tuple[nn.Module, dict]:
        best_model = model
        min_loss = float("inf")
        cnt, cnt2, best_r2, last_r2 = 0, 0, -1.0, -1.0
        train_losses, train_r2s, val_losses, val_r2s = [], [], [], []
        model, is_parallel = self._begin_train(model)
        train_loader = self._build_train_loader(train_set, collate_fn, sampler)
        val_loader = self._build_val_loader(
            val_set, self.eval_batch_size, self.num_eval_workers, collate_fn
        )
        optimizer, scheduler = self.get_optimizer_scheduler(model)
        is_tuple_params = isinstance(next(iter(val_loader)), (tuple, list))
        monitor = monitor.lower() in {"r2_score", "r2"}

        for epoch in range(1, self.epochs + 1):
            model.train()
            r2, avg_loss = train_epoch_r2(
                model,
                train_loader,
                optimizer,
                self.device,
                scheduler,
                epoch,
                self.epochs,
                show_progress,
                is_tuple_params,
                is_parallel
            )
            val_loss, val_r2 = r2_evaluate_epoch(
                model,
                val_loader,
                self.device,
                epoch,
                self.epochs,
                show_progress,
                is_tuple_params,
                is_parallel
            )
            train_r2s.append(r2)
            train_losses.append(avg_loss)
            val_r2s.append(val_r2)
            val_losses.append(val_loss)

            self.try_print(
                self.print,
                show_progress,
                epoch,
                optimizer.param_groups[0]["lr"],
                avg_loss,
                r2=r2,
                val_loss=val_loss,
                val_r2=val_r2,
            )
            self.try_checkpoint(model, epoch)

            if monitor:
                if is_improve(best_r2, val_r2, min_loss, val_loss, eps):
                    cnt, cnt2 = 0, 0
                    best_r2, best_model = val_r2, deepcopy(model)
                    last_r2, min_loss = val_r2, min(min_loss, val_loss)
                    continue
            elif is_improve_loss(best_r2, val_r2, min_loss, val_loss, eps):
                cnt, cnt2 = 0, 0
                min_loss, best_model = val_loss, deepcopy(model)
                last_r2, best_r2 = val_r2, max(best_r2, val_r2)
                continue

            cnt += 1
            if abs(last_r2 - val_r2) < eps:  # val_r2不在变化
                cnt2 += 1
            else:
                cnt2 = 0

            # x次epoch的val_acc不提升或x次epoch的val_acc不变化
            if is_early_stopping(epoch, max(cnt, cnt2), self.early_stopping_rounds):
                log_utils.info(f"Early stopping at Epoch-{epoch}")
                break

            last_r2 = val_r2
            best_r2 = max(best_r2, val_r2)
            min_loss = min(min_loss, val_loss)

        log_utils.info(f"Best R2 Score: {best_r2:.4f}, Min Loss: {min_loss:.4f}\n")
        return best_model, {
            TRAIN_LOSS: train_losses,
            TRAIN_R2: train_r2s,
            VAL_LOSS: val_losses,
            VAL_R2: val_r2s,
        }

    def print(self, show_progress, epoch, lr, loss, r2, val_loss, val_r2):
        if not show_progress:
            log_utils.info(
                f"Epoch-{epoch}/{self.epochs}  lr: {lr:.6f}, train_loss: {loss:.4f}, train_r2: {r2:.4f}, "
                f"val_loss: {val_loss:.4f}, val_r2: {val_r2:.4f}"
            )
