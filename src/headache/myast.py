import ast
import typing as tp

# noinspection PyUnresolvedReferences
from ast import mod, expr, stmt, expr_context, slice
# noinspection PyUnresolvedReferences
from ast import (Add, And, AugLoad, AugStore, BitAnd, BitOr, BitXor, Del, Div, Eq, FloorDiv, Gt, GtE, In, Invert, Is,
                 IsNot, LShift, Load, Lt, LtE, MatMult, Mod, Mult, Not, NotEq, NotIn, Or, Param, Pow, RShift, Store,
                 Sub, UAdd, USub, Pass, Break, Continue)

from frozenlist import FrozenList
from more_itertools import last

empty = FrozenList()
empty.freeze()

identifier = str
string = str
constant = tp.Any


class Rehashable(type):
    def __hash__(self):
        return hash(self.__bases__[0])

    def __eq__(self, other):
        return other is self.__bases__[0] or super().__eq__(other)


class comprehension(ast.comprehension, metaclass=Rehashable):
    target: expr
    iter: expr
    ifs: tp.List[expr]
    is_async: int

    def __init__(self, *, target: expr, iter: expr, ifs: tp.List[expr], is_async: int):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class arg(ast.arg, metaclass=Rehashable):
    arg: identifier
    annotation: tp.Optional[expr]
    type_comment: string = None

    def __init__(self, *, arg: identifier, annotation: tp.Optional[expr] = None,
                 type_comment: string = None):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class arguments(ast.arguments, metaclass=Rehashable):
    posonlyargs: tp.List[ast.arg]
    args: tp.List[ast.arg]
    vararg: tp.Optional[ast.arg]
    kwonlyargs: tp.List[ast.arg]
    kw_defaults: tp.List[expr]
    kwarg: tp.Optional[ast.arg]
    defaults: tp.List[expr] = empty

    def __init__(self, *, posonlyargs: tp.List[ast.arg] = empty, args: tp.List[ast.arg] = empty,
                 vararg: tp.Optional[ast.arg] = None,
                 kwonlyargs: tp.List[ast.arg] = empty, kw_defaults: tp.List[expr] = empty,
                 kwarg: tp.Optional[ast.arg] = None,
                 defaults: tp.List[expr] = empty):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class keyword(ast.keyword, metaclass=Rehashable):
    arg: identifier
    value: expr

    def __init__(self, *, arg: identifier = None, value: expr):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class alias(ast.alias, metaclass=Rehashable):
    name: identifier
    asname: identifier = None

    def __init__(self, *, name: identifier, asname: identifier = None):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class withitem(ast.withitem, metaclass=Rehashable):
    context_expr: expr
    optional_vars: tp.Optional[expr] = None

    def __init__(self, *, context_expr: expr, optional_vars: tp.Optional[expr] = None):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class Module(ast.Module, metaclass=Rehashable):
    body: tp.List[stmt]
    type_ignores: tp.List[ast.type_ignore] = empty

    def __init__(self, *, body: tp.List[stmt], type_ignores: tp.List[ast.type_ignore] = empty):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class Interactive(ast.Interactive, metaclass=Rehashable):
    body: tp.List[stmt]

    def __init__(self, *, body: tp.List[stmt]):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class Expression(ast.Expression, metaclass=Rehashable):
    body: expr

    def __init__(self, *, body: expr):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class FunctionType(ast.FunctionType, metaclass=Rehashable):
    argtypes: tp.List[expr]
    returns: expr

    def __init__(self, *, argtypes: tp.List[expr], returns: expr):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class Suite(ast.Suite, metaclass=Rehashable):
    body: tp.List[stmt]

    def __init__(self, *, body: tp.List[stmt]):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class FunctionDef(ast.FunctionDef, metaclass=Rehashable):
    name: identifier
    args: ast.arguments
    body: tp.List[stmt]
    decorator_list: tp.List[expr]
    returns: tp.Optional[expr]
    type_comment: string = None

    def __init__(self, *, name: identifier, args: ast.arguments, body: tp.List[stmt],
                 decorator_list: tp.List[expr] = empty, returns: tp.Optional[expr] = None, type_comment: string = None):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class AsyncFunctionDef(ast.AsyncFunctionDef, metaclass=Rehashable):
    name: identifier
    args: ast.arguments
    body: tp.List[stmt]
    decorator_list: tp.List[expr]
    returns: tp.Optional[expr]
    type_comment: string = None

    def __init__(self, *, name: identifier, args: ast.arguments, body: tp.List[stmt],
                 decorator_list: tp.List[expr], returns: tp.Optional[expr] = None,
                 type_comment: string = None):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class ClassDef(ast.ClassDef, metaclass=Rehashable):
    name: identifier
    body: tp.List[stmt]
    bases: tp.List[expr]
    keywords: tp.List[ast.keyword]
    decorator_list: tp.List[expr] = empty

    def __init__(self, *, name: identifier, body: tp.List[stmt], bases: tp.List[expr] = empty,
                 keywords: tp.List[ast.keyword] = empty, decorator_list: tp.List[expr] = empty):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class Return(ast.Return, metaclass=Rehashable):
    value: tp.Optional[expr] = None

    def __init__(self, *, value: tp.Optional[expr] = None):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class Delete(ast.Delete, metaclass=Rehashable):
    targets: tp.List[expr]

    def __init__(self, *, targets: tp.List[expr]):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class Assign(ast.Assign, metaclass=Rehashable):
    targets: tp.List[expr]
    value: expr
    type_comment: string = None

    def __init__(self, *, targets: tp.List[expr], value: expr, type_comment: string = None):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class AugAssign(ast.AugAssign, metaclass=Rehashable):
    target: expr
    op: ast.operator
    value: expr

    def __init__(self, *, target: expr, op: ast.operator, value: expr):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class AnnAssign(ast.AnnAssign, metaclass=Rehashable):
    target: expr
    annotation: expr
    value: tp.Optional[expr]
    simple: int = 1

    def __init__(self, *, target: expr, annotation: expr, value: tp.Optional[expr] = None, simple: int = 1):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class For(ast.For, metaclass=Rehashable):
    target: expr
    iter: expr
    body: tp.List[stmt]
    orelse: tp.List[stmt]
    type_comment: string = None

    def __init__(self, *, target: expr, iter: expr, body: tp.List[stmt], orelse: tp.List[stmt],
                 type_comment: string = None):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class AsyncFor(ast.AsyncFor, metaclass=Rehashable):
    target: expr
    iter: expr
    body: tp.List[stmt]
    orelse: tp.List[stmt]
    type_comment: string = None

    def __init__(self, *, target: expr, iter: expr, body: tp.List[stmt], orelse: tp.List[stmt],
                 type_comment: string = None):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class While(ast.While, metaclass=Rehashable):
    test: expr
    body: tp.List[stmt]
    orelse: tp.List[stmt]

    def __init__(self, *, test: expr, body: tp.List[stmt], orelse: tp.List[stmt]):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class If(ast.If, metaclass=Rehashable):
    test: expr
    body: tp.List[stmt]
    orelse: tp.List[stmt]

    def __init__(self, *, test: expr, body: tp.List[stmt], orelse: tp.List[stmt]):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class With(ast.With, metaclass=Rehashable):
    items: tp.List[ast.withitem]
    body: tp.List[stmt]
    type_comment: string = None

    def __init__(self, *, items: tp.List[ast.withitem], body: tp.List[stmt], type_comment: string = None):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class AsyncWith(ast.AsyncWith, metaclass=Rehashable):
    items: tp.List[ast.withitem]
    body: tp.List[stmt]
    type_comment: string = None

    def __init__(self, *, items: tp.List[ast.withitem], body: tp.List[stmt], type_comment: string = None):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class Raise(ast.Raise, metaclass=Rehashable):
    exc: tp.Optional[expr]
    cause: tp.Optional[expr] = None

    def __init__(self, *, exc: tp.Optional[expr] = None, cause: tp.Optional[expr] = None):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class Try(ast.Try, metaclass=Rehashable):
    body: tp.List[stmt]
    handlers: tp.List[ast.excepthandler]
    orelse: tp.List[stmt]
    finalbody: tp.List[stmt]

    def __init__(self, *, body: tp.List[stmt], handlers: tp.List[ast.excepthandler], orelse: tp.List[stmt],
                 finalbody: tp.List[stmt]):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class Assert(ast.Assert, metaclass=Rehashable):
    test: expr
    msg: tp.Optional[expr] = None

    def __init__(self, *, test: expr, msg: tp.Optional[expr] = None):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class Import(ast.Import, metaclass=Rehashable):
    names: tp.List[ast.alias]

    def __init__(self, *, names: tp.List[ast.alias]):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class ImportFrom(ast.ImportFrom, metaclass=Rehashable):
    module: identifier
    names: tp.List[ast.alias]
    level: int = 0

    def __init__(self, *, module: identifier = None, names: tp.List[ast.alias], level: int = 0):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class Global(ast.Global, metaclass=Rehashable):
    names: tp.List[identifier]

    def __init__(self, *, names: tp.List[identifier]):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class Nonlocal(ast.Nonlocal, metaclass=Rehashable):
    names: tp.List[identifier]

    def __init__(self, *, names: tp.List[identifier]):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class Expr(ast.Expr, metaclass=Rehashable):
    value: expr

    def __init__(self, *, value: expr):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class BoolOp(ast.BoolOp, metaclass=Rehashable):
    op: ast.boolop
    values: tp.List[expr]

    def __init__(self, *, op: ast.boolop, values: tp.List[expr]):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class NamedExpr(ast.NamedExpr, metaclass=Rehashable):
    target: expr
    value: expr

    def __init__(self, *, target: expr, value: expr):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class BinOp(ast.BinOp, metaclass=Rehashable):
    left: expr
    op: ast.operator
    right: expr

    def __init__(self, *, left: expr, op: ast.operator, right: expr):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class UnaryOp(ast.UnaryOp, metaclass=Rehashable):
    op: ast.unaryop
    operand: expr

    def __init__(self, *, op: ast.unaryop, operand: expr):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class Lambda(ast.Lambda, metaclass=Rehashable):
    args: ast.arguments
    body: expr

    def __init__(self, *, args: ast.arguments, body: expr):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class IfExp(ast.IfExp, metaclass=Rehashable):
    test: expr
    body: expr
    orelse: expr

    def __init__(self, *, test: expr, body: expr, orelse: expr):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class Dict(ast.Dict, metaclass=Rehashable):
    keys: tp.List[expr]
    values: tp.List[expr]

    def __init__(self, *, keys: tp.List[expr], values: tp.List[expr]):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class Set(ast.Set, metaclass=Rehashable):
    elts: tp.List[expr]

    def __init__(self, *, elts: tp.List[expr]):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class ListComp(ast.ListComp, metaclass=Rehashable):
    elt: expr
    generators: tp.List[ast.comprehension]

    def __init__(self, *, elt: expr, generators: tp.List[ast.comprehension]):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class SetComp(ast.SetComp, metaclass=Rehashable):
    elt: expr
    generators: tp.List[ast.comprehension]

    def __init__(self, *, elt: expr, generators: tp.List[ast.comprehension]):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class DictComp(ast.DictComp, metaclass=Rehashable):
    key: expr
    value: expr
    generators: tp.List[ast.comprehension]

    def __init__(self, *, key: expr, value: expr, generators: tp.List[ast.comprehension]):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class GeneratorExp(ast.GeneratorExp, metaclass=Rehashable):
    elt: expr
    generators: tp.List[ast.comprehension]

    def __init__(self, *, elt: expr, generators: tp.List[ast.comprehension]):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class Await(ast.Await, metaclass=Rehashable):
    value: expr

    def __init__(self, *, value: expr):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class Yield(ast.Yield, metaclass=Rehashable):
    value: tp.Optional[expr] = None

    def __init__(self, *, value: tp.Optional[expr] = None):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class YieldFrom(ast.YieldFrom, metaclass=Rehashable):
    value: expr

    def __init__(self, *, value: expr):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class Compare(ast.Compare, metaclass=Rehashable):
    left: expr
    ops: tp.List[ast.cmpop]
    comparators: tp.List[expr]

    def __init__(self, *, left: expr, ops: tp.List[ast.cmpop], comparators: tp.List[expr]):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class Call(ast.Call, metaclass=Rehashable):
    func: expr
    args: tp.List[expr]
    keywords: tp.List[ast.keyword] = empty

    def __init__(self, *, func: expr, args: tp.List[expr] = empty, keywords: tp.List[ast.keyword] = empty):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class FormattedValue(ast.FormattedValue, metaclass=Rehashable):
    value: expr
    conversion: int
    format_spec: tp.Optional[expr] = None

    def __init__(self, *, value: expr, conversion: int = None,
                 format_spec: tp.Optional[expr] = None):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class JoinedStr(ast.JoinedStr, metaclass=Rehashable):
    values: tp.List[expr]

    def __init__(self, *, values: tp.List[expr]):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class Constant(ast.Constant, metaclass=Rehashable):
    value: constant
    kind: string = None

    def __init__(self, *, value: constant, kind: string = None):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class Attribute(ast.Attribute, metaclass=Rehashable):
    value: expr
    attr: identifier
    ctx: expr_context

    def __init__(self, *, value: expr, attr: identifier, ctx: expr_context):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class Subscript(ast.Subscript, metaclass=Rehashable):
    value: expr
    slice: slice
    ctx: expr_context

    def __init__(self, *, value: expr, slice: slice, ctx: expr_context):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class Starred(ast.Starred, metaclass=Rehashable):
    value: expr
    ctx: expr_context

    def __init__(self, *, value: expr, ctx: expr_context):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class Name(ast.Name, metaclass=Rehashable):
    id: identifier
    ctx: expr_context

    def __init__(self, *, id: identifier, ctx: expr_context):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class List(ast.List, metaclass=Rehashable):
    elts: tp.List[expr]
    ctx: expr_context = Load()

    def __init__(self, *, elts: tp.List[expr], ctx: expr_context = Load()):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class Tuple(ast.Tuple, metaclass=Rehashable):
    elts: tp.List[expr]
    ctx: expr_context = Load()

    def __init__(self, *, elts: tp.List[expr], ctx: expr_context = Load()):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class Slice(ast.Slice, metaclass=Rehashable):
    lower: tp.Optional[expr]
    upper: tp.Optional[expr]
    step: tp.Optional[expr] = None

    def __init__(self, *, lower: tp.Optional[expr] = None, upper: tp.Optional[expr] = None,
                 step: tp.Optional[expr] = None):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class ExtSlice(ast.ExtSlice, metaclass=Rehashable):
    dims: tp.List[slice]

    def __init__(self, *, dims: tp.List[slice]):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class Index(ast.Index, metaclass=Rehashable):
    value: expr

    def __init__(self, *, value: expr):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class ExceptHandler(ast.ExceptHandler, metaclass=Rehashable):
    type: tp.Optional[expr]
    name: identifier
    body: tp.List[stmt]

    def __init__(self, *, type: tp.Optional[expr] = None, name: identifier = None,
                 body: tp.List[stmt]):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


class TypeIgnore(ast.TypeIgnore, metaclass=Rehashable):
    lineno: int
    tag: string

    def __init__(self, *, lineno: int, tag: string):
        super().__init__(**{key: value for key, value in locals().items() if key not in ('self', '__class__')})


_compile = compile


def compile(tree, mode=None, *args, **kwargs):
    return _compile(ast.fix_missing_locations(tree), '_file',
                    mode
                    or isinstance(tree, ast.Module) and 'exec'
                    or isinstance(tree, ast.Expression) and 'eval'
                    or 'single',
                    *args, **kwargs)


def dotted_name(name: str, ctx: expr_context) -> expr:
    res = last(res for res in [None] for p in name.split('.') for res in [
        Name(id=p, ctx=Load()) if res is None else Attribute(value=res, attr=p, ctx=Load())
    ])
    res.ctx = ctx
    return res


def lvalue(name: str) -> expr:
    return dotted_name(name, Store())


def rvalue(name: str) -> expr:
    return dotted_name(name, Load())


def assign(name: str, value: expr, type_comment: str = None):
    return Assign(targets=[lvalue(name)], value=value, type_comment=type_comment)


def call(funcname: str, args: tp.List[expr]) -> Call:
    return Call(func=rvalue(funcname), args=args)
