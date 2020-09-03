import _ctypes
import ctypes as ct
import inspect
import typing as tp

from .utils import dictunion


CType = tp.NewType('CType', tp.Any)
CPointerType = _ctypes._Pointer
CArrayType = _ctypes.Array
CFuncType = _ctypes.CFuncPtr


class CTSignature(inspect.Signature):
    @property
    def _as_parameter_(self):
        return ct.CFUNCTYPE(self.return_annotation,
                            *(arg.annotation for arg in self.parameters.values()))

    # Public accessor
    @property
    def as_parameter(self):
        return self._as_parameter_

    @classmethod
    def make(cls, argnames: tp.Sequence[str], argtypes: tp.Sequence[CType], rettype: CType):
        return cls(
            parameters=[
                inspect.Parameter(name=argname, kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=argtype)
                for argname, argtype in zip(argnames, argtypes)
            ],
            return_annotation=rettype
        )


class c_enum_meta(type(ct.c_uint)):
    def __new__(cls, name, bases, __dict__):
        if name != 'c_enum':
            __dict__['__members'] = {}
            __dict__['__members_inv'] = {}
            for key, val in __dict__.items():
                if not (any(key in base.__dict__ for base in bases) or key.startswith('__')):
                    __dict__['__members'][key] = val
                    __dict__['__members_inv'][val] = key
        return super().__new__(cls, name, bases, __dict__)

    @property
    def _members(cls) -> tp.Mapping[str, int]:
        return dictunion(getattr(cls, '__members', {}) for cls in cls.__mro__)

    @property
    def _members_inv(cls) -> tp.Mapping[int, str]:
        return dictunion(getattr(cls, '__members_inv', {}) for cls in cls.__mro__)


class c_enum(ct.c_uint, metaclass=c_enum_meta):
    _members: tp.Mapping[str, int]
    _members_inv: tp.Mapping[int, str]

    def __init__(self, value=None):
        if value is not None:
            try:
                self.name = self._members_inv[value]
            except KeyError:
                raise ValueError(f'{self.__class__.__name__} does not have a member with value {value}')
        else:
            value = 0

        super().__init__(value)

    @classmethod
    def from_param(cls, param):
        if isinstance(param, c_enum):
            if param.__class__ != cls:
                raise ValueError(f'Enumeration {param.__class__.__name__} passed as {cls.__name__}')
            else:
                return param
        else:
            return cls(param)

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.__class__._members_inv.get(self.value, "UNDEFINED")} (= {self.value})'
