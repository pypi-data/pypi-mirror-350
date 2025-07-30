"""
torch functions
"""

import os
import threading

import numpy as np
import torch
import torch.nn as nn

threading_local = threading.local()


def tensor(v):
    if isinstance(v, torch.Tensor):
        return cuda(v)
    else:
        return cuda(torch.tensor(v))


def tensorf(v):
    return torch.tensor(v).float()


def device(module):
    if hasattr(module, '_is_replica') and module._is_replica:
        if hasattr(module, 'weight'):
            return module.weight.device
        for _value in module.modules():
            if _value is module:
                continue
            _device = device(_value)
            if _device is not None:
                return _device
        return None
    else:
        return next(module.parameters()).device


def zeros(*args):
    v = torch.zeros(*args)
    return tensor(v)


def ones(*args):
    v = torch.ones(*args)
    return tensor(v)


def full(*args, **kwargs):
    v = torch.full(*args, **kwargs)
    return tensor(v)


def arange(*args, **kwargs):
    v = torch.arange(*args, **kwargs)
    return tensor(v)


def logical_or(a, b, *args, **kwargs):
    _logical_or = torch.logical_or if torch.is_tensor(a) else np.logical_or
    return _logical_or(a, b, *args, **kwargs)


def clip(values, *args, **kwargs):
    _clip = torch.clamp if torch.is_tensor(values) else np.clip
    return _clip(values, *args, **kwargs)


def stack(values, *args, **kwargs):
    _stack = torch.stack if torch.is_tensor(values[0]) else np.stack
    _fix_dim_axis(torch.is_tensor(values), kwargs)
    return _stack(values, *args, **kwargs)


def cat(values, *args, **kwargs):
    _cat = torch.cat if torch.is_tensor(values[0]) else np.concatenate
    _fix_dim_axis(torch.is_tensor(values), kwargs)
    return _cat(values, *args, **kwargs)


def zeros_like(values, *args, **kwargs):
    _func = torch.zeros_like if torch.is_tensor(values) else np.zeros_like
    return _func(values, *args, **kwargs)


def isempty(values):
    return values.numel() == 0 if torch.is_tensor(values) else values.size == 0


def atan2(a, b):
    _func = torch.atan2 if torch.is_tensor(a) else np.arctan2
    return _func(a, b)


def rad2deg(values):
    return torch.rad2deg(values) if torch.is_tensor(values) else np.rad2deg(values)


def empty_like(values: np.ndarray | torch.Tensor, dtype=None):
    is_tensor = torch.is_tensor(values)
    dtype = (
        make_dtype(dtype, 'tensor' if is_tensor else 'numpy') if dtype is not None else values.dtype
    )
    if is_tensor:
        return torch.zeros(  # type: ignore
            (0, *values.shape[1:]),
            dtype=dtype,  # type: ignore
            device=values.device,  # type:ignore
        )
    else:
        return np.zeros(  # type: ignore
            (0, *values.shape[1:]),
            dtype=dtype,  # type: ignore
        )


def _fix_dim_axis(is_tensor, kwargs):
    if is_tensor:
        if 'axis' in kwargs:
            kwargs['dim'] = kwargs['axis']
            del kwargs['axis']
    else:
        if 'dim' in kwargs:
            kwargs['axis'] = kwargs['dim']
            del kwargs['dim']


def round(values, *args, **kwargs):
    _round = torch.round if torch.is_tensor(values) else np.round
    return _round(values, *args, **kwargs)


def randn(*args, **kwargs):
    v = torch.randn(*args, **kwargs)
    return tensor(v)


def astype(values, dtype):
    is_tensor = torch.is_tensor(values)
    if dtype in ['long', 'int64']:
        return values.long() if is_tensor else values.astype(np.int64)
    elif dtype in ['uint8', 'byte']:
        return values.byte() if is_tensor else values.astype(np.uint8)
    elif dtype in ['int64', 'short']:
        return values.short() if is_tensor else values.astype(np.int16)
    elif dtype in ['int', 'int32']:
        return values.int() if is_tensor else values.astype(np.int32)
    elif dtype in ['float', 'float32']:
        return values.float() if is_tensor else values.astype(np.float32)
    elif dtype in ['double', 'float64']:
        return values.double() if is_tensor else values.astype(np.float64)
    elif dtype in ['bool']:
        return values.bool() if is_tensor else values.astype(np.bool_)
    else:
        raise NotImplementedError()


