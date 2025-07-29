import inspect
from typing import Collection, List, Tuple, Union, Callable
import numpy as np
from tqdm import tqdm
from sklearn.metrics import r2_score
import torch
from torch import nn
from torch.optim.lr_scheduler import LRScheduler
from torch.nn import functional as F
from torch.utils.data import DataLoader, Dataset

from model_wrapper.utils import cal_count, cal_correct, get_workers, get_device, acc_predict


def _forward(model, batch, device):
    batch = [x.to(device) if torch.is_tensor(x) else x for x in batch]
    return model(*batch)


def _forward_dict(model, batch, device):
    batch = {
        key: value.to(device) if torch.is_tensor(value) else value
        for key, value in batch.items()
    }
    return model(**batch)


def _fit(model, batch, device):
    batch = [x.to(device) if torch.is_tensor(x) else x for x in batch]
    return model.fit(*batch)


def _fit_dict(model, batch, device):
    batch = {
        key: value.to(device) if torch.is_tensor(value) else value
        for key, value in batch.items()
    }
    return model.fit(**batch)

def _diff_params(model, batch, is_parallel: bool):
    """
    判断所传参数个数是与方法定义的参数相差多少
    """
    return len(batch) - len(inspect.signature(model.module.forward if is_parallel else model.forward).parameters)

def _is_same_params(model, batch, is_parallel: bool):
    """
    判断所传参数个数是与方法是否一致
    """
    return len(batch) == len(inspect.signature(model.module.forward if is_parallel else model.forward).parameters)  

def _forward_y(model, batch, device, is_parallel: bool):
    # 判断所传参数个数是否与方法一致
    diff = _diff_params(model, batch, is_parallel)
    batch = [x.to(device) if torch.is_tensor(x) else x for x in batch]
    if diff == 0:
        return model(*batch), batch[-1]
    # 参数个数不一致，去掉多余的(正常只有一个）
    return model(*(batch[:-diff])), batch[-1]


def _forward_y_dict(model, batch, device, is_parallel: bool):
    # 判断所传参数个数是否与方法一致
    same_params = _is_same_params(model, batch, is_parallel)
    batch = {
        key: value.to(device) if torch.is_tensor(value) else value
        for key, value in batch.items()
    }

    if same_params:
        y = batch["labels"] if "labels" in batch else batch["targets"]
    else:  # 参数个数不一致，要把 'labels' 或 'targets' 从参数里剔除
        y = batch.pop("labels") if "labels" in batch else batch.pop("targets")
    return model(**batch), y


def _fit_y(model, batch, device):
    batch = [x.to(device) if torch.is_tensor(x) else x for x in batch]
    arg_len = len(batch)
    parma_len = len(inspect.signature(model.fit).parameters)
       
    if arg_len == parma_len:
        return model.fit(*batch), batch[-1]
    
    return model.fit(*batch[:-1], *[None for _ in range(parma_len-arg_len)], batch[-1]), batch[-1]


def _fit_y_dict(model, batch, device):
    batch = {
        key: value.to(device) if torch.is_tensor(value) else value
        for key, value in batch.items()
    }
    return model.fit(**batch), (
        batch["labels"] if "labels" in batch else batch["targets"]
    )

#   ----------------------------------------------------------------

def predict_dataset(
    model: nn.Module,
    dataset: Dataset,
    batch_size: int,
    num_workers: int,
    collate_fn: Callable,
    device: Union[str, int, torch.device],
) -> Tuple[torch.Tensor, torch.Tensor]:
    logits = []
    targets = []
    device = get_device(device)
    model = model.to(device).eval()
    data_loader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers if num_workers is not None else get_workers(len(dataset), batch_size, train=False),
        collate_fn=collate_fn,
    )
    is_tuple_params = _is_tuple_params(None, dataset)
    is_parallel = isinstance(model, nn.DataParallel)
    with torch.no_grad():
        if is_tuple_params:
            for batch in data_loader:
                outputs, y = _forward_y(model, batch, device, is_parallel)
                logits.append(outputs.cpu())
                targets.append(y.cpu())
        else:
            for batch in data_loader:
                outputs, y = _forward_y_dict(model, batch, device, is_parallel)
                logits.append(outputs.cpu())
                targets.append(y.cpu())

    logits = torch.cat(logits, dim=0)
    targets = torch.cat(targets, dim=0)
    return logits, targets


def acc_predict_dataset(
    model: nn.Module,
    dataset: Dataset,
    batch_size: int,
    threshold: float,
    num_workers: int,
    collate_fn: Callable,
    device: Union[str, int, torch.device],
) -> Tuple[np.ndarray, np.ndarray]:
    logits, targets = predict_dataset(
        model, dataset, batch_size, num_workers, collate_fn, device
    )
    preds = acc_predict(logits, threshold)
    return preds, targets.numpy()


def evaluate(model, val_loader, device, is_tuple_params: bool = None, is_parallel=False) -> float:
    total_loss = torch.Tensor([0.0]).to(device)
    is_tuple_params = _is_tuple_params(is_tuple_params, val_loader)
    model.eval()
    with torch.inference_mode():
        if hasattr(model, "fit"):
            if is_tuple_params:
                for batch in val_loader:
                    loss, _ = _fit(model, batch, device)
                    total_loss += loss
            else:
                for batch in val_loader:
                    loss, _ = _fit_dict(model, batch, device)
                    total_loss += loss
        else:
            if is_tuple_params:
                for batch in val_loader:
                    loss, _ = _forward(model, batch, device)
                    total_loss += loss
            else:
                for batch in val_loader:
                    loss, _ = _forward_dict(model, batch, device)
                    total_loss += loss
    return total_loss.item() / len(val_loader)


def evaluate_progress(
    model, val_loader, device, epoch, epochs, is_tuple_params: bool = None, is_parallel=False
) -> float:
    steps = 0
    total_loss = torch.Tensor([0.0]).to(device)
    is_tuple_params = _is_tuple_params(is_tuple_params, val_loader)
    model.eval()
    with torch.inference_mode():
        loop = tqdm(
            val_loader,
            desc=f"[Epoch-{epoch}/{epochs} Valid]",
            total=len(val_loader),
            colour="green",
        )
        if hasattr(model, "fit"):
            if is_tuple_params:
                for batch in loop:
                    loss, _ = _fit(model, batch, device)
                    total_loss += loss
                    steps += 1
                    loop.set_postfix(Loss=f"{total_loss.item() / steps:.4f}")
            else:
                for batch in loop:
                    loss, _ = _fit_dict(model, batch, device)
                    total_loss += loss
                    steps += 1
                    loop.set_postfix(Loss=f"{total_loss.item() / steps:.4f}")
        else:
            if is_tuple_params:
                for batch in loop:
                    loss, _ = _forward(model, batch, device)
                    total_loss += loss
                    steps += 1
                    loop.set_postfix(Loss=f"{total_loss.item() / steps:.4f}")
            else:
                for batch in loop:
                    loss, _ = _forward_dict(model, batch, device)
                    total_loss += loss
                    steps += 1
                    loop.set_postfix(Loss=f"{total_loss.item() / steps:.4f}")
        loop.write('')
        loop.close()

    return total_loss.item() / steps


