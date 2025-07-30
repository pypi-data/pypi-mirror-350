import functools
import operator
from typing import Any, TypeVar
from collections.abc import Iterable, Callable
from collections import UserDict


def _flatten_no_check(iterable: Iterable) -> list[Any]:
    """Flatten an iterable of iterables, returns a flattened list. Note that if `iterable` is not Iterable, this will return `[iterable]`."""
    if isinstance(iterable, Iterable) and not isinstance(iterable, str):
        return [a for i in iterable for a in _flatten_no_check(i)]
    return [iterable]

def flatten(iterable: Iterable) -> list[Any]:
    """Flatten an iterable of iterables, returns a flattened list. If `iterable` is not iterable, raises a TypeError."""
    if isinstance(iterable, Iterable): return [a for i in iterable for a in _flatten_no_check(i)]
    raise TypeError(f'passed object is not an iterable, {type(iterable) = }')

X = TypeVar("X")
# def reduce_dim[X](x:Iterable[Iterable[X]]) -> list[X]: # pylint:disable=E0602
def reduce_dim(x:Iterable[Iterable[X]]) -> list[X]: # pylint:disable=E0602
    """Reduces one level of nesting. Takes an iterable of iterables of X, and returns an iterable of X."""
    return functools.reduce(operator.iconcat, x, [])

def generic_eq(x: int | float | Iterable[int | float], y: int | float | Iterable[int | float]) -> bool:
    """generic equals function that supports scalars and lists of numbers"""
    if isinstance(x, (int,float)):
        if isinstance(y, (int,float)): return x==y
        return all(i==x for i in y)
    if isinstance(y, (int,float)):
        return all(i==y for i in x)
    return all(i==j for i,j in zip(x,y))

def zipmap(self, fn: Callable, other: Any | list | tuple, *args, **kwargs):
    """If `other` is list/tuple, applies `fn` to self zipped with `other`.
    Otherwise applies `fn` to this sequence and `other`.
    Returns a new sequence with return values of the callable."""
    if isinstance(other, (list, tuple)): return self.__class__(fn(i, j, *args, **kwargs) for i, j in zip(self, other))
    return self.__class__(fn(i, other, *args, **kwargs) for i in self)

