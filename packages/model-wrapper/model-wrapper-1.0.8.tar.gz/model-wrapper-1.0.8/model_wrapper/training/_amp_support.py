from tqdm import tqdm
import torch
from torch.optim.lr_scheduler import LRScheduler
from torch.amp import autocast
try:
    from torch.amp import GradScaler
except ImportError:
    from torch.cuda.amp import GradScaler

from model_wrapper.utils import cal_count, cal_correct, get_workers, get_device, acc_predict

from ._support import get_reset, _forward, _forward_dict, _fit, _fit_dict, _fit_y_dict, _forward_y, _forward_y_dict, \
    _fit_y,  acc_loss_logits, cal_r2_score, r2_loss_logits, get_forward_fn, get_forward_y_fn


def do_train(model, batch, optimizer, device, scaler: GradScaler, forward_fn):
    optimizer.zero_grad()
    with autocast('cuda'):
        loss, _ = forward_fn(model, batch, device)
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
    return loss


def do_train_scheduler(model, batch, optimizer, device, scheduler: LRScheduler, scaler: GradScaler, forward_fn):
    optimizer.zero_grad()
    with autocast('cuda'):
        loss, _ = forward_fn(model, batch, device)
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
    return loss


def train_epoch_base(model, train_loader, optimizer, device, is_tuple_params, scaler: GradScaler):
    steps = 0
    total_loss = torch.Tensor([0.0]).to(device)
    num_iter = len(train_loader)
    reset = get_reset(num_iter)
    forward_fn = get_forward_fn(model, train_loader, is_tuple_params)

    for batch in train_loader:
        loss = do_train(model, batch, optimizer, device, scaler, forward_fn)
        total_loss += loss
        steps += 1
        if reset == steps:
            steps = 0
            total_loss = torch.Tensor([0.0]).to(device)

    return total_loss.item() / steps


def train_epoch_progress(
    model, train_loader, optimizer, device, epoch, epochs, is_tuple_params, scaler: GradScaler
):
    steps = 0
    total_loss = torch.Tensor([0.0]).to(device)
    num_iter = len(train_loader)
    reset = get_reset(num_iter)
    forward_fn = get_forward_fn(model, train_loader, is_tuple_params)

    loop = tqdm(
        train_loader,
        desc=f"[Epoch-{epoch}/{epochs} Train]",
        total=len(train_loader),
        colour="green",
    )
    
    for batch in loop:
        loss = do_train(model, batch, optimizer, device, scaler, forward_fn)
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
    model, train_loader, optimizer, device, scheduler: LRScheduler, is_tuple_params, scaler: GradScaler
):
    steps = 0
    total_loss = torch.Tensor([0.0]).to(device)
    num_iter = len(train_loader)
    reset = get_reset(num_iter)
    forward_fn = get_forward_fn(model, train_loader, is_tuple_params)
    
    for batch in train_loader:
        loss = do_train_scheduler(model, batch, optimizer, device, scheduler, scaler, forward_fn)
        total_loss += loss
        steps += 1
        if reset == steps:
            steps = 0
            total_loss = torch.Tensor([0.0]).to(device)

    return total_loss.item() / steps


def train_epoch_scheduler_progress(
    model, train_loader, optimizer, device, scheduler, epoch, epochs, is_tuple_params, scaler: GradScaler
):
    steps = 0
    total_loss = torch.Tensor([0.0]).to(device)
    num_iter = len(train_loader)
    reset = get_reset(num_iter)
    forward_fn = get_forward_fn(model, train_loader, is_tuple_params)

    loop = tqdm(
        train_loader,
        desc=f"[Epoch-{epoch}/{epochs} Train]",
        total=len(train_loader),
        colour="green",
    )
    
    for batch in loop:
        loss = do_train_scheduler(model, batch, optimizer, device, scheduler, scaler, forward_fn)
        total_loss += loss
        steps += 1
        loop.set_postfix_str(f"LR={optimizer.param_groups[0]['lr']:.6f}, Loss={total_loss.item() / steps:.4f}")
        if reset == steps:
            steps = 0
            total_loss = torch.Tensor([0.0]).to(device)

    loop.close()
    return total_loss.item() / steps

def amp_train_epoch(
    model,
    train_loader,
    optimizer,
    device,
    scheduler,
    epoch,
    epochs,
    show_progress,
    is_tuple_params,
    scaler: GradScaler
):
    if show_progress:
        if scheduler is None:
            return train_epoch_progress(
                model, train_loader, optimizer, device, epoch, epochs, is_tuple_params, scaler
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
            scaler
        )
    else:
        if scheduler is None:
            return train_epoch_base(
                model, train_loader, optimizer, device, is_tuple_params, scaler
            )
        return train_epoch_scheduler(
            model, train_loader, optimizer, device, scheduler, is_tuple_params, scaler
        )
    