def evaluate_epoch(
    model, val_loader, device, epoch, epochs, show_progress, is_tuple_params, is_parallel=False
):
    if show_progress:
        return evaluate_progress(
            model, val_loader, device, epoch, epochs, is_tuple_params=is_tuple_params, is_parallel=is_parallel
        )
    else:
        return evaluate(model, val_loader, device, is_tuple_params=is_tuple_params, is_parallel=is_parallel)


def do_train(model, batch, optimizer, device):
    loss, _ = _forward(model, batch, device)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss


def do_train_dict(model, batch, optimizer, device):
    loss, _ = _forward_dict(model, batch, device)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss


def do_fit(model, batch, optimizer, device):
    loss, _ = _fit(model, batch, device)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss


def do_fit_dict(model, batch, optimizer, device):
    loss, _ = _fit_dict(model, batch, device)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss


def do_train_scheduler(model, batch, optimizer, device, scheduler: LRScheduler):
    loss, _ = _forward(model, batch, device)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    scheduler.step()
    return loss


def do_train_scheduler_dict(model, batch, optimizer, device, scheduler: LRScheduler):
    loss, _ = _forward_dict(model, batch, device)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    scheduler.step()
    return loss


def do_fit_scheduler(model, batch, optimizer, device, scheduler: LRScheduler):
    loss, _ = _fit(model, batch, device)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    scheduler.step()
    return loss


def do_fit_scheduler_dict(model, batch, optimizer, device, scheduler: LRScheduler):
    loss, _ = _fit_dict(model, batch, device)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    scheduler.step()
    return loss


def train_epoch_base(model, train_loader, optimizer, device, is_tuple_params, is_parallel: bool):
    steps = 0
    total_loss = torch.Tensor([0.0]).to(device)
    num_iter = len(train_loader)
    reset = get_reset(num_iter)
    if hasattr(model, "fit"):
        if is_tuple_params:
            for batch in train_loader:
                loss = do_fit(model, batch, optimizer, device)
                total_loss += loss
                steps += 1
                if reset == steps:
                    steps = 0
                    total_loss = torch.Tensor([0.0]).to(device)
        else:
            for batch in train_loader:
                loss = do_fit_dict(model, batch, optimizer, device)
                total_loss += loss
                steps += 1
                if reset == steps:
                    steps = 0
                    total_loss = torch.Tensor([0.0]).to(device)
    else:
        if is_tuple_params:
            for batch in train_loader:
                loss = do_train(model, batch, optimizer, device)
                total_loss += loss
                steps += 1
                if reset == steps:
                    steps = 0
                    total_loss = torch.Tensor([0.0]).to(device)
        else:
            for batch in train_loader:
                loss = do_train_dict(model, batch, optimizer, device)
                total_loss += loss
                steps += 1
                if reset == steps:
                    steps = 0
                    total_loss = torch.Tensor([0.0]).to(device)

    return total_loss.item() / steps


def train_epoch_progress(
    model, train_loader, optimizer, device, epoch, epochs, is_tuple_params, is_parallel: bool
):
    steps = 0
    total_loss = torch.Tensor([0.0]).to(device)
    num_iter = len(train_loader)
    reset = get_reset(num_iter)
    loop = tqdm(
        train_loader,
        desc=f"[Epoch-{epoch}/{epochs} Train]",
        total=len(train_loader),
        colour="green",
    )
    if hasattr(model, "fit"):
        if is_tuple_params:
            for batch in loop:
                loss = do_fit(model, batch, optimizer, device)
                total_loss += loss
                steps += 1
                loop.set_postfix(
                    Loss=f"{total_loss.item() / steps:.4f}",
                    LR=f'{optimizer.param_groups[0]["lr"]:.6f}',
                )
                if reset == steps:
                    steps = 0
                    total_loss = torch.Tensor([0.0]).to(device)
        else:
            for batch in loop:
                loss = do_fit_dict(model, batch, optimizer, device)
                total_loss += loss
                steps += 1
                loop.set_postfix(
                    Loss=f"{total_loss.item() / steps:.4f}",
                    LR=f'{optimizer.param_groups[0]["lr"]:.6f}',
                )
                if reset == steps:
                    steps = 0
                    total_loss = torch.Tensor([0.0]).to(device)
    else:
        if is_tuple_params:
            for batch in loop:
                loss = do_train(model, batch, optimizer, device)
                total_loss += loss
                steps += 1
                loop.set_postfix(
                    Loss=f"{total_loss.item() / steps:.4f}",
                    LR=f'{optimizer.param_groups[0]["lr"]:.6f}',
                )
                if reset == steps:
                    steps = 0
                    total_loss = torch.Tensor([0.0]).to(device)
        else:
            for batch in loop:
                loss = do_train_dict(model, batch, optimizer, device)
                total_loss += loss
                steps += 1
                loop.set_postfix(
                    Loss=f"{total_loss.item() / steps:.4f}",
                    LR=f'{optimizer.param_groups[0]["lr"]:.6f}',
                )
                if reset == steps:
                    steps = 0
                    total_loss = torch.Tensor([0.0]).to(device)
    loop.close()
    return total_loss.item() / steps


def train_epoch_scheduler(
    model, train_loader, optimizer, device, scheduler: LRScheduler, is_tuple_params, is_parallel=False
):
    steps = 0
    total_loss = torch.Tensor([0.0]).to(device)
    num_iter = len(train_loader)
    reset = get_reset(num_iter)
    if hasattr(model, "fit"):
        if is_tuple_params:
            for batch in train_loader:
                loss = do_fit_scheduler(model, batch, optimizer, device, scheduler)
                total_loss += loss
                steps += 1
                if reset == steps:
                    steps = 0
                    total_loss = torch.Tensor([0.0]).to(device)
        else:
            for batch in train_loader:
                loss = do_fit_scheduler_dict(model, batch, optimizer, device, scheduler)
                total_loss += loss
                steps += 1
                if reset == steps:
                    steps = 0
                    total_loss = torch.Tensor([0.0]).to(device)
    else:
        if is_tuple_params:
            for batch in train_loader:
                loss = do_train_scheduler(model, batch, optimizer, device, scheduler)
                total_loss += loss
                steps += 1
                if reset == steps:
                    steps = 0
                    total_loss = torch.Tensor([0.0]).to(device)
        else:
            for batch in train_loader:
                loss = do_train_scheduler_dict(
                    model, batch, optimizer, device, scheduler
                )
                total_loss += loss
                steps += 1
                if reset == steps:
                    steps = 0
                    total_loss = torch.Tensor([0.0]).to(device)
    return total_loss.item() / steps


