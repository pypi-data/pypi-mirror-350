from operator import itemgetter
from typing import Literal

import torch

from ...core import Module, Target, Transform, Chainable, Vars, apply
from ...utils import NumberList, TensorList
from ..functional import sqrt_centered_ema_sq_, sqrt_ema_sq_


def rmsprop_(
    tensors_: TensorList,
    exp_avg_sq_: TensorList,
    smoothing: float | NumberList,
    eps: float | NumberList,
    debiased: bool,
    step: int,
    exp_avg_: TensorList | None = None,
    max_exp_avg_sq_: TensorList | None = None,
    pow: float = 2,

    # inner args
    inner: Module | None = None,
    params: list[torch.Tensor] | None = None,
    grads: list[torch.Tensor] | None = None,
    vars: Vars | None = None,
):
    """returns `tensors_`"""
    if exp_avg_ is not None:
        sqrt_exp_avg_sq = sqrt_centered_ema_sq_(tensors=tensors_, exp_avg_=exp_avg_,
                                                exp_avg_sq_=exp_avg_sq_,max_exp_avg_sq_=max_exp_avg_sq_,
                                                beta=smoothing,debiased=debiased,step=step,pow=pow)
    else:
        sqrt_exp_avg_sq = sqrt_ema_sq_(tensors=tensors_,exp_avg_sq_=exp_avg_sq_,max_exp_avg_sq_=max_exp_avg_sq_,
                                       beta=smoothing,debiased=debiased,step=step,pow=pow)

    if inner is not None:
        assert params is not None
        tensors_ = TensorList(apply(inner, tensors_, params=params, grads=grads, vars=vars))

    return tensors_.div_(sqrt_exp_avg_sq.add_(eps))

class RMSprop(Transform):
    """Divides graient by EMA of gradient squares. Matches pytorch RMSprop if "init" is set to "zeros".

    Args:
        smoothing (float, optional): beta for exponential moving average of gradient squares. Defaults to 0.99.
        eps (float, optional): epsilon for division. Defaults to 1e-8.
        centered (bool, optional): whether to center EMA of gradient squares using an additional EMA. Defaults to False.
        debiased (bool, optional): applies Adam debiasing. Defaults to False.
        amsgrad (bool, optional): Whether to divide by maximum of EMA of gradient squares instead. Defaults to False.
        pow (float, optional): power used in second momentum power and root. Defaults to 2.
        init (str, optional): how to initialize EMA, either "update" to use first update or "zeros". Defaults to "update".
        inner (Chainable | None, optional): Inner modules that are applied after updating EMA and before preconditioning. Defaults to None.
    """
    def __init__(
        self,
        smoothing: float = 0.99,
        eps: float = 1e-8,
        centered: bool = False,
        debiased: bool = False,
        amsgrad: bool = False,
        pow: float = 2,
        init: Literal["zeros", "update"] = "update",
        inner: Chainable | None = None,
    ):
        defaults = dict(smoothing=smoothing,eps=eps,centered=centered,debiased=debiased,amsgrad=amsgrad,pow=pow,init=init)
        super().__init__(defaults=defaults, uses_grad=False)
        self.current_step = 0
        if inner is not None:
            self.set_child('inner', inner)

    def transform(self, tensors, params, grads, vars):
        self.current_step += 1

        smoothing,eps = self.get_settings('smoothing', 'eps', params=params, cls=NumberList)
        centered,debiased,amsgrad,pow,init = itemgetter('centered','debiased','amsgrad','pow','init')(self.settings[params[0]])

        exp_avg_sq = self.get_state('exp_avg_sq', params=params, cls=TensorList)
        exp_avg = self.get_state('exp_avg', params=params, cls=TensorList) if centered else None
        max_exp_avg_sq = self.get_state('max_exp_avg_sq', params=params, cls=TensorList) if amsgrad else None

        if init == 'update' and self.current_step == 1:
            exp_avg_sq.set_([t**2 for t in tensors])
            if exp_avg is not None: exp_avg.set_([t.clone() for t in tensors])

        return rmsprop_(
            TensorList(tensors),
            exp_avg_sq_=exp_avg_sq,
            smoothing=smoothing,
            eps=eps,
            debiased=debiased,
            step=self.current_step,
            exp_avg_=exp_avg,
            max_exp_avg_sq_=max_exp_avg_sq,
            pow=pow,

            # inner args
            inner=self.children.get("inner", None),
            params=params,
            grads=grads,
            vars=vars,
        )