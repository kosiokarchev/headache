import ctypes as ct
import inspect
import os
import re
import subprocess
import textwrap
import typing as tp
from itertools import chain, repeat

import pygccxml
from astor import to_source, source_repr
from frozendict import frozendict
from more_itertools import lstrip
from pygccxml import declarations as d

from . import cutils, myast as ast
from .cutils import c_enum, CArrayType, CFuncType, CPointerType, CTSignature, CType
from .doxml import DoXML
from .utils import patch, tryall, unzip

_ctftypes = {key: val for key, val in ct.__dict__.items() if key.startswith('c_')}


class CTyper:
    fundamental_typemap: tp.Dict[tp.Union[d.type_t, d.class_t], CType] = {
        pgxtype: getattr(ct, key, None)
        for key, pgxtype in d.FUNDAMENTAL_TYPES.items()
        if not (key.startswith('j') or key.startswith('__'))
        for key in ['c_' + ('u' if 'unsigned' in key else '')
                    + (key.replace('unsigned ', '').replace('signed ', '')
                          .replace('long int', 'long').replace('long ', 'long').replace('short int', 'short')
                          .replace('_t', ''))]
        if key == 'c_void' or key in _ctftypes
    }
    fundamental_typemap[d.FUNDAMENTAL_TYPES['unsigned char']] = ct.c_ubyte

    def __init__(self):
        self.defines: tp.Dict[str, tp.Any] = {}
        self.typemap = self.fundamental_typemap.copy()
        self.functions: tp.Dict[str, inspect.Signature] = {}

        self._createed_types = {}

    compiler_path = 'C:/Program Files (x86)/Microsoft Visual Studio/2019/BuildTools/VC/Tools/MSVC/14.27.29110/bin/Hostx86/x86/cl.exe'

    def load_header(self, fname: str, compiler_path: str = None):
        generator_path, generator_name = pygccxml.utils.find_xml_generator()

        xml_generator_config = pygccxml.parser.xml_generator_configuration_t(
            xml_generator_path=generator_path,
            xml_generator=generator_name,
            compiler_path=compiler_path if compiler_path is not None else self.compiler_path
        )

        ns = pygccxml.parser.parse([fname], config=xml_generator_config)[0]
        self.process_namespace(ns)
        self.process_defines(fname)
        return ns

    @staticmethod
    def process_define(expr: str, defines: tp.Dict[str, tp.Any] = frozendict()) -> tp.Optional[tp.Any]:
        if expr != '':
            return tryall(*(lambda: eval(_expr, defines)
                            for _expr in (expr, re.sub(r'([\d.+\-x]*)[fFdDlLuU]*', '\\1', expr))))

    def process_defines(self, fname: str):
        undefined = {}
        newdefs = True

        for defs in chain(
            (((match.group(1), match.group(2))
              for match in re.finditer(
                r'^#define\s+([^\s]*)(?: |)([^\r\n]*)[\s\r\n]*$',
                subprocess.run(
                    ['castxml', '-E', '-dM', '-Wno-everything', fname], stdout=subprocess.PIPE
                ).stdout.decode(),
                re.MULTILINE
            )),),
            repeat(undefined.items())
        ):
            if not defs or not newdefs:
                break
            newdefs = False
            for name, expr in defs:
                try:
                    self.defines[name] = self.process_define(expr, self.defines)
                    undefined.pop(name, None)
                    newdefs = True
                except ValueError:
                    undefined[name] = expr
                    continue

        self.defines.pop('__builtins__', None)


    def get_type(self, pgxtype: d.type_t) -> CType:
        if isinstance(pgxtype, d.pointer_t):
            return ct.POINTER(self.get_type(pgxtype.base))

        elif isinstance(pgxtype, d.array_t):
            return self.get_type(pgxtype.base) * pgxtype.size

        elif isinstance(pgxtype, d.free_function_type_t):
            return CTSignature.make(
                *unzip(((f'_{i}', self.get_type(argpgxtype))
                        for i, argpgxtype in enumerate(pgxtype.arguments_types)), 2),
                self.get_type(pgxtype.return_type)
            ).as_parameter
        else:
            try:
                return self.typemap[d.remove_cv(pgxtype)]
            except KeyError as e:
                if isinstance(pgxtype, d.declarated_t):
                    return self.process_declaration(pgxtype.declaration)
                else:
                    raise e

    def _in_dict(self, key, value, dct=None):
        if dct is None:
            dct = self.typemap
        dct[key] = value
        return dct[key]

    def process_typedef(self, tdef: d.typedef_t) -> CType:
        if isinstance(tdef.decl_type, d.declarated_t) and tdef.decl_type.declaration.name == tdef.name:
            return self.typemap[tdef.decl_type.declaration]

        ctype = self.get_type(tdef.decl_type)
        return self._in_dict(d.declarated_t(tdef), (
            (ctype if issubclass(ctype, CFuncType) else type(tdef.name, (ctype,), {}))
            if isinstance(ctype, type) else ctype
        ))

    def process_variable(self, var: d.variable_t) -> tp.Tuple[str, CType]:
        return var.name, self.get_type(var.decl_type)

    def process_classdef(self, cdef: d.class_declaration_t) -> CType:
        return self.process_class(d.class_t(name=cdef.name, class_type=d.CLASS_TYPES.STRUCT))

    def process_class(self, cls: d.class_t) -> CType:
        return self._in_dict(cls, type(cls.name, (ct.Structure,),
                                       dict(_fields_=[self.process_variable(var)
                                                      for var in cls.variables(allow_empty=True)])))

    def process_enum(self, enum: d.enumeration_t) -> CType:
        return self._in_dict(enum, type(enum.name, (c_enum,), dict(enum.values)))

    def process_function(self, func: d.free_function_t) -> inspect.Signature:
        return self._in_dict(func.name, CTSignature.make(
            *unzip(((arg.name, self.get_type(arg.decl_type)) for arg in func.required_args), 2),
            self.get_type(func.return_type)
        ), self.functions)

    def process_declaration(self, decl: d.declaration_t) -> tp.Union[CType, inspect.Signature]:
        if isinstance(decl, d.typedef_t):
            return self.process_typedef(decl)
        elif isinstance(decl, d.class_declaration_t):
            return self.process_classdef(decl)
        elif isinstance(decl, d.class_t):
            return self.process_class(decl)
        elif isinstance(decl, d.enumeration_t):
            return self.process_enum(decl)
        elif isinstance(decl, d.free_function_t):
            return self.process_function(decl)
        else:
            raise ValueError('Unrecognised type.')

    def process_namespace(self, ns: d.namespace_t):
        for decl in ns.declarations:
            if not decl.location.file_name == '<builtin>' and not decl.is_artificial:
                self.process_declaration(decl)