def train_epoch_scheduler_progress(
    model, train_loader, optimizer, device, scheduler, epoch, epochs, is_tuple_params, is_parallel=False
):
    steps = 0
    total_loss = torch.Tensor([0.0]).to(device)
    num_iter = len(train_loader)
    reset = get_reset(num_iter)
    loop = tqdm(
        train_loader,
        desc=f"[Epoch-{epoch}/{epochs} Train]",
        total=len(train_loader),
        colour="green",
    )
    if hasattr(model, "fit"):
        if is_tuple_params:
            for batch in loop:
                loss = do_fit_scheduler(model, batch, optimizer, device, scheduler)
                total_loss += loss
                steps += 1
                loop.set_postfix_str(f"LR={optimizer.param_groups[0]['lr']:.6f}, Loss={total_loss.item() / steps:.4f}")
                if reset == steps:
                    steps = 0
                    total_loss = torch.Tensor([0.0]).to(device)
        else:
            for batch in loop:
                loss = do_fit_scheduler_dict(model, batch, optimizer, device, scheduler)
                total_loss += loss
                steps += 1
                loop.set_postfix_str(f"LR={optimizer.param_groups[0]['lr']:.6f}, Loss={total_loss.item() / steps:.4f}")
                if reset == steps:
                    steps = 0
                    total_loss = torch.Tensor([0.0]).to(device)
    else:
        if is_tuple_params:
            for batch in loop:
                loss = do_train_scheduler(model, batch, optimizer, device, scheduler)
                total_loss += loss
                steps += 1
                loop.set_postfix_str(f"LR={optimizer.param_groups[0]['lr']:.6f}, Loss={total_loss.item() / steps:.4f}")
                if reset == steps:
                    steps = 0
                    total_loss = torch.Tensor([0.0]).to(device)
        else:
            for batch in loop:
                loss = do_train_scheduler_dict(
                    model, batch, optimizer, device, scheduler
                )
                total_loss += loss
                steps += 1
                loop.set_postfix_str(f"LR={optimizer.param_groups[0]['lr']:.6f}, Loss={total_loss.item() / steps:.4f}")
                if reset == steps:
                    steps = 0
                    total_loss = torch.Tensor([0.0]).to(device)
    loop.close()
    return total_loss.item() / steps


def train_epoch(
    model,
    train_loader,
    optimizer,
    device,
    scheduler,
    epoch,
    epochs,
    show_progress,
    is_tuple_params,
    is_parallel,
):
    if show_progress:
        if scheduler is None:
            return train_epoch_progress(
                model, train_loader, optimizer, device, epoch, epochs, is_tuple_params, is_parallel
            )
        return train_epoch_scheduler_progress(
            model,
            train_loader,
            optimizer,
            device,
            scheduler,
            epoch,
            epochs,
            is_tuple_params,
            is_parallel,
        )
    else:
        if scheduler is None:
            return train_epoch_base(
                model, train_loader, optimizer, device, is_tuple_params, is_parallel
            )
        return train_epoch_scheduler(
            model, train_loader, optimizer, device, scheduler, is_tuple_params, is_parallel
        )

#  ----------------------------------------------------------------

def acc_loss_logits(outputs: torch.Tensor, targets: torch.Tensor, weight: torch.Tensor):
    if isinstance(outputs, tuple):
        loss, logits = outputs
    else:
        logits = outputs
        shape = logits.size()
        shape_len = len(shape)
        if shape_len == 2 and shape[1] > 1:
            # 多分类 logits: (N, num_classes), targets: (N,) 一维
            loss = F.cross_entropy(logits, targets, weight)
        elif shape_len > 2:
            # 多分类 logits: (N, K, num_classes), targets: (N, K)
            targets = targets.view(-1)  # (N * K,) 一维
            logits = logits.reshape(targets.size(0), -1)  # (N * K, num_classes)
            loss = F.cross_entropy(logits, targets, weight)
        else:
            # 二分类 targets 是小数
            if shape_len == 2:
                # (N, 1)
                logits = logits.view(-1)  # (N,) 一维
            if len(targets.shape) == 2:
                targets = targets.view(-1)  # (N,) 一维
            loss = F.binary_cross_entropy(logits, targets, weight)

    return loss, logits


def acc_evaluate(
    model, val_loader, device, weight, threshold: float = 0.5, is_tuple_params: bool = None, is_parallel: bool = False
):
    total, correct = 0, 0
    total_loss = torch.Tensor([0.0]).to(device)
    is_tuple_params = _is_tuple_params(is_tuple_params, val_loader)
    model.eval()
    with torch.inference_mode():
        if hasattr(model, "fit"):
            if is_tuple_params:
                for batch in val_loader:
                    outputs, y = _fit_y(model, batch, device)
                    loss, logits = acc_loss_logits(outputs, y, None if weight is None else weight.to(device))
                    total_loss += loss
                    total += cal_count(y)
                    correct += cal_correct(logits, y, threshold)
            else:
                for batch in val_loader:
                    outputs, y = _fit_y_dict(model, batch, device)
                    loss, logits = acc_loss_logits(outputs, y, None if weight is None else weight.to(device))
                    total_loss += loss
                    total += cal_count(y)
                    correct += cal_correct(logits, y, threshold)
        else:
            if is_tuple_params:
                for batch in val_loader:
                    outputs, y = _forward_y(model, batch, device, is_parallel)
                    loss, logits = acc_loss_logits(outputs, y, None if weight is None else weight.to(device))
                    total_loss += loss
                    total += cal_count(y)
                    correct += cal_correct(logits, y, threshold)
            else:
                for batch in val_loader:
                    outputs, y = _forward_y_dict(model, batch, device, is_parallel)
                    loss, logits = acc_loss_logits(outputs, y, None if weight is None else weight.to(device))
                    total_loss += loss
                    total += cal_count(y)
                    correct += cal_correct(logits, y, threshold)

    return (total_loss.item() / len(val_loader)), (correct / total)