# ==========================================================================================================

def do_train_acc(model, batch, optimizer, device, weight, is_parallel: bool, scaler: GradScaler, forward_fn):
    optimizer.zero_grad()
    with autocast('cuda'):
        outputs, y = forward_fn(model, batch, device, is_parallel)
        loss, logits = acc_loss_logits(outputs, y, None if weight is None else weight.to(device))
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
    return loss, cal_count(y), cal_correct(logits.detach(), y)


def do_train_scheduler_acc(
        model, batch, optimizer, device, weight, scheduler: LRScheduler, is_parallel: bool, scaler: GradScaler, forward_fn
    ):
    optimizer.zero_grad()
    with autocast('cuda'):
        outputs, y = forward_fn(model, batch, device, is_parallel)
        loss, logits = acc_loss_logits(outputs, y, None if weight is None else weight.to(device))
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
    scheduler.step()
    return loss, cal_count(y), cal_correct(logits.detach(), y)


def train_epoch_base_acc(model, train_loader, optimizer, device, weight, is_tuple_params, is_parallel: bool, scaler: GradScaler):
    total, steps, total_correct = 0, 0, 0
    total_loss = torch.Tensor([0.0]).to(device)
    num_iter = len(train_loader)
    reset = get_reset(num_iter)
    forward_fn = get_forward_y_fn(model, train_loader, is_tuple_params)

    for batch in train_loader:
        loss, count, correct = do_train_acc(model, batch, optimizer, device, weight, is_parallel, scaler, forward_fn)
        total_loss += loss
        total += count
        total_correct += correct
        steps += 1
        if reset == steps:
            total, steps, total_correct = 0, 0, 0
            total_loss = torch.Tensor([0.0]).to(device)

    return total_correct / total, total_loss.item() / steps