class DLLWrapper:
    def __init__(self, headername: str, typer: CTyper = CTyper(), doxml_base=None):
        self.headername = headername
        self.typer = typer
        self.ns = self.typer.load_header(headername)

        self.doxml = doxml_base and DoXML(doxml_base)
        self.textwidth = 80
        self.tabwidth = 4

    _createed_types: tp.Dict[CType, str] = {}

    def format_docstring(self, docstring):
        return (
            '\n'
            + textwrap.indent('\n\n'.join(textwrap.fill(line, self.textwidth - self.tabwidth - 1)
                                          for line in docstring.replace('\r', '').split('\n')),
                              ' ' * self.tabwidth)
            + '\n' + ' ' * self.tabwidth
        )

    @staticmethod
    def get_typename(typ):
        return f'{typ.__module__}.{typ.__qualname__}'.replace(f'{__name__}.', '').replace('builtins.', '')

    def create_typename(self, typ) -> ast.expr:
        if typ in self._createed_types:
            return ast.rvalue(self._createed_types[typ])
        else:
            if issubclass(typ, CFuncType):
                return ast.call('ctypes.CFUNCTYPE',
                                list(map(self.create_typename, chain((typ._restype_,), typ._argtypes_))))
            elif issubclass(typ, CPointerType):
                return ast.call('ctypes.POINTER', [self.create_typename(typ._type_)])
            elif issubclass(typ, CArrayType):
                return ast.BinOp(left=ast.Constant(value=typ._length_),
                                 op=ast.Mult(),
                                 right=self.create_typename(typ._type_))
            else:
                return ast.rvalue(self.get_typename(typ))

    def create_define(self, name: str, value) -> ast.ast.Assign:
        return ast.assign(name, self.create_typename(value) if isinstance(value, type) else ast.Constant(value=value))

    def create_defines(self) -> tp.List[ast.stmt]:
        return [self.create_define(key, val) for key, val in self.typer.defines.items()]

    def create_typedef_predefined_base(self, name: str, base: CType):
        return self.create_define(name, base)

    def create_typedef_struct(self, name: str, ctype: CType):
        return ast.ClassDef(
            name=name, bases=[ast.rvalue('ctypes.Structure')],
            body=[
                 ast.assign('_fields_', ast.List(
                     elts=[ast.Tuple(elts=[ast.Constant(value=fname), self.create_typename(ftype)])
                           for fname, ftype in ctype._fields_]))
            ] + [
                 ast.AnnAssign(target=ast.lvalue(fname), annotation=self.create_typename(ftype))
                 for fname, ftype in ctype._fields_
            ]
        )

    @staticmethod
    def create_typedef_enum(name: str, ctype: CType):
        return ast.ClassDef(
            name=name, bases=[ast.rvalue('c_enum')],
            body=[ast.assign(key, ast.Constant(value=val)) for key, val in ctype._members.items()]
        )

    def create_typedef_multibase(self, name: str, ctype: CType):
        return ast.ClassDef(name=name, bases=list(map(self.create_typename, ctype.__bases__)), body=[ast.Pass()])

    def create_typedef(self, name: str, ctype: CType) -> ast.stmt:
        if isinstance(ctype, type):
            if len(ctype.__bases__) == 1:
                if (base := ctype.__bases__[0]) in self._createed_types:
                    return self.create_typedef_predefined_base(name, base)
                elif issubclass(ctype, ct.Structure):
                    return self.create_typedef_struct(name, ctype)
                elif issubclass(ctype, c_enum):
                    return self.create_typedef_enum(name, ctype)
            else:
                return self.create_typedef_multibase(name, ctype)

        return self.create_define(name, ctype)

    def create_typedefs(self) -> tp.List[ast.stmt]:
        self._createed_types = {}
        self._createed_types = {
            typ: self.get_typename(typ) for typ in self.typer.fundamental_typemap.values()
            if isinstance(typ, type)
        }

        return [(self.create_typedef(name, ctype), self._createed_types.__setitem__(ctype, name))[0]
                for pgxtype, ctype in self.typer.typemap.items()
                if ctype not in ct.__dict__.values()
                for name in [pgxtype.declaration.name if isinstance(pgxtype, d.declarated_t)else
                             pgxtype.name if isinstance(pgxtype, d.declaration_t) else
                             pgxtype._name]]

    def create_function(self, name: str, sig: inspect.Signature, body: tp.List[ast.stmt]) -> ast.FunctionDef:
        return ast.FunctionDef(
            name=name,
            args=ast.arguments(args=[
                ast.arg(arg=pname, annotation=self.create_typename(param.annotation))
                for pname, param in sig.parameters.items()
            ]),
            returns=self.create_typename(sig.return_annotation),
            body=body
        )

    def create_functions(self, dllvar='__dll') -> tp.List[ast.stmt]:
        return sum([
            [
                ast.assign(f'{cfuncname}.argtypes', ast.Tuple(
                    elts=list(self.create_typename(param.annotation) for param in sig.parameters.values())
                )),
                self.create_function(name, sig, body=list(lstrip((
                    docstring and ast.Expr(value=ast.Constant(value=self.format_docstring(docstring))),
                    ast.Return(value=ast.call(cfuncname, [ast.rvalue(pname) for pname in sig.parameters.keys()]))
                ), lambda x: x is None)))
            ]
            for name, sig in self.typer.functions.items()
            for cfuncname in [f'{dllvar}.{name}']
            for docstring in [self.doxml and self.doxml.get_docs(name)]
        ], [])

    def create(self, dllname=None, dllvar='__dll'):
        dllname = dllname or os.path.splitext(self.headername)[0]
        return ast.Module(body=[
            ast.Import(names=[ast.alias(name='ctypes')]),
            ast.ImportFrom(module=f'{cutils.__name__}', names=[ast.alias(name='c_enum')]),
            ast.assign('__dll',
                       ast.call('ctypes.cdll.LoadLibrary', [ast.Constant(value=dllname)]))
        ] + self.create_defines() + self.create_typedefs() + self.create_functions(dllvar=dllvar))

    def print(self, file: tp.Union[str, tp.TextIO], dllname=None, dllvar='__dll'):
        mod = self.create(dllname, dllvar)

        # Ugly hack
        with patch(source_repr.split_lines, '__defaults__', (65535,)):
            (open(file, 'w') if isinstance(file, str) else file).write(to_source(mod))
        return mod
