import math

import numpy as np
import torch
from torch import nn
import trimesh
from trimesh.caching import TrackedArray


def norm(x, dim=None, keepdims=False):
    """
    compute L2 norm of a tensor or a numpy array
    :param x:
    :return:
    """
    if isinstance(x, np.ndarray):
        return np.linalg.norm(x, axis=dim, keepdims=keepdims)
    elif isinstance(x, torch.Tensor):
        return torch.norm(x.float(), dim=dim, keepdim=keepdims)
    else:
        raise TypeError()


def to_array(x, dtype=float):
    if isinstance(x, np.ndarray):
        return x.astype(dtype)
    elif isinstance(x, torch.Tensor):
        return x.detach().cpu().numpy().astype(dtype)
    elif isinstance(x, list):
        return [to_array(a) for a in x]
    elif isinstance(x, dict):
        return {k: to_array(v) for k, v in x.items()}
    elif isinstance(x, TrackedArray):
        return np.array(x)
    else:
        return x


def exp(x):
    if isinstance(x, np.ndarray):
        return np.exp(x)
    elif isinstance(x, torch.Tensor):
        return torch.exp(x)
    else:
        return math.exp(x)


def to_same_type(x, y, dtype=float):
    """
    return x with the same type of y
    :param x:
    :param y:
    :param dtype:
    :return:
    """
    if isinstance(y, np.ndarray):
        return to_array(x, dtype)
    elif isinstance(y, torch.Tensor):
        if isinstance(x, torch.Tensor):
            return x.to(device=y.device, dtype=dtype)
        else:
            return torch.tensor(x, device=y.device, dtype=dtype)
    else:
        raise TypeError()


def to_same_type_if_present(x, y, dtype=float):
    if x is None:
        return None
    else:
        return to_same_type(x, y, dtype=y.dtype)


def from_numpy_if_present(x, dtype=torch.float):
    if x is None:
        return None
    return torch.from_numpy(x).to(dtype=dtype)


def min_max(x, dim=None):
    if isinstance(x, np.ndarray):
        return x.min(axis=dim), x.max(axis=dim)
    elif isinstance(x, torch.Tensor):
        return x.min(dim=dim).values, x.max(dim=dim).values
    else:
        raise TypeError()


def ptp(x, dim=None):
    if isinstance(x, np.ndarray):
        return x.ptp(axis=dim)
    elif isinstance(x, torch.Tensor):
        return x.max(dim=dim).values - x.min(dim=dim).values
    else:
        raise TypeError()


def random_choice(x, size, dim=None, replace=True):
    if dim is None:
        assert len(x.shape) == 1
        n = x.shape[0]
        idxs = np.random.choice(n, size, replace)
        return x[idxs], idxs
    else:
        n = x.shape[dim]
        idxs = np.random.choice(n, size, replace)
        if isinstance(x, np.ndarray):
            swap_function = np.swapaxes
        elif isinstance(x, torch.Tensor):
            swap_function = torch.transpose
        else:
            raise TypeError()
        x_ = swap_function(x, 0, dim)
        x_ = x_[idxs]
        x_ = swap_function(x_, 0, dim)
        return x_, idxs


def masked_softmax(x, mask, **kwargs):
    x_masked = x.clone()
    x_masked[mask == 0] = -float("inf")

    return torch.softmax(x_masked, **kwargs)


def as_tensor_if_present(data, dtype=None, device=None):
    if data is None:
        return None
    else:
        return torch.as_tensor(data, dtype=dtype, device=device)


def to_tensor_if_present(data, dtype=None, device=None):
    if data is None:
        return None
    else:
        if isinstance(data, torch.Tensor):
            return data.clone().to(dtype=dtype, device=device)
        else:
            return torch.tensor(data, dtype=dtype, device=device)


def to_tensor(data, dtype=None, device=None):
    if isinstance(data, torch.Tensor):
        return data.clone().to(dtype=dtype, device=device)
    else:
        return torch.tensor(data, dtype=dtype, device=device)


def to_tensor_if_present_and_not_ndarray(data, dtype=None, device=None):
    if data is None:
        return None
    elif isinstance(data, np.ndarray):
        return data
    else:
        if isinstance(data, torch.Tensor):
            return data.clone().to(dtype=dtype, device=device)
        else:
            return torch.tensor(data, dtype=dtype, device=device)


def numpy_if_present(data):
    if data is None:
        return None
    else:
        return to_array(data)


def to_device_if_present(data, device):
    if data is None:
        return None
    else:
        return data.to(device=device)