def make_dtype(dtype, mode):
    is_tensor = mode == 'tensor'
    if dtype in ['long', 'int64']:
        return torch.long if is_tensor else np.int64
    elif dtype in ['uint8', 'byte']:
        return torch.uint8 if is_tensor else np.uint8
    elif dtype in ['int64', 'short']:
        return torch.short if is_tensor else np.int16
    elif dtype in ['int', 'int32']:
        return torch.int if is_tensor else np.int32
    elif dtype in ['float', 'float32']:
        return torch.float32 if is_tensor else np.float32
    elif dtype in ['double', 'float64']:
        return torch.float64 if is_tensor else np.float64
    elif dtype in ['bool']:
        return torch.bool if is_tensor else np.bool_
    else:
        raise NotImplementedError()


def ranf(a=0, b=1):
    return np.random.ranf() * (b - a) + a


def sequence_mask(lengths, max_len=None):
    batch_size = lengths.numel()
    max_len = max_len or (lengths.max() if lengths.sum() > 0 else 0)
    if 0 == batch_size:
        return zeros(batch_size, 0).type_as(lengths)
    return (
        torch.arange(0, max_len)
        .to(lengths.device)
        .type_as(lengths)
        .repeat(batch_size, 1)
        .lt(lengths.unsqueeze(1))
    )


def pad(value, full_size, dim=0, pad_value=0):
    if full_size == value.shape[dim]:
        return value
    padding = [0] * (value.dim() * 2)
    padding[-dim * 2 - 1] = full_size - value.shape[dim]
    padded_value = nn.functional.pad(value, padding, value=pad_value)
    return padded_value


def majority(data):
    values, counts = np.unique(data, return_counts=True)
    if counts.size == 0:
        return None
    return values[counts.argmax()]


def softmax_mask(val, mask):
    return -1e18 * (1 - mask.float()) + val


def onehot(val, dim):
    shape = list(val.shape) + [dim]
    onehot = zeros(*shape).scatter_(-1, val.unsqueeze(-1), 1)
    return onehot


def to_numpy_if_possible(values):
    if torch.is_tensor(values):
        return values.cpu().numpy()
    else:
        return values


def to_numpy_force(values):
    if torch.is_tensor(values):
        return values.cpu().numpy()
    else:
        return np.array(values)


def gpu_available():
    return torch.cuda.is_available()


def use_device(device):
    threading_local.gpu = device


def current_device():
    def __get_device_setting(device):
        return int(os.environ[device]) if device in os.environ else None

    if hasattr(threading_local, 'gpu'):
        return threading_local.gpu
    else:
        device = __get_device_setting('MT_GPU')
        if device is not None:
            return device
        else:
            return __get_device_setting('MT_TRAINER')


def cuda(module, device=None):
    if device is None:
        device = current_device()
    if device is None or device == -1 or not gpu_available():
        return module
    else:
        device = torch.cuda._device(device)
        module = module.to(device)
        if hasattr(module, '_set_device'):
            module._set_device(device)
        return module


def load_checkpoint(path):
    return torch.load(path, map_location=lambda storage, location: storage)


def clone_states(module):
    states = module.state_dict()
    for key in states:
        states[key] = states[key].clone().cpu()
    return states


def multinomial(x, padding_ids, best_in_k=1):
    _, mids = x.max(-1)
    pad_mask = 0
    for padding_id in padding_ids:
        pad_mask += (mids == padding_id).long()
    if 1 == best_in_k:
        x = x.multinomial(1).squeeze(1)
    else:
        ids = x.multinomial(best_in_k, replacement=False)
        x = x.gather(-1, ids)
        _, m = x.max(-1)
        x = ids.gather(-1, m.unsqueeze(1)).squeeze(-1)
    x = x * (1 - pad_mask) + padding_id * pad_mask
    return x