def train_epoch_progress_acc(
    model, train_loader, optimizer, device, epoch, epochs, weight, is_tuple_params, is_parallel: bool, scaler: GradScaler
):
    total, steps, total_correct = 0, 0, 0
    total_loss = torch.Tensor([0.0]).to(device)
    num_iter = len(train_loader)
    reset = get_reset(num_iter)
    forward_fn = get_forward_y_fn(model, train_loader, is_tuple_params)

    loop = tqdm(
        train_loader,
        desc=f"[Epoch-{epoch}/{epochs} Train]",
        total=len(train_loader),
        colour="green",
    )
    
    for batch in loop:
        loss, count, correct = do_train_acc(model, batch, optimizer, device, weight, is_parallel, scaler, forward_fn)
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
    model, train_loader, optimizer, device, weight, scheduler: LRScheduler, is_tuple_params, is_parallel: bool, scaler: GradScaler
):
    total, steps, total_correct = 0, 0, 0
    total_loss = torch.Tensor([0.0]).to(device)
    num_iter = len(train_loader)
    reset = get_reset(num_iter)
    forward_fn = get_forward_y_fn(model, train_loader, is_tuple_params)
    
    for batch in train_loader:
        loss, count, correct = do_train_scheduler_acc(
            model, batch, optimizer, device, weight, scheduler, is_parallel, scaler, forward_fn
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
    model, train_loader, optimizer, device, weight, scheduler, epoch, epochs, is_tuple_params, is_parallel: bool, scaler: GradScaler
):
    total, steps, total_correct = 0, 0, 0
    total_loss = torch.Tensor([0.0]).to(device)
    num_iter = len(train_loader)
    reset = get_reset(num_iter)
    forward_fn = get_forward_y_fn(model, train_loader, is_tuple_params)

    loop = tqdm(
        train_loader,
        desc=f"[Epoch-{epoch}/{epochs} Train]",
        total=len(train_loader),
        colour="green",
    )
    
    for batch in loop:
        loss, count, correct = do_train_scheduler_acc(
            model, batch, optimizer, device, weight, scheduler, is_parallel, scaler, forward_fn
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


def amp_train_epoch_acc(
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
    scaler: GradScaler
):
    if show_progress:
        if scheduler is None:
            return train_epoch_progress_acc(
                model, train_loader, optimizer, device, epoch, epochs, weight, is_tuple_params, is_parallel, scaler
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
            scaler
        )
    else:
        if scheduler is None:
            return train_epoch_base_acc(
                model, train_loader, optimizer, device, weight, is_tuple_params, is_parallel, scaler
            )
        return train_epoch_scheduler_acc(
            model, train_loader, optimizer, device, scheduler, weight, is_tuple_params, is_parallel, scaler
        )

# ============================================================================

def do_train_r2(model, batch, optimizer, device, is_parallel: bool, scaler: GradScaler, forward_fn):
    optimizer.zero_grad()
    with autocast('cuda'):
        outputs, y = forward_fn(model, batch, device, is_parallel)
        loss, logits = r2_loss_logits(outputs, y)
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
    return loss, y.cpu().numpy(), logits.detach().cpu().numpy()


def do_train_scheduler_r2(model, batch, optimizer, device, scheduler: LRScheduler, is_parallel: bool, scaler: GradScaler, forward_fn):
    optimizer.zero_grad()
    with autocast('cuda'):
        outputs, y = forward_fn(model, batch, device, is_parallel)
        loss, logits = r2_loss_logits(outputs, y)
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
    scheduler.step()
    return loss, y.cpu().numpy(), logits.detach().cpu().numpy()


def train_epoch_base_r2(model, train_loader, optimizer, device, is_tuple_params, is_parallel, scaler: GradScaler):
    steps = 0
    total_loss = torch.Tensor([0.0]).to(device)
    labels, preds = [], []
    num_iter = len(train_loader)
    reset = get_reset(num_iter)
    forward_fn = get_forward_y_fn(model, train_loader, is_tuple_params)

    for batch in train_loader:
        loss, label, pred = do_train_r2(model, batch, optimizer, device, is_parallel, scaler, forward_fn)
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
    model, train_loader, optimizer, device, epoch, epochs, is_tuple_params, is_parallel, scaler: GradScaler
):
    steps = 0
    total_loss = torch.Tensor([0.0]).to(device)
    labels, preds = [], []
    num_iter = len(train_loader)
    reset = get_reset(num_iter)
    forward_fn = get_forward_y_fn(model, train_loader, is_tuple_params)

    loop = tqdm(
        train_loader,
        desc=f"[Epoch-{epoch}/{epochs} Train]",
        total=len(train_loader),
        colour="green",
    )
    
    for batch in loop:
        loss, label, pred = do_train_r2(model, batch, optimizer, device, is_parallel, scaler, forward_fn)
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
    model, train_loader, optimizer, device, scheduler: LRScheduler, is_tuple_params, is_parallel: bool, scaler: GradScaler
):
    total_loss = torch.Tensor([0.0]).to(device)
    labels, preds = [], []
    num_iter = len(train_loader)
    reset = get_reset(num_iter)
    forward_fn = get_forward_y_fn(model, train_loader, is_tuple_params)

    for batch in train_loader:
        loss, label, pred = do_train_scheduler_r2(
            model, batch, optimizer, device, scheduler, is_parallel, scaler, forward_fn
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
    model, train_loader, optimizer, device, scheduler, epoch, epochs, is_tuple_params, is_parallel: bool, scaler: GradScaler
):
    steps = 0
    total_loss = torch.Tensor([0.0]).to(device)
    labels, preds = [], []
    num_iter = len(train_loader)
    reset = get_reset(num_iter)
    forward_fn = get_forward_y_fn(model, train_loader, is_tuple_params)

    loop = tqdm(
        train_loader,
        desc=f"[Epoch-{epoch}/{epochs} Train]",
        total=len(train_loader),
        colour="green",
    )
   
    for batch in loop:
        loss, label, pred = do_train_scheduler_r2(
            model, batch, optimizer, device, scheduler, is_parallel, scaler, forward_fn
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


def amp_train_epoch_r2(
    model,
    train_loader,
    optimizer,
    device,
    scheduler,
    epoch,
    epochs,
    show_progress,
    is_tuple_params,
    is_parallel: bool,
    scaler: GradScaler
):
    if show_progress:
        if scheduler is None:
            return train_epoch_progress_r2(
                model, train_loader, optimizer, device, epoch, epochs, is_tuple_params, is_parallel, scaler
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
            is_parallel, 
            scaler
        )
    else:
        if scheduler is None:
            return train_epoch_base_r2(
                model, train_loader, optimizer, device, is_tuple_params, is_parallel, scaler
            )
        return train_epoch_scheduler_r2(
            model, train_loader, optimizer, device, scheduler, is_tuple_params, is_parallel, scaler
        )