def clone_if_present(data):
    if data is None:
        return None
    elif isinstance(data, np.ndarray):
        return data.copy()
    elif isinstance(data, torch.Tensor):
        return torch.clone(data)
    elif isinstance(data, (int, float, str)):
        return data
    elif isinstance(data, dict):
        return {k: clone_if_present(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clone_if_present(i) for i in data]
    elif isinstance(data, trimesh.Trimesh):
        return data.copy()
    else:
        raise NotImplementedError()


def padded_stack(tensors, dim=0, *, out=None):
    max_dim = max(t.shape[dim] for t in tensors)
    padded_tensors = []
    for t in tensors:
        shape_to_pad = list(t.shape[0:dim]) + [max_dim - t.shape[dim]] + list(t.shape[dim + 1:])
        padded_tensors.append(
            torch.cat((t, torch.full(shape_to_pad, -1000, dtype=t.dtype, device=t.device)), dim=dim)
        )
    return torch.stack(padded_tensors, dim=dim, out=out)


def setdiff1d_pytorch(ar1, ar2, assume_unique=False):
    """
    Find the set difference of two arrays.

    Return the unique values in `ar1` that are not in `ar2`.

    Parameters
    ----------
    ar1 : array_like
        Input array.
    ar2 : array_like
        Input comparison array.
    assume_unique : bool
        If True, the input arrays are both assumed to be unique, which
        can speed up the calculation.  Default is False.

    Returns
    -------
    setdiff1d : ndarray
        1D array of values in `ar1` that are not in `ar2`. The result
        is sorted when `assume_unique=False`, but otherwise only sorted
        if the input is sorted.

    See Also
    --------
    numpy.lib.arraysetops : Module with a number of other functions for
                            performing set operations on arrays.

    Examples
    --------
    >>> a = np.array([1, 2, 3, 2, 4, 1])
    >>> b = np.array([3, 4, 5, 6])
    >>> np.setdiff1d(a, b)
    array([1, 2])

    """
    if assume_unique:
        ar1 = ar1.reshape(-1)
    else:
        ar1 = torch.unique(ar1)
        ar2 = torch.unique(ar2)
    return ar1[in1d_pytorch(ar1, ar2, assume_unique=True, invert=True)]


def clone(x):
    if isinstance(x, torch.Tensor):
        return x.clone()
    elif isinstance(x, np.ndarray):
        return x.copy()
    elif isinstance(x, list):
        return [clone(el) for el in x]
    elif isinstance(x, dict):
        return {k: clone(v) for k, v in x.items()}
    elif isinstance(x, (int, float, str)):
        return x
    else:
        raise TypeError()


def stack(l, dim=0):
    if len(l) == 0:
        return l
    if isinstance(l[0], np.ndarray):
        return np.stack(l, dim)
    else:
        return torch.stack(l, dim)


def floor(x):
    if isinstance(x, np.ndarray):
        return np.floor(x)
    elif isinstance(x, torch.Tensor):
        return torch.floor(x)
    else:
        return math.floor(x)


def ceil(x):
    if isinstance(x, np.ndarray):
        return np.ceil(x)
    elif isinstance(x, torch.Tensor):
        return torch.ceil(x)
    else:
        return math.ceil(x)


def intersect1d_pytorch(ar1, ar2, assume_unique=False, return_indices=False):
    if not assume_unique:
        if return_indices:
            ar1, inv_ind1 = torch.unique(ar1, return_inverse=True)
            perm = torch.arange(inv_ind1.size(0), dtype=inv_ind1.dtype, device=inv_ind1.device)
            inverse, perm = inv_ind1.flip([0]), perm.flip([0])
            ind1 = inverse.new_empty(ar1.size(0)).scatter_(0, inverse, perm)
            ar2, inv_ind2 = torch.unique(ar2, return_inverse=True)
            perm = torch.arange(inv_ind2.size(0), dtype=inv_ind2.dtype, device=inv_ind2.device)
            inverse, perm = inv_ind2.flip([0]), perm.flip([0])
            ind2 = inverse.new_empty(ar2.size(0)).scatter_(0, inverse, perm)
        else:
            ar1 = torch.unique(ar1)
            ar2 = torch.unique(ar2)
    else:
        ar1 = ar1.reshape(-1)
        ar2 = ar2.reshape(-1)

    aux = torch.cat((ar1, ar2))
    if return_indices:
        # aux_sort_indices = torch.argsort(aux)
        aux_sort_indices = torch.from_numpy(np.argsort(to_array(aux), kind='mergesort'))
        aux = aux[aux_sort_indices]
    else:
        aux, _ = aux.sort()

    mask = aux[1:] == aux[:-1]
    int1d = aux[:-1][mask]

    if return_indices:
        ar1_indices = aux_sort_indices[:-1][mask]
        ar2_indices = aux_sort_indices[1:][mask] - ar1.numel()
        if not assume_unique:
            ar1_indices = ind1[ar1_indices]
            ar2_indices = ind2[ar2_indices]

        return int1d, ar1_indices, ar2_indices
    else:
        return int1d


#
# def torch_all_close(x, y, rtol: float = 1e-05, atol: float = 1e-08, equal_nan: bool = False):
#     if isinstance(x, torch.Tensor):
#         return torch.allclose(x.detach().cpu(), y.detach().cpu(), rtol, atol, equal_nan)
#     elif isinstance(x,)

def numel(x):
    if isinstance(x, torch.Tensor):
        return x.numel()
    elif isinstance(x, np.ndarray):
        return x.size
    else:
        raise TypeError()


def zero_module(module):
    for p in module.parameters():
        nn.init.zeros_(p)
    return module
