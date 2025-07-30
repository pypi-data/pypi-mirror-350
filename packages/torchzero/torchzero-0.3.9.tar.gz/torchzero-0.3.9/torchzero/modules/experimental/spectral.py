from abc import ABC, abstractmethod
import math
from collections import deque
from typing import Literal, Any

import torch
from ...core import Chainable, TensorwisePreconditioner
from ...utils.linalg.matrix_funcs import matrix_power_eigh
from ...utils.linalg.svd import randomized_svd
from ...utils.linalg.qr import qr_householder


class _Solver:
    @abstractmethod
    def update(self, history: deque[torch.Tensor], damping: float | None) -> tuple[Any, Any]:
        """returns stuff for apply"""
    @abstractmethod
    def apply(self, __g: torch.Tensor, __A:torch.Tensor, __B:torch.Tensor) -> torch.Tensor:
        """apply preconditioning to tensor"""

class _SVDSolver(_Solver):
    def __init__(self, driver=None): self.driver=driver
    def update(self, history, damping):
        M_hist = torch.stack(tuple(history), dim=1)
        device = None # driver is CUDA only
        if self.driver is not None:
            device = M_hist.device
            M_hist = M_hist.cuda()

        try:
            U, S, _ = torch.linalg.svd(M_hist, full_matrices=False, driver=self.driver) # pylint:disable=not-callable

            if self.driver is not None:
                U = U.to(device); S = S.to(device)

            if damping is not None and damping != 0: S.add_(damping)
            return U, S

        except torch.linalg.LinAlgError:
            return None, None

    def apply(self, g: torch.Tensor, U: torch.Tensor, S: torch.Tensor):
        Utg = (U.T @ g).div_(S)
        return U @ Utg

class _SVDLowRankSolver(_Solver):
    def __init__(self, q: int = 6, niter: int = 2): self.q, self.niter = q, niter
    def update(self, history, damping):
        M_hist = torch.stack(tuple(history), dim=1)
        try:
            U, S, _ = torch.svd_lowrank(M_hist, q=self.q, niter=self.niter)
            if damping is not None and damping != 0: S.add_(damping)
            return U, S
        except torch.linalg.LinAlgError:
            return None, None

    def apply(self, g: torch.Tensor, U: torch.Tensor, S: torch.Tensor):
        Utg = (U.T @ g).div_(S)
        return U @ Utg

class _RandomizedSVDSolver(_Solver):
    def __init__(self, k: int = 3, driver: str | None = 'gesvda'):
        self.driver = driver
        self.k = k

    def update(self, history, damping):
        M_hist = torch.stack(tuple(history), dim=1)
        device = None # driver is CUDA only
        if self.driver is not None:
            device = M_hist.device
            M_hist = M_hist.cuda()

        try:
            U, S, _ = randomized_svd(M_hist, k=self.k, driver=self.driver)

            if self.driver is not None:
                U = U.to(device); S = S.to(device)

            if damping is not None and damping != 0: S.add_(damping)
            return U, S

        except torch.linalg.LinAlgError:
            return None, None

    def apply(self, g: torch.Tensor, U: torch.Tensor, S: torch.Tensor):
        Utg = (U.T @ g).div_(S)
        return U @ Utg

class _QRDiagonalSolver(_Solver):
    def __init__(self, sqrt=True): self.sqrt = sqrt
    def update(self, history, damping):
        M_hist = torch.stack(tuple(history), dim=1)
        try:
            Q, R = torch.linalg.qr(M_hist, mode='reduced') # pylint:disable=not-callable
            R_diag = R.diag().abs()
            if damping is not None and damping != 0: R_diag.add_(damping)
            if self.sqrt: R_diag.sqrt_()
            return Q, R_diag
        except torch.linalg.LinAlgError:
            return None, None

    def apply(self, g: torch.Tensor, Q: torch.Tensor, R_diag: torch.Tensor):
        Qtg = (Q.T @ g).div_(R_diag)
        return Q @ Qtg

