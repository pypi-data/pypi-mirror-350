from collections.abc import Sequence
from functools import partial
from operator import itemgetter
from typing import Literal

import torch

from ...core import Target, Transform
from ...utils import NumberList, TensorList
from ..functional import ema_, ema_sq_, sqrt_ema_sq_
from .ema import EMASquared, SqrtEMASquared
from .momentum import nag_


def precentered_ema_sq_(
    tensors: TensorList,
    exp_avg_: TensorList,
    exp_avg_sq_: TensorList,
    beta1: float | NumberList,
    beta2: float | NumberList,
    step: int,
    min_step: int,
    pow: float,
    max_exp_avg_sq_: TensorList | None,
):
    """
    Squared EMA of (update - 1st EMA). Starts taking effect after `min_step` to avoid division by epsilon.

    returns `exp_avg_sq_` or `max_exp_avg_sq_`.
    """
    exp_avg_ = ema_(tensors, exp_avg_=exp_avg_, beta=beta1, dampening=0, lerp=False)

    if step < min_step: centered_update = tensors
    else: centered_update = tensors - exp_avg_

    exp_avg_sq_=ema_sq_(
        centered_update,
        exp_avg_sq_=exp_avg_sq_,
        beta=beta2,
        pow=pow,
        max_exp_avg_sq_=max_exp_avg_sq_,
    )
    return exp_avg_sq_

class PrecenteredEMASquared(Transform):
    def __init__(self, beta1:float=0.99, beta2=0.99, min_step: int = 2, amsgrad=False, pow:float=2, target: Target = 'update'):
        defaults = dict(beta1=beta1,beta2=beta2,pow=pow,amsgrad=amsgrad, min_step=min_step)
        super().__init__(defaults, uses_grad=False, target=target)
        self.current_step = 0

    @torch.no_grad
    def transform(self, tensors, params, grads, vars):
        self.current_step += 1

        beta1, beta2 = self.get_settings('beta1','beta2', params=params, cls=NumberList)
        amsgrad, pow, min_step = itemgetter('amsgrad', 'pow', 'min_step')(self.settings[params[0]])

        if amsgrad:
            exp_avg, exp_avg_sq, max_exp_avg_sq = self.get_state('exp_avg', 'exp_avg_sq', 'max_exp_avg_sq', params=params, cls=TensorList)
        else:
            exp_avg, exp_avg_sq = self.get_state('exp_avg', 'exp_avg_sq', params=params, cls=TensorList)
            max_exp_avg_sq = None

        return precentered_ema_sq_(
            TensorList(tensors),
            exp_avg_ = exp_avg,
            exp_avg_sq_=exp_avg_sq,
            beta1=beta1,
            beta2=beta2,
            step = self.current_step,
            min_step=min_step,
            pow=pow,
            max_exp_avg_sq_=max_exp_avg_sq,
        ).clone()


def nag_ema_sq_(
    tensors: TensorList,
    exp_avg_sq_: TensorList,
    beta: float | NumberList,
    max_exp_avg_sq_: TensorList | None,
    pow: float,
    lerp:bool=True,
):
    """
    Nesterov EMA of squared tensors.

    Returns `exp_avg_sq_` or `max_exp_avg_sq_`.
    """
    if pow == 1: tensors = tensors.abs()
    elif pow%2 == 0: tensors = tensors.pow(pow)
    else: tensors = tensors.pow(pow).abs()

    exp_avg_sq_=nag_(tensors,velocity_=exp_avg_sq_,momentum=beta,dampening=0,lerp=lerp,)

    # AMSGrad
    if max_exp_avg_sq_ is not None:
        max_exp_avg_sq_.maximum_(exp_avg_sq_)
        exp_avg_sq_ = max_exp_avg_sq_

    return exp_avg_sq_

def sqrt_nag_ema_sq_(
    tensors: TensorList,
    exp_avg_sq_: TensorList,
    beta: float | NumberList,
    max_exp_avg_sq_: TensorList | None,
    debiased: bool,
    step: int,
    pow: float,
    lerp:bool=False,
):
    """
    Square root of nesterov EMA of squared tensors.

    Returns new tensors.
    """
    return sqrt_ema_sq_(tensors=tensors,exp_avg_sq_=exp_avg_sq_,beta=beta,max_exp_avg_sq_=max_exp_avg_sq_,
                        pow=pow,debiased=debiased,step=step,ema_sq_fn=partial(nag_ema_sq_,lerp=lerp))

class NesterovEMASquared(EMASquared):
    EMA_SQ_FN = staticmethod(nag_ema_sq_)

class SqrtNesterovEMASquared(SqrtEMASquared):
    SQRT_EMA_SQ_FN = staticmethod(sqrt_nag_ema_sq_)


def coordinate_momentum_(
    tensors: TensorList,
    velocity_: TensorList,
    p: float | NumberList,
):
    """
    sets `velocity_` to p% random values from `tensors`.

    Returns `velocity_`
    """
    mask = tensors.bernoulli_like(p).as_bool()
    velocity_.masked_set_(mask, tensors)
    return velocity_


class CoordinateMomentum(Transform):
    def __init__(self, p: float = 0.1, target: Target = 'update'):
        defaults = dict(p=p)
        super().__init__(defaults, uses_grad=False, target=target)

    @torch.no_grad
    def transform(self, tensors, params, grads, vars):
        p = self.get_settings('p', params=params, cls=NumberList)
        velocity = self.get_state('velocity', params=params, cls=TensorList)
        return coordinate_momentum_(TensorList(tensors), velocity_=velocity, p=p).clone()


# def multiplicative_momentum_(
#     tensors_: TensorList,
#     velocity_: TensorList,
#     momentum: float | NumberList,
#     dampening: float | NumberList,
#     normalize_velocity: bool = True,
#     abs: bool = False,
#     lerp: bool = False,
# ):
#     """
#     abs: if True, tracks momentum of absolute magnitudes.

#     returns `tensors_`.
#     """
#     tensors_into_velocity = tensors_.abs() if abs else tensors_
#     ema_(tensors_into_velocity, exp_avg_=velocity_, beta=momentum, dampening=0, lerp=lerp)

#     if normalize_velocity: velocity_ = velocity_ / velocity_.std().add_(1e-8)
#     return tensors_.mul_(velocity_.lazy_mul(1-dampening) if abs else velocity_.abs().lazy_mul_(1-dampening))


# class MultiplicativeMomentum(Transform):
#     """sucks"""
#     def __init__(self, momentum: float = 0.9, dampening: float = 0,normalize_velocity: bool = True, abs: bool = False, lerp: bool = False):
#         defaults = dict(momentum=momentum, dampening=dampening, normalize_velocity=normalize_velocity,abs=abs, lerp=lerp)
#         super().__init__(defaults, uses_grad=False)

#     @torch.no_grad
#     def transform(self, tensors, params, grads, vars):
#         momentum,dampening = self.get_settings('momentum','dampening', params=params, cls=NumberList)
#         abs,lerp,normalize_velocity = self.first_setting('abs','lerp','normalize_velocity', params=params)
#         velocity = self.get_state('velocity', params=params, cls=TensorList)
#         return multiplicative_momentum_(TensorList(target), velocity_=velocity, momentum=momentum, dampening=dampening,
#                                         normalize_velocity=normalize_velocity,abs=abs,lerp=lerp)