def acc_evaluate_progress(
    model,
    val_loader,
    device,
    epoch,
    epochs,
    weight: torch.Tensor,
    threshold: float = 0.5,
    is_tuple_params: bool = None,
    is_parallel: bool = False
):
    total, correct, steps = 0, 0, 0
    total_loss = torch.Tensor([0.0]).to(device)
    is_tuple_params = _is_tuple_params(is_tuple_params, val_loader)
    model.eval()
    with torch.inference_mode():
        loop = tqdm(
            val_loader,
            desc=f"[Epoch-{epoch}/{epochs} Valid]",
            total=len(val_loader),
            colour="green",
        )
        if hasattr(model, "fit"):
            if is_tuple_params:
                for batch in loop:
                    outputs, y = _fit_y(model, batch, device)
                    loss, logits = acc_loss_logits(outputs, y, None if weight is None else weight.to(device))
                    total_loss += loss
                    total += cal_count(y)
                    correct += cal_correct(logits, y, threshold)
                    steps += 1
                    loop.set_postfix(Acc=f"{correct / total:.4f}", Loss=f"{total_loss.item() / steps:.4f}")
            else:
                for batch in loop:
                    outputs, y = _fit_y_dict(model, batch, device)
                    loss, logits = acc_loss_logits(outputs, y, None if weight is None else weight.to(device))
                    total_loss += loss
                    total += cal_count(y)
                    correct += cal_correct(logits, y, threshold)
                    steps += 1
                    loop.set_postfix(Acc=f"{correct / total:.4f}", Loss=f"{total_loss.item() / steps:.4f}")
        else:
            if is_tuple_params:
                for batch in loop:
                    outputs, y = _forward_y(model, batch, device, is_parallel)
                    loss, logits = acc_loss_logits(outputs, y, None if weight is None else weight.to(device))
                    total_loss += loss
                    total += cal_count(y)
                    correct += cal_correct(logits, y, threshold)
                    steps += 1
                    loop.set_postfix(Acc=f"{correct / total:.4f}", Loss=f"{total_loss.item() / steps:.4f}")
            else:
                for batch in loop:
                    outputs, y = _forward_y_dict(model, batch, device, is_parallel)
                    loss, logits = acc_loss_logits(outputs, y, None if weight is None else weight.to(device))
                    total_loss += loss
                    total += cal_count(y)
                    correct += cal_correct(logits, y, threshold)
                    steps += 1
                    loop.set_postfix(Acc=f"{correct / total:.4f}", Loss=f"{total_loss.item() / steps:.4f}")
        loop.write('')
        loop.close()

    return (total_loss.item() / steps), (correct / total)


def acc_evaluate_epoch(
    model, val_loader, device, epoch, epochs, weight, show_progress, is_tuple_params, is_parallel
):
    if show_progress:
        return acc_evaluate_progress(
            model, val_loader, device, epoch, epochs, weight, is_tuple_params=is_tuple_params, is_parallel=is_parallel
        )
    else:
        return acc_evaluate(model, val_loader, device, weight, is_tuple_params=is_tuple_params, is_parallel=is_parallel)


def do_train_acc(model, batch, optimizer, device, weight, is_parallel: bool):
    outputs, y = _forward_y(model, batch, device, is_parallel)
    loss, logits = acc_loss_logits(outputs, y, None if weight is None else weight.to(device))
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss, cal_count(y), cal_correct(logits.detach(), y)


def do_train_acc_dict(model, batch, optimizer, device, weight, is_parallel: bool):
    outputs, y = _forward_y_dict(model, batch, device, is_parallel)
    loss, logits = acc_loss_logits(outputs, y, None if weight is None else weight.to(device))
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss, cal_count(y), cal_correct(logits.detach(), y)


def do_fit_acc(model, batch, optimizer, device, weight):
    outputs, y = _fit_y(model, batch, device)
    loss, logits = acc_loss_logits(outputs, y, None if weight is None else weight.to(device))
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss, cal_count(y), cal_correct(logits.detach(), y)


def do_fit_acc_dict(model, batch, optimizer, device, weight):
    outputs, y = _fit_y_dict(model, batch, device)
    loss, logits = acc_loss_logits(outputs, y, None if weight is None else weight.to(device))
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss, cal_count(y), cal_correct(logits.detach(), y)


def do_train_scheduler_acc(model, batch, optimizer, device, weight, scheduler: LRScheduler, is_parallel: bool):
    outputs, y = _forward_y(model, batch, device, is_parallel)
    loss, logits = acc_loss_logits(outputs, y, None if weight is None else weight.to(device))
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    scheduler.step()
    return loss, cal_count(y), cal_correct(logits.detach(), y)


def do_train_scheduler_acc_dict(
    model, batch, optimizer, device, weight, scheduler: LRScheduler, is_parallel: bool
):
    outputs, y = _forward_y_dict(model, batch, device, is_parallel)
    loss, logits = acc_loss_logits(outputs, y, None if weight is None else weight.to(device))
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    scheduler.step()
    return loss, cal_count(y), cal_correct(logits.detach(), y)


def do_fit_scheduler_acc(model, batch, optimizer, device, weight, scheduler: LRScheduler):
    outputs, y = _fit_y(model, batch, device)
    loss, logits = acc_loss_logits(outputs, y, None if weight is None else weight.to(device))
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    scheduler.step()
    return loss, cal_count(y), cal_correct(logits.detach(), y)


def do_fit_scheduler_acc_dict(model, batch, optimizer, device, weight, scheduler: LRScheduler):
    outputs, y = _fit_y_dict(model, batch, device)
    loss, logits = acc_loss_logits(outputs, y, None if weight is None else weight.to(device))
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    scheduler.step()
    return loss, cal_count(y), cal_correct(logits.detach(), y)


def train_epoch_base_acc(model, train_loader, optimizer, device, weight, is_tuple_params, is_parallel: bool):
    total, steps, total_correct = 0, 0, 0
    total_loss = torch.Tensor([0.0]).to(device)
    num_iter = len(train_loader)
    reset = get_reset(num_iter)
    if hasattr(model, "fit"):
        if is_tuple_params:
            for batch in train_loader:
                loss, count, correct = do_fit_acc(model, batch, optimizer, device, weight)
                total_loss += loss
                total += count
                total_correct += correct
                steps += 1
                if reset == steps:
                    total, steps, total_correct = 0, 0, 0
                    total_loss = torch.Tensor([0.0]).to(device)
        else:
            for batch in train_loader:
                loss, count, correct = do_fit_acc_dict(model, batch, optimizer, device, weight)
                total_loss += loss
                total += count
                total_correct += correct
                steps += 1
                if reset == steps:
                    total, steps, total_correct = 0, 0, 0
                    total_loss = torch.Tensor([0.0]).to(device)
    else:
        if is_tuple_params:
            for batch in train_loader:
                loss, count, correct = do_train_acc(model, batch, optimizer, device, weight, is_parallel)
                total_loss += loss
                total += count
                total_correct += correct
                steps += 1
                if reset == steps:
                    total, steps, total_correct = 0, 0, 0
                    total_loss = torch.Tensor([0.0]).to(device)
        else:
            for batch in train_loader:
                loss, count, correct = do_train_acc_dict(
                    model, batch, optimizer, device, weight, is_parallel
                )
                total_loss += loss
                total += count
                total_correct += correct
                steps += 1
                if reset == steps:
                    total, steps, total_correct = 0, 0, 0
                    total_loss = torch.Tensor([0.0]).to(device)
    return total_correct / total, total_loss.item() / steps


