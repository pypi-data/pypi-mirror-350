import warnings
from functools import partial
from typing import Literal
from collections.abc import Callable
import torch

from ...core import Chainable, apply, Module
from ...utils import vec_to_tensors, TensorList
from ...utils.derivatives import (
    hessian_list_to_mat,
    hessian_mat,
    jacobian_and_hessian_wrt,
)
from ..second_order.newton import lu_solve, cholesky_solve, least_squares_solve

def tropical_sum(x, dim): return torch.amax(x, dim=dim)
def tropical_mul(x, y): return x+y

def tropical_matmul(x: torch.Tensor, y: torch.Tensor):
    # this imlements matmul by calling mul and sum

    x_squeeze = False
    y_squeeze = False

    if x.ndim == 1:
        x_squeeze = True
        x = x.unsqueeze(0)

    if y.ndim == 1:
        y_squeeze = True
        y = y.unsqueeze(1)

    res = tropical_sum(tropical_mul(x.unsqueeze(-1), y.unsqueeze(-3)), dim = -2)

    if x_squeeze: res = res.squeeze(-2)
    if y_squeeze: res = res.squeeze(-1)

    return res

def tropical_dot(x:torch.Tensor, y:torch.Tensor):
    assert x.ndim == 1 and y.ndim == 1
    return tropical_matmul(x.unsqueeze(0), y.unsqueeze(1))

def tropical_outer(x:torch.Tensor, y:torch.Tensor):
    assert x.ndim == 1 and y.ndim == 1
    return tropical_matmul(x.unsqueeze(1), y.unsqueeze(0))


def tropical_solve(A: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
    r = b.unsqueeze(1) - A
    return r.amin(dim=-2)

def tropical_solve_and_reconstruct(A: torch.Tensor, b: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    r = b.unsqueeze(1) - A
    x = r.amin(dim=-2)
    b_hat = tropical_matmul(A, x)
    return x, b_hat

def tikhonov(H: torch.Tensor, reg: float):
    if reg!=0: H += torch.eye(H.size(-1), dtype=H.dtype, device=H.device) * reg
    return H


class TropicalNewton(Module):
    """suston"""
    def __init__(
        self,
        reg: float | None = None,
        hessian_method: Literal["autograd", "func", "autograd.functional"] = "autograd",
        vectorize: bool = True,
        interpolate:bool=False,
        inner: Chainable | None = None,
    ):
        defaults = dict(reg=reg, hessian_method=hessian_method, vectorize=vectorize, interpolate=interpolate)
        super().__init__(defaults)

        if inner is not None:
            self.set_child('inner', inner)

    @torch.no_grad
    def step(self, vars):
        params = TensorList(vars.params)
        closure = vars.closure
        if closure is None: raise RuntimeError('NewtonCG requires closure')

        settings = self.settings[params[0]]
        reg = settings['reg']
        hessian_method = settings['hessian_method']
        vectorize = settings['vectorize']
        interpolate = settings['interpolate']

        # ------------------------ calculate grad and hessian ------------------------ #
        if hessian_method == 'autograd':
            with torch.enable_grad():
                loss = vars.loss = vars.loss_approx = closure(False)
                g_list, H_list = jacobian_and_hessian_wrt([loss], params, batched=vectorize)
                g_list = [t[0] for t in g_list] # remove leading dim from loss
                vars.grad = g_list
                H = hessian_list_to_mat(H_list)

        elif hessian_method in ('func', 'autograd.functional'):
            strat = 'forward-mode' if vectorize else 'reverse-mode'
            with torch.enable_grad():
                g_list = vars.get_grad(retain_graph=True)
                H: torch.Tensor = hessian_mat(partial(closure, backward=False), params,
                                method=hessian_method, vectorize=vectorize, outer_jacobian_strategy=strat) # pyright:ignore[reportAssignmentType]

        else:
            raise ValueError(hessian_method)

        # -------------------------------- inner step -------------------------------- #
        if 'inner' in self.children:
            g_list = apply(self.children['inner'], list(g_list), params=params, grads=list(g_list), vars=vars)
        g = torch.cat([t.view(-1) for t in g_list])

        # ------------------------------- regulazition ------------------------------- #
        if reg is not None: H = tikhonov(H, reg)

        # ----------------------------------- solve ---------------------------------- #
        tropical_update, g_hat = tropical_solve_and_reconstruct(H, g)

        g_norm = torch.linalg.vector_norm(g) # pylint:disable=not-callable
        abs_error = torch.linalg.vector_norm(g-g_hat) # pylint:disable=not-callable
        rel_error = abs_error/g_norm.clip(min=1e-8)

        if interpolate:
            if rel_error > 1e-8:

                update = cholesky_solve(H, g)
                if update is None: update = lu_solve(H, g)
                if update is None: update = least_squares_solve(H, g)

                tropical_update.lerp_(update.ravel(), rel_error.clip(max=1))

        vars.update = vec_to_tensors(tropical_update, params)
        return vars