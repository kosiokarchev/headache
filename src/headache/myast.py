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


def comprehension(*, target: expr, iter: expr, ifs: tp.List[expr], is_async: int) -> ast.comprehension:
    return ast.comprehension(**locals())


def arg(*, arg: identifier, annotation: tp.Optional[expr] = None,
        type_comment: string = None) -> ast.arg:
    return ast.arg(**locals())


def arguments(*, posonlyargs: tp.List[ast.arg] = empty, args: tp.List[ast.arg] = empty, vararg: tp.Optional[ast.arg] = None,
              kwonlyargs: tp.List[ast.arg] = empty, kw_defaults: tp.List[expr] = empty, kwarg: tp.Optional[ast.arg] = None,
              defaults: tp.List[expr] = empty) -> ast.arguments:
    return ast.arguments(**locals())


def keyword(*, arg: identifier = None, value: expr) -> ast.keyword:
    return ast.keyword(**locals())


def alias(*, name: identifier, asname: identifier = None) -> ast.alias:
    return ast.alias(**locals())


def withitem(*, context_expr: expr, optional_vars: tp.Optional[expr] = None) -> ast.withitem:
    return ast.withitem(**locals())


def Module(*, body: tp.List[stmt], type_ignores: tp.List[ast.type_ignore] = empty) -> ast.Module:
    return ast.Module(**locals())


def Interactive(*, body: tp.List[stmt]) -> ast.Interactive:
    return ast.Interactive(**locals())


def Expression(*, body: expr) -> ast.Expression:
    return ast.Expression(**locals())


def FunctionType(*, argtypes: tp.List[expr], returns: expr) -> ast.FunctionType:
    return ast.FunctionType(**locals())


def Suite(*, body: tp.List[stmt]) -> ast.Suite:
    return ast.Suite(**locals())


def FunctionDef(*, name: identifier, args: ast.arguments, body: tp.List[stmt], decorator_list: tp.List[expr] = empty,
                returns: tp.Optional[expr] = None, type_comment: string = None) -> ast.FunctionDef:
    return ast.FunctionDef(**locals())


def AsyncFunctionDef(*, name: identifier, args: ast.arguments, body: tp.List[stmt],
                     decorator_list: tp.List[expr], returns: tp.Optional[expr] = None,
                     type_comment: string = None) -> ast.AsyncFunctionDef:
    return ast.AsyncFunctionDef(**locals())


def ClassDef(*, name: identifier, body: tp.List[stmt], bases: tp.List[expr] = empty,
             keywords: tp.List[ast.keyword] = empty, decorator_list: tp.List[expr] = empty) -> ast.ClassDef:
    return ast.ClassDef(**locals())


def Return(*, value: tp.Optional[expr] = None) -> ast.Return:
    return ast.Return(**locals())


def Delete(*, targets: tp.List[expr]) -> ast.Delete:
    return ast.Delete(**locals())


def Assign(*, targets: tp.List[expr], value: expr, type_comment: string = None) -> ast.Assign:
    return ast.Assign(**locals())


def AugAssign(*, target: expr, op: ast.operator, value: expr) -> ast.AugAssign:
    return ast.AugAssign(**locals())


def AnnAssign(*, target: expr, annotation: expr, value: tp.Optional[expr] = None, simple: int = 1) -> ast.AnnAssign:
    return ast.AnnAssign(**locals())


def For(*, target: expr, iter: expr, body: tp.List[stmt], orelse: tp.List[stmt],
        type_comment: string = None) -> ast.For:
    return ast.For(**locals())


def AsyncFor(*, target: expr, iter: expr, body: tp.List[stmt], orelse: tp.List[stmt],
             type_comment: string = None) -> ast.AsyncFor:
    return ast.AsyncFor(**locals())


def While(*, test: expr, body: tp.List[stmt], orelse: tp.List[stmt]) -> ast.While:
    return ast.While(**locals())


def If(*, test: expr, body: tp.List[stmt], orelse: tp.List[stmt]) -> ast.If:
    return ast.If(**locals())


def With(*, items: tp.List[ast.withitem], body: tp.List[stmt], type_comment: string = None) -> ast.With:
    return ast.With(**locals())


def AsyncWith(*, items: tp.List[ast.withitem], body: tp.List[stmt], type_comment: string = None) -> ast.AsyncWith:
    return ast.AsyncWith(**locals())


def Raise(*, exc: tp.Optional[expr] = None, cause: tp.Optional[expr] = None) -> ast.Raise:
    return ast.Raise(**locals())


def Try(*, body: tp.List[stmt], handlers: tp.List[ast.excepthandler], orelse: tp.List[stmt],
        finalbody: tp.List[stmt]) -> ast.Try:
    return ast.Try(**locals())


def Assert(*, test: expr, msg: tp.Optional[expr] = None) -> ast.Assert:
    return ast.Assert(**locals())


def Import(*, names: tp.List[ast.alias]) -> ast.Import:
    return ast.Import(**locals())