def train_epoch_progress_acc(
    model, train_loader, optimizer, device, epoch, epochs, weight, is_tuple_params, is_parallel: bool
):
    total, steps, total_correct = 0, 0, 0
    total_loss = torch.Tensor([0.0]).to(device)
    num_iter = len(train_loader)
    reset = get_reset(num_iter)
    loop = tqdm(
        train_loader,
        desc=f"[Epoch-{epoch}/{epochs} Train]",
        total=len(train_loader),
        colour="green",
    )
    if hasattr(model, "fit"):
        if is_tuple_params:
            for batch in loop:
                loss, count, correct = do_fit_acc(model, batch, optimizer, device, weight)
                total_loss += loss
                total += count
                total_correct += correct
                steps += 1
                loop.set_postfix_str(f"LR={optimizer.param_groups[0]['lr']:.6f}, Acc={total_correct.item() / total:.4f}, Loss={total_loss.item() / steps:.4f}")
                if reset == steps:
                    total, steps, total_correct = 0, 0, 0
                    total_loss = torch.Tensor([0.0]).to(device)
        else:
            for batch in loop:
                loss, count, correct = do_fit_acc_dict(model, batch, optimizer, device, weight)
                total_loss += loss
                total += count
                total_correct += correct
                steps += 1
                loop.set_postfix_str(f"LR={optimizer.param_groups[0]['lr']:.6f}, Acc={total_correct.item() / total:.4f}, Loss={total_loss.item() / steps:.4f}")
                if reset == steps:
                    total, steps, total_correct = 0, 0, 0
                    total_loss = torch.Tensor([0.0]).to(device)
    else:
        if is_tuple_params:
            for batch in loop:
                loss, count, correct = do_train_acc(model, batch, optimizer, device, weight, is_parallel)
                total_loss += loss
                total += count
                total_correct += correct
                steps += 1
                loop.set_postfix_str(f"LR={optimizer.param_groups[0]['lr']:.6f}, Acc={total_correct.item() / total:.4f}, Loss={total_loss.item() / steps:.4f}")
                if reset == steps:
                    total, steps, total_correct = 0, 0, 0
                    total_loss = torch.Tensor([0.0]).to(device)
        else:
            for batch in loop:
                loss, count, correct = do_train_acc_dict(
                    model, batch, optimizer, device, weight, is_parallel
                )
                total_loss += loss
                total += count
                total_correct += correct
                steps += 1
                loop.set_postfix_str(f"LR={optimizer.param_groups[0]['lr']:.6f}, Acc={total_correct.item() / total:.4f}, Loss={total_loss.item() / steps:.4f}")
                if reset == steps:
                    total, steps, total_correct = 0, 0, 0
                    total_loss = torch.Tensor([0.0]).to(device)
    loop.close()
    return total_correct / total, total_loss.item() / steps


def train_epoch_scheduler_acc(
    model, train_loader, optimizer, device, weight, scheduler: LRScheduler, is_tuple_params, is_parallel: bool
):
    total, steps, total_correct = 0, 0, 0
    total_loss = torch.Tensor([0.0]).to(device)
    num_iter = len(train_loader)
    reset = get_reset(num_iter)
    if hasattr(model, "fit"):
        if is_tuple_params:
            for batch in train_loader:
                loss, count, correct = do_fit_scheduler_acc(
                    model, batch, optimizer, device, weight, scheduler
                )
                total_loss += loss
                total += count
                total_correct += correct
                steps += 1
                if reset == steps:
                    total, steps, total_correct = 0, 0, 0
                    total_loss = torch.Tensor([0.0]).to(device)
        else:
            for batch in train_loader:
                loss, count, correct = do_fit_scheduler_acc_dict(
                    model, batch, optimizer, device, weight, scheduler
                )
                total_loss += loss
                total += count
                total_correct += correct
                steps += 1
                if reset == steps:
                    total, steps, total_correct = 0, 0, 0
                    total_loss = torch.Tensor([0.0]).to(device)
    else:
        if is_tuple_params:
            for batch in train_loader:
                loss, count, correct = do_train_scheduler_acc(
                    model, batch, optimizer, device, weight, scheduler, is_parallel
                )
                total_loss += loss
                total += count
                total_correct += correct
                steps += 1
                if reset == steps:
                    total, steps, total_correct = 0, 0, 0
                    total_loss = torch.Tensor([0.0]).to(device)
        else:
            for batch in train_loader:
                loss, count, correct = do_train_scheduler_acc_dict(
                    model, batch, optimizer, device, weight, scheduler, is_parallel
                )
                total_loss += loss
                total += count
                total_correct += correct
                steps += 1
                if reset == steps:
                    total, steps, total_correct = 0, 0, 0
                    total_loss = torch.Tensor([0.0]).to(device)
    return total_correct / total, total_loss.item() / steps


def train_epoch_scheduler_progress_acc(
    model, train_loader, optimizer, device, weight, scheduler, epoch, epochs, is_tuple_params, is_parallel: bool
):
    total, steps, total_correct = 0, 0, 0
    total_loss = torch.Tensor([0.0]).to(device)
    num_iter = len(train_loader)
    reset = get_reset(num_iter)
    loop = tqdm(
        train_loader,
        desc=f"[Epoch-{epoch}/{epochs} Train]",
        total=len(train_loader),
        colour="green",
    )
    if hasattr(model, "fit"):
        if is_tuple_params:
            for batch in loop:
                loss, count, correct = do_fit_scheduler_acc(
                    model, batch, optimizer, device, weight, scheduler
                )
                total_loss += loss
                total += count
                total_correct += correct
                steps += 1
                loop.set_postfix_str(f"LR={optimizer.param_groups[0]['lr']:.6f}, Acc={total_correct.item() / total:.4f}, Loss={total_loss.item() / steps:.4f}")
                if reset == steps:
                    total, steps, total_correct = 0, 0, 0
                    total_loss = torch.Tensor([0.0]).to(device)
        else:
            for batch in loop:
                loss, count, correct = do_fit_scheduler_acc_dict(
                    model, batch, optimizer, device, weight, scheduler
                )
                total_loss += loss
                total += count
                total_correct += correct
                steps += 1
                loop.set_postfix_str(f"LR={optimizer.param_groups[0]['lr']:.6f}, Acc={total_correct.item() / total:.4f}, Loss={total_loss.item() / steps:.4f}")
                if reset == steps:
                    total, steps, total_correct = 0, 0, 0
                    total_loss = torch.Tensor([0.0]).to(device)
    else:
        if is_tuple_params:
            for batch in loop:
                loss, count, correct = do_train_scheduler_acc(
                    model, batch, optimizer, device, weight, scheduler, is_parallel
                )
                total_loss += loss
                total += count
                total_correct += correct
                steps += 1
                loop.set_postfix_str(f"LR={optimizer.param_groups[0]['lr']:.6f}, Acc={total_correct.item() / total:.4f}, Loss={total_loss.item() / steps:.4f}")
                if reset == steps:
                    total, steps, total_correct = 0, 0, 0
                    total_loss = torch.Tensor([0.0]).to(device)
        else:
            for batch in loop:
                loss, count, correct = do_train_scheduler_acc_dict(
                    model, batch, optimizer, device, weight, scheduler, is_parallel
                )
                total_loss += loss
                total += count
                total_correct += correct
                steps += 1
                loop.set_postfix_str(f"LR={optimizer.param_groups[0]['lr']:.6f}, Acc={total_correct.item() / total:.4f}, Loss={total_loss.item() / steps:.4f}")
                if reset == steps:
                    total, steps, total_correct = 0, 0, 0
                    total_loss = torch.Tensor([0.0]).to(device)
    loop.close()

    return total_correct / total, total_loss.item() / steps