class _QRSolver(_Solver):
    def __init__(self, sqrt=True): self.sqrt = sqrt
    def update(self, history, damping):
        M_hist = torch.stack(tuple(history), dim=1)
        try:
            # Q: d x k, R: k x k
            Q, R = torch.linalg.qr(M_hist, mode='reduced') # pylint:disable=not-callable
            A = R @ R.T
            if damping is not None and damping != 0: A.diagonal(dim1=-2, dim2=-1).add_(damping)
            if self.sqrt: A = matrix_power_eigh(A, 0.5)
            return Q, A
        except (torch.linalg.LinAlgError):
            return None,None

    def apply(self, g: torch.Tensor, Q: torch.Tensor, A: torch.Tensor) -> torch.Tensor:
        g_proj = Q.T @ g
        y, _ = torch.linalg.solve_ex(A, g_proj) # pylint:disable=not-callable
        return Q @ y

class _QRHouseholderSolver(_Solver):
    def __init__(self, sqrt=True): self.sqrt = sqrt
    def update(self, history, damping):
        M_hist = torch.stack(tuple(history), dim=1)
        try:
            # Q: d x k, R: k x k
            Q, R = qr_householder(M_hist, mode='reduced') # pylint:disable=not-callable
            A = R @ R.T
            if damping is not None and damping != 0: A.diagonal(dim1=-2, dim2=-1).add_(damping)
            if self.sqrt: A = matrix_power_eigh(A, 0.5)
            return Q, A
        except (torch.linalg.LinAlgError):
            return None,None

    def apply(self, g: torch.Tensor, Q: torch.Tensor, A: torch.Tensor) -> torch.Tensor:
        g_proj = Q.T @ g
        y, _ = torch.linalg.solve_ex(A, g_proj) # pylint:disable=not-callable
        return Q @ y


class _EighSolver(_Solver):
    def __init__(self, sqrt=True):
        self.sqrt = sqrt

    def update(self, history, damping):
        M_hist = torch.stack(tuple(history), dim=1)
        grams = M_hist @ M_hist.T # (d, d)
        if damping is not None and damping != 0: grams.diagonal(dim1=-2, dim2=-1).add_(damping)
        try:
            L, Q = torch.linalg.eigh(grams) # L: (d,), Q: (d, d) # pylint:disable=not-callable
            L = L.abs().clamp_(min=1e-12)
            if self.sqrt: L = L.sqrt()
            return Q, L
        except torch.linalg.LinAlgError:
            return None, None

    def apply(self, g: torch.Tensor, Q: torch.Tensor, L: torch.Tensor) -> torch.Tensor:
        Qtg = (Q.T @ g).div_(L)
        return Q @ Qtg


SOLVERS = {
    "svd": _SVDSolver(), # fallbacks on "gesvd" which basically takes ages or just hangs completely
    "svd_gesvdj": _SVDSolver("gesvdj"), # no fallback on slow "gesvd"
    "svd_gesvda": _SVDSolver("gesvda"), # approximate method for wide matrices, sometimes better sometimes worse but faster
    "svd_lowrank": _SVDLowRankSolver(), # maybe need to tune parameters for this, with current ones its slower and worse
    "randomized_svd2": _RandomizedSVDSolver(2),
    "randomized_svd3": _RandomizedSVDSolver(3),
    "randomized_svd4": _RandomizedSVDSolver(4),
    "randomized_svd5": _RandomizedSVDSolver(5),
    "eigh": _EighSolver(), # this is O(n**2) storage, but is this more accurate?
    "qr": _QRSolver(),
    "qr_householder": _QRHouseholderSolver(), # this is slower... but maybe it won't freeze? I think svd_gesvda is better
    "qrdiag": _QRDiagonalSolver(),
}

def maybe_lerp_(state_: dict, beta: float | None, key, value: Any):
    if (key not in state_) or (beta is None) or (not isinstance(value, torch.Tensor)): state_[key] = value
    else:
        if state_[key].shape != value.shape: state_[key] = value
        else: state_[key].lerp_(value, 1-beta)

