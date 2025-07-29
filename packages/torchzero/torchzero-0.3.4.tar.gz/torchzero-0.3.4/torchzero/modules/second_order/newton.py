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


def lu_solve(H: torch.Tensor, g: torch.Tensor):
    x, info = torch.linalg.solve_ex(H, g) # pylint:disable=not-callable
    if info == 0: return x
    return None

def cholesky_solve(H: torch.Tensor, g: torch.Tensor):
    x, info = torch.linalg.cholesky_ex(H) # pylint:disable=not-callable
    if info == 0:
        g.unsqueeze_(1)
        return torch.cholesky_solve(g, x)
    return None

def least_squares_solve(H: torch.Tensor, g: torch.Tensor):
    return torch.linalg.lstsq(H, g)[0] # pylint:disable=not-callable

def eigh_solve(H: torch.Tensor, g: torch.Tensor, tfm: Callable | None):
    try:
        L, Q = torch.linalg.eigh(H) # pylint:disable=not-callable
        if tfm is not None: L = tfm(L)
        L.reciprocal_()
        return torch.linalg.multi_dot([Q * L.unsqueeze(-2), Q.mH, g]) # pylint:disable=not-callable
    except torch.linalg.LinAlgError:
        return None

def tikhonov_(H: torch.Tensor, reg: float):
    if reg!=0: H.add_(torch.eye(H.size(-1), dtype=H.dtype, device=H.device).mul_(reg))
    return H

def eig_tikhonov_(H: torch.Tensor, reg: float):
    v = torch.linalg.eigvalsh(H).min().clamp_(max=0).neg_() + reg # pylint:disable=not-callable
    return tikhonov_(H, v)


class Newton(Module):
    """Exact newton via autograd.

    Args:
        reg (float, optional): tikhonov regularizer value. Defaults to 1e-6.
        eig_reg (bool, optional): whether to use largest negative eigenvalue as regularizer. Defaults to False.
        hessian_method (str):
            how to calculate hessian. Defaults to "autograd".
        vectorize (bool, optional):
            whether to enable vectorized hessian. Defaults to True.
        inner (Chainable | None, optional): inner modules. Defaults to None.
        H_tfm (Callable | None, optional):
            optional hessian transforms, takes in two arguments - `(hessian, gradient)`.

            must return a tuple: `(hessian, is_inverted)` with transformed hessian and a boolean value
            which must be True if transform inverted the hessian and False otherwise. Defaults to None.
        eigval_tfm (Callable | None, optional):
            optional eigenvalues transform, for example :code:`torch.abs` or :code:`lambda L: torch.clip(L, min=1e-8)`.
            If this is specified, eigendecomposition will be used to solve Hx = g.

    """
    def __init__(
        self,
        reg: float = 1e-6,
        eig_reg: bool = False,
        hessian_method: Literal["autograd", "func", "autograd.functional"] = "autograd",
        vectorize: bool = True,
        inner: Chainable | None = None,
        H_tfm: Callable[[torch.Tensor, torch.Tensor], tuple[torch.Tensor, bool]] | None = None,
        eigval_tfm: Callable[[torch.Tensor], torch.Tensor] | None = None,
    ):
        defaults = dict(reg=reg, eig_reg=eig_reg, abs=abs,hessian_method=hessian_method, vectorize=vectorize, H_tfm=H_tfm, eigval_tfm=eigval_tfm)
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
        eig_reg = settings['eig_reg']
        hessian_method = settings['hessian_method']
        vectorize = settings['vectorize']
        H_tfm = settings['H_tfm']
        eigval_tfm = settings['eigval_tfm']

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
        if eig_reg: H = eig_tikhonov_(H, reg)
        else: H = tikhonov_(H, reg)

        # ----------------------------------- solve ---------------------------------- #
        update = None
        if H_tfm is not None:
            H, is_inv = H_tfm(H, g)
            if is_inv: update = H

        if eigval_tfm is not None:
            update = eigh_solve(H, g, eigval_tfm)

        if update is None: update = cholesky_solve(H, g)
        if update is None: update = lu_solve(H, g)
        if update is None: update = least_squares_solve(H, g)

        vars.update = vec_to_tensors(update, params)
        return vars