def train_epoch_acc(
    model,
    train_loader,
    optimizer,
    device,
    scheduler,
    epoch,
    epochs,
    weight,
    show_progress,
    is_tuple_params,
    is_parallel: bool,
):
    if show_progress:
        if scheduler is None:
            return train_epoch_progress_acc(
                model, train_loader, optimizer, device, epoch, epochs, weight, is_tuple_params, is_parallel
            )
        return train_epoch_scheduler_progress_acc(
            model,
            train_loader,
            optimizer,
            device,
            scheduler,
            epoch,
            epochs,
            weight,
            is_tuple_params,
            is_parallel,
        )
    else:
        if scheduler is None:
            return train_epoch_base_acc(
                model, train_loader, optimizer, device, weight, is_tuple_params, is_parallel
            )
        return train_epoch_scheduler_acc(
            model, train_loader, optimizer, device, scheduler, weight, is_tuple_params, is_parallel
        )

#   ----------------------------------------------------------------

def r2_loss_logits(logits, targets):
    return logits if isinstance(logits, tuple) else F.mse_loss(logits, targets.view(logits.size())), logits


def cal_r2_score(y_true: list[np.ndarray], y_pred: list[np.ndarray]):
    y_true = np.concatenate(y_true, axis=0).ravel()
    y_pred = np.concatenate(y_pred, axis=0).ravel()
    return r2_score(y_true, y_pred)


def r2_evaluate(model, val_loader, device, is_tuple_params: bool = None, is_parallel=False):
    labels, preds = [], []
    total_loss = torch.Tensor([0.0]).to(device)
    is_tuple_params = (
        is_tuple_params
        if is_tuple_params is not None
        else isinstance(next(iter(val_loader)), (list, tuple))
    )
    model.eval()
    with torch.inference_mode():
        if hasattr(model, "fit"):
            if is_tuple_params:
                for batch in val_loader:
                    outputs, y = _fit_y(model, batch, device)
                    loss, logits = r2_loss_logits(outputs, y)
                    total_loss += loss
                    labels.append(y.cpu().numpy().ravel())
                    preds.append(logits.cpu().numpy().ravel())
            else:
                for batch in val_loader:
                    outputs, y = _fit_y_dict(model, batch, device)
                    loss, logits = r2_loss_logits(outputs, y)
                    total_loss += loss
                    labels.append(y.cpu().numpy().ravel())
                    preds.append(logits.cpu().numpy().ravel())
        else:
            if is_tuple_params:
                for batch in val_loader:
                    outputs, y = _forward_y(model, batch, device, is_parallel)
                    loss, logits = r2_loss_logits(outputs, y)
                    total_loss += loss
                    labels.append(y.cpu().numpy().ravel())
                    preds.append(logits.cpu().numpy().ravel())
            else:
                for batch in val_loader:
                    outputs, y = _forward_y_dict(model, batch, device, is_parallel)
                    loss, logits = r2_loss_logits(outputs, y)
                    total_loss += loss
                    labels.append(y.cpu().numpy().ravel())
                    preds.append(logits.cpu().numpy().ravel())

    return total_loss.item() / len(val_loader), cal_r2_score(labels, preds)


def r2_evaluate_progress(
    model, val_loader, device, epoch, epochs, is_tuple_params: bool = None, is_parallel=False
):
    steps = 0
    labels, preds = [], []
    total_loss = torch.Tensor([0.0]).to(device)
    is_tuple_params = (
        is_tuple_params
        if is_tuple_params is not None
        else isinstance(next(iter(val_loader)), (list, tuple))
    )
    model.eval()
    with torch.inference_mode():
        loop = tqdm(
            val_loader,
            desc=f"[Epoch-{epoch}/{epochs} Valid]",
            total=len(val_loader),
            colour="green",
        )
        if hasattr(model, "fit"):
            if is_tuple_params:
                for batch in loop:
                    outputs, y = _fit_y(model, batch, device)
                    loss, logits = r2_loss_logits(outputs, y)
                    total_loss += loss
                    labels.append(y.cpu().numpy().ravel())
                    preds.append(logits.cpu().numpy().ravel())
                    steps += 1
                    loop.set_postfix_str(f"R2={cal_r2_score(labels, preds):.4f}, Loss={total_loss.item() / steps:.4f}")
            else:
                for batch in loop:
                    outputs, y = _fit_y_dict(model, batch, device)
                    loss, logits = r2_loss_logits(outputs, y)
                    total_loss += loss
                    labels.append(y.cpu().numpy().ravel())
                    preds.append(logits.cpu().numpy().ravel())
                    steps += 1
                    loop.set_postfix_str(f"R2={cal_r2_score(labels, preds):.4f}, Loss={total_loss.item() / steps:.4f}")
        else:
            if is_tuple_params:
                for batch in loop:
                    outputs, y = _forward_y(model, batch, device, is_parallel)
                    loss, logits = r2_loss_logits(outputs, y)
                    total_loss += loss
                    labels.append(y.cpu().numpy().ravel())
                    preds.append(logits.cpu().numpy().ravel())
                    steps += 1
                    loop.set_postfix_str(f"R2={cal_r2_score(labels, preds):.4f}, Loss={total_loss.item() / steps:.4f}")
            else:
                for batch in loop:
                    outputs, y = _forward_y_dict(model, batch, device, is_parallel)
                    loss, logits = r2_loss_logits(outputs, y)
                    total_loss += loss
                    labels.append(y.cpu().numpy().ravel())
                    preds.append(logits.cpu().numpy().ravel())
                    steps += 1
                    loop.set_postfix_str(f"R2={cal_r2_score(labels, preds):.4f}, Loss={total_loss.item() / steps:.4f}")
        loop.write("")
        loop.close()

    return total_loss.item() / steps, cal_r2_score(labels, preds)


def r2_evaluate_epoch(
    model, val_loader, device, epoch, epochs, show_progress, is_tuple_params, is_parallel=False
):
    if show_progress:
        return r2_evaluate_progress(
            model, val_loader, device, epoch, epochs, is_tuple_params=is_tuple_params, is_parallel=is_parallel
        )
    else:
        return r2_evaluate(model, val_loader, device, is_tuple_params=is_tuple_params, is_parallel=is_parallel)