def inv_sigmoid(values):
    if isinstance(values, float):
        values = np.float32(values)
    return np.log(values.clip(1e-18)) - np.log((1 - values).clip(1e-18))


def unique(values):
    return [x for i, x in enumerate(values) if i == values.index(x)]


def align1d(value, mlen, fill=0):
    if torch.is_tensor(value):
        fill = torch.tensor(fill, dtype=value.dtype, device=value.device)
        return torch.cat([value] + [fill.unsqueeze(dim=0)] * (mlen - len(value)))
    else:
        return list(value) + [fill] * (mlen - len(value))


def align2d(values, fill=0):
    mlen = max([len(row) for row in values])
    return [align1d(row, mlen, fill) for row in values]


def align3d(values, fill=0):
    lengths = [[len(x) for x in y] for y in values]
    maxlen0 = max([max(x) for x in lengths])
    maxlen1 = max([len(x) for x in lengths])
    nvalues = []
    for row in values:
        nrow = []
        for line in row:
            line = list(line) + [fill] * (maxlen0 - len(line))
            nrow.append(line)
        nrow += [[fill] * maxlen0] * (maxlen1 - len(row))
        nvalues.append(nrow)
    return nvalues


def eval_dim(values):
    dim = 0
    inp = values
    while (
        isinstance(inp, list)
        or isinstance(inp, tuple)
        or isinstance(inp, np.ndarray)
        or (isinstance(inp, torch.Tensor) and inp.dim() > 0)
    ):
        dim += 1
        if 0 == len(inp):
            return dim
        inp = inp[0]
    return dim


def align(values, fill=0):
    dim = 0
    values = list(values)
    dim = eval_dim(values) - eval_dim(fill)
    if dim == 1:
        return values
    elif dim == 2:
        return align2d(values, fill)
    elif dim == 3:
        return align3d(values, fill)
    else:
        raise NotImplementedError()


def chunk(values, size, overlap=0):
    if not isinstance(values, list) and not torch.is_tensor(values):
        values = list(values)
    if len(values) == 0:
        return
    if len(values) <= overlap:
        yield values
    else:
        for i in range(0, len(values) - overlap, size - overlap):
            yield values[i : i + size]


def enumerate_pairs(group, both_size=False):
    if isinstance(group, int):
        group = list(range(group))
    for j in range(len(group)):
        for i in range(j):
            yield group[i], group[j]
            if both_size:
                yield group[j], group[i]


def deeper_chunk(values, size, depth=1):
    assert depth >= 1
    if not isinstance(values, list) and not torch.is_tensor(values):
        values = list(values)

    def deeper_len(value, depth):
        if depth == 0:
            return len(value)
        else:
            return sum([deeper_len(v, depth - 1) for v in value])

    offset, total_length = 0, 0
    for i in range(len(values)):
        curr_length = deeper_len(values[i], depth - 1)
        if total_length + curr_length > size:
            yield values[offset:i]
            offset, total_length = i, 0
        total_length += curr_length
    if offset != len(values):
        yield values[offset:]


def trace(x, access):
    q = [e for e in x]
    visited = set(q)
    while q:
        e = q.pop(0)
        access(e)
        for c in e.children:
            if c not in visited:
                visited.add(c)
                q.append(c)


def flatten(l2):
    return [item for l1 in l2 for item in l1]


def dropout(value, dropout):
    return dropout(value) if value.numel() > 0 else value


def dropout_layer(tensor, dropout, training=True):
    if training and np.random.ranf() < dropout:
        return tensor * 0.0
    else:
        return tensor


def dropout_batch_layer(tensors, dropout, training=True):
    if training and np.random.ranf() < dropout:
        mask = np.random.choice([True, False], size=tensors[0].shape[0], p=[dropout, 1 - dropout])
        for tensor in tensors:
            tensor[mask, :] = 0


def mask_region(mask):
    ys, xs = np.where(mask)
    region = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    return region