def ImportFrom(*, module: identifier = None, names: tp.List[ast.alias], level: int = 0) -> ast.ImportFrom:
    return ast.ImportFrom(**locals())


def Global(*, names: tp.List[identifier]) -> ast.Global:
    return ast.Global(**locals())


def Nonlocal(*, names: tp.List[identifier]) -> ast.Nonlocal:
    return ast.Nonlocal(**locals())


def Expr(*, value: expr) -> ast.Expr:
    return ast.Expr(**locals())


def BoolOp(*, op: ast.boolop, values: tp.List[expr]) -> ast.BoolOp:
    return ast.BoolOp(**locals())


def NamedExpr(*, target: expr, value: expr) -> ast.NamedExpr:
    return ast.NamedExpr(**locals())


def BinOp(*, left: expr, op: ast.operator, right: expr) -> ast.BinOp:
    return ast.BinOp(**locals())


def UnaryOp(*, op: ast.unaryop, operand: expr) -> ast.UnaryOp:
    return ast.UnaryOp(**locals())


def Lambda(*, args: ast.arguments, body: expr) -> ast.Lambda:
    return ast.Lambda(**locals())


def IfExp(*, test: expr, body: expr, orelse: expr) -> ast.IfExp:
    return ast.IfExp(**locals())


def Dict(*, keys: tp.List[expr], values: tp.List[expr]) -> ast.Dict:
    return ast.Dict(**locals())


def Set(*, elts: tp.List[expr]) -> ast.Set:
    return ast.Set(**locals())


def ListComp(*, elt: expr, generators: tp.List[ast.comprehension]) -> ast.ListComp:
    return ast.ListComp(**locals())


def SetComp(*, elt: expr, generators: tp.List[ast.comprehension]) -> ast.SetComp:
    return ast.SetComp(**locals())


def DictComp(*, key: expr, value: expr, generators: tp.List[ast.comprehension]) -> ast.DictComp:
    return ast.DictComp(**locals())


def GeneratorExp(*, elt: expr, generators: tp.List[ast.comprehension]) -> ast.GeneratorExp:
    return ast.GeneratorExp(**locals())


def Await(*, value: expr) -> ast.Await:
    return ast.Await(**locals())


def Yield(*, value: tp.Optional[expr] = None) -> ast.Yield:
    return ast.Yield(**locals())


def YieldFrom(*, value: expr) -> ast.YieldFrom:
    return ast.YieldFrom(**locals())


def Compare(*, left: expr, ops: tp.List[ast.cmpop], comparators: tp.List[expr]) -> ast.Compare:
    return ast.Compare(**locals())


def Call(*, func: expr, args: tp.List[expr] = empty, keywords: tp.List[ast.keyword] = empty) -> ast.Call:
    return ast.Call(**locals())


def FormattedValue(*, value: expr, conversion: int = None,
                   format_spec: tp.Optional[expr] = None) -> ast.FormattedValue:
    return ast.FormattedValue(**locals())


def JoinedStr(*, values: tp.List[expr]) -> ast.JoinedStr:
    return ast.JoinedStr(**locals())


def Constant(*, value: constant, kind: string = None) -> ast.Constant:
    return ast.Constant(**locals())


def Attribute(*, value: expr, attr: identifier, ctx: expr_context) -> ast.Attribute:
    return ast.Attribute(**locals())


def Subscript(*, value: expr, slice: slice, ctx: expr_context) -> ast.Subscript:
    return ast.Subscript(**locals())


def Starred(*, value: expr, ctx: expr_context) -> ast.Starred:
    return ast.Starred(**locals())


def Name(*, id: identifier, ctx: expr_context) -> ast.Name:
    return ast.Name(**locals())


def List(*, elts: tp.List[expr], ctx: expr_context = Load()) -> ast.List:
    return ast.List(**locals())


def Tuple(*, elts: tp.List[expr], ctx: expr_context = Load()) -> ast.Tuple:
    return ast.Tuple(**locals())


def Slice(*, lower: tp.Optional[expr] = None, upper: tp.Optional[expr] = None,
          step: tp.Optional[expr] = None) -> ast.Slice:
    return ast.Slice(**locals())


def ExtSlice(*, dims: tp.List[slice]) -> ast.ExtSlice:
    return ast.ExtSlice(**locals())


def Index(*, value: expr) -> ast.Index:
    return ast.Index(**locals())


def ExceptHandler(*, type: tp.Optional[expr] = None, name: identifier = None,
                  body: tp.List[stmt]) -> ast.ExceptHandler:
    return ast.ExceptHandler(**locals())


def TypeIgnore(*, lineno: int, tag: string) -> ast.TypeIgnore:
    return ast.TypeIgnore(**locals())


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


def lvalue(name: str) -> Name:
    return dotted_name(name, Store())


def rvalue(name: str) -> Name:
    return dotted_name(name, Load())


def assign(name: str, value: expr, type_comment: str = None):
    return Assign(targets=[lvalue(name)], value=value, type_comment=type_comment)


def call(funcname: str, args: tp.List[expr]) -> Call:
    return Call(func=rvalue(funcname), args=args)