def train_epoch_r2(
    model,
    train_loader,
    optimizer,
    device,
    scheduler,
    epoch,
    epochs,
    show_progress,
    is_tuple_params,
    is_parallel=False
):
    if show_progress:
        if scheduler is None:
            return train_epoch_progress_r2(
                model, train_loader, optimizer, device, epoch, epochs, is_tuple_params, is_parallel
            )
        return train_epoch_scheduler_progress_r2(
            model,
            train_loader,
            optimizer,
            device,
            scheduler,
            epoch,
            epochs,
            is_tuple_params,
            is_parallel
        )
    else:
        if scheduler is None:
            return train_epoch_base_r2(
                model, train_loader, optimizer, device, is_tuple_params, is_parallel
            )
        return train_epoch_scheduler_r2(
            model, train_loader, optimizer, device, scheduler, is_tuple_params, is_parallel
        )


def train_epoch_base_r2(model, train_loader, optimizer, device, is_tuple_params, is_parallel=False):
    steps = 0
    total_loss = torch.Tensor([0.0]).to(device)
    labels, preds = [], []
    num_iter = len(train_loader)
    reset = get_reset(num_iter)
    if hasattr(model, "fit"):
        if is_tuple_params:
            for batch in train_loader:
                loss, label, pred = do_fit_r2(model, batch, optimizer, device)
                total_loss += loss
                steps += 1
                labels.append(label.ravel())
                preds.append(pred.ravel())
                if reset == steps:
                    steps = 0
                    total_loss = torch.Tensor([0.0]).to(device)
                    labels.clear()
                    preds.clear()
        else:
            for batch in train_loader:
                loss, label, pred = do_fit_r2_dict(model, batch, optimizer, device)
                total_loss += loss
                steps += 1
                labels.append(label.ravel())
                preds.append(pred.ravel())
                if reset == steps:
                    steps = 0
                    total_loss = torch.Tensor([0.0]).to(device)
                    labels.clear()
                    preds.clear()
    else:
        if is_tuple_params:
            for batch in train_loader:
                loss, label, pred = do_train_r2(model, batch, optimizer, device, is_parallel)
                total_loss += loss
                steps += 1
                labels.append(label.ravel())
                preds.append(pred.ravel())
                if reset == steps:
                    steps = 0
                    total_loss = torch.Tensor([0.0]).to(device)
                    labels.clear()
                    preds.clear()
        else:
            for batch in train_loader:
                loss, label, pred = do_train_r2_dict(model, batch, optimizer, device, is_parallel)
                total_loss += loss
                steps += 1
                labels.append(label.ravel())
                preds.append(pred.ravel())
                if reset == steps:
                    steps = 0
                    total_loss = torch.Tensor([0.0]).to(device)
                    labels.clear()
                    preds.clear()

    return cal_r2_score(labels, preds), total_loss.item() / steps


def train_epoch_progress_r2(
    model, train_loader, optimizer, device, epoch, epochs, is_tuple_params, is_parallel=False
):
    steps = 0
    total_loss = torch.Tensor([0.0]).to(device)
    labels, preds = [], []
    num_iter = len(train_loader)
    reset = get_reset(num_iter)
    loop = tqdm(
        train_loader,
        desc=f"[Epoch-{epoch}/{epochs} Train]",
        total=len(train_loader),
        colour="green",
    )
    if hasattr(model, "fit"):
        if is_tuple_params:
            for batch in loop:
                loss, label, pred = do_fit_r2(model, batch, optimizer, device)
                total_loss += loss
                steps += 1
                labels.append(label.ravel())
                preds.append(pred.ravel())
                loop.set_postfix_str(f"LR={optimizer.param_groups[0]['lr']:.6f}, R2={cal_r2_score(labels, preds):.4f}, Loss={total_loss.item() / steps:.4f}")
                if reset == steps:
                    steps = 0
                    total_loss = torch.Tensor([0.0]).to(device)
                    labels.clear()
                    preds.clear()

        else:
            for batch in loop:
                loss, label, pred = do_fit_r2_dict(model, batch, optimizer, device)
                total_loss += loss
                steps += 1
                labels.append(label.ravel())
                preds.append(pred.ravel())
                loop.set_postfix_str(f"LR={optimizer.param_groups[0]['lr']:.6f}, R2={cal_r2_score(labels, preds):.4f}, Loss={total_loss.item() / steps:.4f}")
                if reset == steps:
                    steps = 0
                    total_loss = torch.Tensor([0.0]).to(device)
                    labels.clear()
                    preds.clear()
    else:
        if is_tuple_params:
            for batch in loop:
                loss, label, pred = do_train_r2(model, batch, optimizer, device, is_parallel)
                total_loss += loss
                steps += 1
                labels.append(label.ravel())
                preds.append(pred.ravel())
                loop.set_postfix_str(f"LR={optimizer.param_groups[0]['lr']:.6f}, R2={cal_r2_score(labels, preds):.4f}, Loss={total_loss.item() / steps:.4f}")
                if reset == steps:
                    steps = 0
                    total_loss = torch.Tensor([0.0]).to(device)
                    labels.clear()
                    preds.clear()
        else:
            for batch in loop:
                loss, label, pred = do_train_r2_dict(model, batch, optimizer, device, is_parallel)
                total_loss += loss
                steps += 1
                labels.append(label.ravel())
                preds.append(pred.ravel())
                loop.set_postfix_str(f"LR={optimizer.param_groups[0]['lr']:.6f}, R2={cal_r2_score(labels, preds):.4f}, Loss={total_loss.item() / steps:.4f}")
                if reset == steps:
                    steps = 0
                    total_loss = torch.Tensor([0.0]).to(device)
                    labels.clear()
                    preds.clear()
    loop.close()

    return cal_r2_score(labels, preds), total_loss.item() / steps


def train_epoch_scheduler_r2(
    model, train_loader, optimizer, device, scheduler: LRScheduler, is_tuple_params, is_parallel: bool = False
):
    total_loss = torch.Tensor([0.0]).to(device)
    labels, preds = [], []
    num_iter = len(train_loader)
    reset = get_reset(num_iter)
    if hasattr(model, "fit"):
        if is_tuple_params:
            for batch in train_loader:
                loss, label, pred = do_fit_scheduler_r2(
                    model, batch, optimizer, device, scheduler
                )
                total_loss += loss
                steps += 1
                labels.append(label.ravel())
                preds.append(pred.ravel())
                if reset == steps:
                    steps = 0
                    total_loss = torch.Tensor([0.0]).to(device)
                    labels.clear()
                    preds.clear()
        else:
            for batch in train_loader:
                loss, label, pred = do_fit_scheduler_r2_dict(
                    model, batch, optimizer, device, scheduler
                )
                total_loss += loss
                steps += 1
                labels.append(label.ravel())
                preds.append(pred.ravel())
                if reset == steps:
                    steps = 0
                    total_loss = torch.Tensor([0.0]).to(device)
                    labels.clear()
                    preds.clear()
    else:
        if is_tuple_params:
            for batch in train_loader:
                loss, label, pred = do_train_scheduler_r2(
                    model, batch, optimizer, device, scheduler, is_parallel
                )
                total_loss += loss
                steps += 1
                labels.append(label.ravel())
                preds.append(pred.ravel())
                if reset == steps:
                    steps = 0
                    total_loss = torch.Tensor([0.0]).to(device)
                    labels.clear()
                    preds.clear()
        else:
            for batch in train_loader:
                loss, label, pred = do_train_scheduler_r2_dict(
                    model, batch, optimizer, device, scheduler, is_parallel
                )
                total_loss += loss
                steps += 1
                labels.append(label.ravel())
                preds.append(pred.ravel())
                if reset == steps:
                    steps = 0
                    total_loss = torch.Tensor([0.0]).to(device)
                    labels.clear()
                    preds.clear()

    return cal_r2_score(labels, preds), total_loss.item() / steps