class SpectralPreconditioner(TensorwisePreconditioner):
    """Whitening preconditioner via SVD on history of past gradients or gradient differences scaled by parameter differences.

    Args:
        history_size (int, optional): number of past gradients to store for preconditioning. Defaults to 10.
        update_freq (int, optional): how often to re-compute the preconditioner. Defaults to 1.
        damping (float, optional): damping term, makes it closer to GD. Defaults to 1e-7.
        order (int, optional):
            whitening order, 1 approximates FIM (maybe), 2 - hessian (maybe), 3+ - god knows what.
        solver (str, optional): what to use for whitening. Defaults to 'svd'.
        A_beta (float | None, optional):
            beta for U (in SVD and other letters in other solvers) (probably a bad idea). Defaults to None.
        B_beta (float | None, optional):
            beta for S (in SVD and other letters in other solvers) (probably a bad idea). Defaults to None.
        interval (int, optional): How often to update history. Defaults to 1 (every step).
        concat_params (bool, optional):
            whether to apply preconditioning to each tensor (False, default) or to all tensors concatenated into a vector (True). Latter will be slower but captures interactions between layers. Defaults to True.
        scale_first (bool, optional): makes first step small, usually not needed. Defaults to False.
        inner (Chainable | None, optional): Inner modules applied after updating preconditioner and before applying it. Defaults to None.
    """
    def __init__(
        self,
        history_size: int = 10,
        update_freq: int = 1,
        damping: float = 1e-12,
        order: int = 1,
        solver: Literal['svd', 'svd_gesvdj', 'svd_gesvda', 'svd_lowrank', 'eigh', 'qr', 'qrdiag', 'qr_householder'] | _Solver | str = 'svd_gesvda',
        A_beta: float | None = None,
        B_beta: float | None = None,
        interval: int = 1,
        concat_params: bool = False,
        scale_first: bool = False,
        inner: Chainable | None = None,
    ):
        if isinstance(solver, str): solver = SOLVERS[solver]
        # history is still updated each step so Precondition's update_freq has different meaning
        defaults = dict(history_size=history_size, update_freq=update_freq, damping=damping, order=order, A_beta=A_beta, B_beta=B_beta, solver=solver)
        super().__init__(defaults, uses_grad=False, concat_params=concat_params, scale_first=scale_first, inner=inner, update_freq=interval)

    @torch.no_grad
    def update_tensor(self, tensor, param, grad, state, settings):
        order = settings['order']
        history_size = settings['history_size']
        update_freq = settings['update_freq']
        damping = settings['damping']
        A_beta = settings['A_beta']
        B_beta = settings['B_beta']
        solver: _Solver = settings['solver']

        if 'history' not in state: state['history'] = deque(maxlen=history_size)
        history = state['history']

        if order == 1: history.append(tensor.clone().view(-1))
        else:

            # if order=2, history is of gradient differences, order 3 is differences between differences, etc
            # normalized by parameter differences
            cur_p = param.clone()
            cur_g = tensor.clone()
            for i in range(1, order):
                if f'prev_g_{i}' not in state:
                    state[f'prev_p_{i}'] = cur_p
                    state[f'prev_g_{i}'] = cur_g
                    break

                s_k = cur_p - state[f'prev_p_{i}']
                y_k = cur_g - state[f'prev_g_{i}']
                state[f'prev_p_{i}'] = cur_p
                state[f'prev_g_{i}'] = cur_g
                cur_p = s_k
                cur_g = y_k

                if i == order - 1:
                    cur_g = cur_g / torch.linalg.norm(cur_p).clip(min=1e-8) # pylint:disable=not-callable
                    history.append(cur_g.view(-1))

        step = state.get('step', 0)
        if step % update_freq == 0 and len(history) != 0:
            A, B = solver.update(history, damping=damping)
            maybe_lerp_(state, A_beta, 'A', A)
            maybe_lerp_(state, B_beta, 'B', B)

        if len(history) != 0:
            state['step'] = step + 1 # do not increment if no history (gathering s_ks and y_ks)

    @torch.no_grad
    def apply_tensor(self, tensor, param, grad, state, settings):
        history_size = settings['history_size']
        solver: _Solver = settings['solver']

        A = state.get('A', None)
        if A is None:
            # make a conservative step to avoid issues due to different GD scaling
            return tensor.clip_(-0.1, 0.1) # pyright:ignore[reportArgumentType]

        B = state['B']
        update = solver.apply(tensor.view(-1), A, B).view_as(tensor)

        n = len(state['history'])
        if n != history_size: update.mul_(n/history_size)
        return update

