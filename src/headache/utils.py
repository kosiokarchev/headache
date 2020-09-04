import typing as tp
from contextlib import contextmanager
from functools import partial
from itertools import chain, islice

from more_itertools import first, last, unzip as _unzip


def unzip(iterable: tp.Iterable, size: int = None):
    """unzip into `size` empty iterables if `iterable` is empty """
    return (_unzip(iterable) if size is None else
            (islice(a, 1, None) for a in unzip(chain(((None,)*size,), iterable))))


def update_dict(other, self):
    self.update(other)
    return self


def dictunion(dicts: tp.Iterable[tp.Dict]):
    return last(map(partial(update_dict, self={}), dicts)) or {}


def tryone(func: tp.Callable) -> tp.Tuple[tp.Optional[Exception], tp.Optional[tp.Any]]:
    try:
        return None, func()
    except Exception as e:
        return e, None


def tryall(*funcs: tp.Callable):
    return first((ret[1] for f in funcs for ret in [tryone(f)] if ret[0] is None))


def iterrepr(iterable: tp.Iterable[str], noparen=False):
    iterable = list(iterable)
    irep = ', '.join(iterable)
    return irep if noparen else f'({irep}{"," if len(iterable) == 1 else ""})'


class AllTrialsFailedError(Exception):
    pass


@contextmanager
def patch(var, prop_or_index, value, str_is_index=False):
    byprop = isinstance(prop_or_index, str) and not str_is_index
    getter = getattr(var, byprop and '__getattribute__' or '__getitem__')
    setter = getattr(var, byprop and '__setattr__' or '__setitem__')

    cache = getter(prop_or_index)
    setter(prop_or_index, value)
    try:
        yield
    finally:
        setter(prop_or_index, cache)