def train_epoch_scheduler_progress_r2(
    model, train_loader, optimizer, device, scheduler, epoch, epochs, is_tuple_params, is_parallel: bool
):
    steps = 0
    total_loss = torch.Tensor([0.0]).to(device)
    labels, preds = [], []
    num_iter = len(train_loader)
    reset = get_reset(num_iter)
    loop = tqdm(
        train_loader,
        desc=f"[Epoch-{epoch}/{epochs} Train]",
        total=len(train_loader),
        colour="green",
    )
    if hasattr(model, "fit"):
        if is_tuple_params:
            for batch in loop:
                loss, label, pred = do_fit_scheduler_r2(
                    model, batch, optimizer, device, scheduler
                )
                total_loss += loss
                steps += 1
                labels.append(label.ravel())
                preds.append(pred.ravel())
                loop.set_postfix_str(f"LR={optimizer.param_groups[0]['lr']:.6f}, R2={cal_r2_score(labels, preds):.4f}, Loss={total_loss.item() / steps:.4f}")
                if reset == steps:
                    steps = 0
                    total_loss = torch.Tensor([0.0]).to(device)
                    labels.clear()
                    preds.clear()
        else:
            for batch in loop:
                loss, label, pred = do_fit_scheduler_r2_dict(
                    model, batch, optimizer, device, scheduler
                )
                total_loss += loss
                steps += 1
                labels.append(label.ravel())
                preds.append(pred.ravel())
                loop.set_postfix_str(f"LR={optimizer.param_groups[0]['lr']:.6f}, R2={cal_r2_score(labels, preds):.4f}, Loss={total_loss.item() / steps:.4f}")
                if reset == steps:
                    steps = 0
                    total_loss = torch.Tensor([0.0]).to(device)
                    labels.clear()
                    preds.clear()
    else:
        if is_tuple_params:
            for batch in loop:
                loss, label, pred = do_train_scheduler_r2(
                    model, batch, optimizer, device, scheduler, is_parallel
                )
                total_loss += loss
                steps += 1
                labels.append(label.ravel())
                preds.append(pred.ravel())
                loop.set_postfix_str(f"LR={optimizer.param_groups[0]['lr']:.6f}, R2={cal_r2_score(labels, preds):.4f}, Loss={total_loss.item() / steps:.4f}")
                if reset == steps:
                    steps = 0
                    total_loss = torch.Tensor([0.0]).to(device)
                    labels.clear()
                    preds.clear()
        else:
            for batch in loop:
                loss, label, pred = do_train_scheduler_r2_dict(
                    model, batch, optimizer, device, scheduler, is_parallel
                )
                total_loss += loss
                steps += 1
                labels.append(label.ravel())
                preds.append(pred.ravel())
                loop.set_postfix_str(f"LR={optimizer.param_groups[0]['lr']:.6f}, R2={cal_r2_score(labels, preds):.4f}, Loss={total_loss.item() / steps:.4f}")
                if reset == steps:
                    steps = 0
                    total_loss = torch.Tensor([0.0]).to(device)
                    labels.clear()
                    preds.clear()

    loop.close()

    return cal_r2_score(labels, preds), total_loss.item() / steps


def do_train_r2(model, batch, optimizer, device, is_parallel: bool):
    outputs, y = _forward_y(model, batch, device, is_parallel)
    loss, logits = r2_loss_logits(outputs, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss, y.cpu().numpy(), logits.detach().cpu().numpy()


def do_train_r2_dict(model, batch, optimizer, device, is_parallel: bool):
    outputs, y = _forward_y_dict(model, batch, device, is_parallel)
    loss, logits = r2_loss_logits(outputs, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss, y.cpu().numpy(), logits.detach().cpu().numpy()


def do_fit_r2(model, batch, optimizer, device):
    outputs, y = _fit_y(model, batch, device)
    loss, logits = r2_loss_logits(outputs, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss, y.cpu().numpy(), logits.detach().cpu().numpy()


def do_fit_r2_dict(model, batch, optimizer, device):
    outputs, y = _fit_y_dict(model, batch, device)
    loss, logits = r2_loss_logits(outputs, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss, y.cpu().numpy(), logits.detach().cpu().numpy()


def do_train_scheduler_r2(model, batch, optimizer, device, scheduler: LRScheduler, is_parallel: bool):
    outputs, y = _forward_y(model, batch, device, is_parallel)
    loss, logits = r2_loss_logits(outputs, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    scheduler.step()
    return loss, y.cpu().numpy(), logits.detach().cpu().numpy()


def do_train_scheduler_r2_dict(model, batch, optimizer, device, scheduler: LRScheduler, is_parallel: bool):
    outputs, y = _forward_y_dict(model, batch, device, is_parallel)
    loss, logits = r2_loss_logits(outputs, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    scheduler.step()
    return loss, loss, y.cpu().numpy(), logits.detach().cpu().numpy()


def do_fit_scheduler_r2(model, batch, optimizer, device, scheduler: LRScheduler):
    outputs, y = _fit_y(model, batch, device)
    loss, logits = r2_loss_logits(outputs, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    scheduler.step()
    return loss, y.cpu().numpy(), logits.detach().cpu().numpy()


def do_fit_scheduler_r2_dict(model, batch, optimizer, device, scheduler: LRScheduler):
    outputs, y = _fit_y_dict(model, batch, device)
    loss, logits = r2_loss_logits(outputs, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    scheduler.step()
    return loss, y.cpu().numpy(), logits.detach().cpu().numpy()


def get_reset(num_iter: int):
    if num_iter <= 4:
        return 0
    elif num_iter <= 8:
        return int(num_iter * 0.5)
    elif num_iter <= 64:
        return int(num_iter * 0.6)
    elif num_iter <= 256:
        return int(num_iter * 0.7)
    elif num_iter <= 512:
        return int(num_iter * 0.8)
    elif num_iter <= 1024:
        return int(num_iter * 0.9)
    else:
        return int(num_iter * 0.95)


def _is_tuple_params(is_tuple_params, data_loader) -> bool:
    return is_tuple_params if is_tuple_params is not None else isinstance(next(iter(data_loader)), (list, tuple))
    