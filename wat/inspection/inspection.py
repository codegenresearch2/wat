from dataclasses import dataclass
import inspect as std_inspect
import os
import re
import sys
from typing import Any, Dict, List, Optional, Type, Iterable, Union

@dataclass
class InspectConfig:
    short: bool
    dunder: bool
    nodocs: bool
    long: bool
    code: bool

@dataclass
class InspectAttribute:
    name: str
    value: Any
    type: Type
    callable: bool
    dunder: bool
    private: bool
    signature: Optional[str]
    doc: Optional[str]

def inspect(obj: Any, *, short: bool = False, dunder: bool = False, nodocs: bool = False, long: bool = False, code: bool = False, all: bool = False):
    '''\n    Examine the object's information, such as its type, formatted value, variables, methods,\n    documentation or source code.\n    :param obj: object to inspect\n    :param short: whether to print short output without attributes (variables and methods)\n    :param long: whether to print non-abbreviated values and documentation\n    :param dunder: whether to print dunder attributes\n    :param code: whether to print source code of a function, method or class\n    :param nodocs: whether to hide documentation for functions and classes\n    :param all: whether to include all information\n    '''
    print(inspect_format(obj, short=short, dunder=dunder or all, long=long or all, nodocs=nodocs, code=code or all))

def inspect_format(obj: Any, *, short: bool = False, dunder: bool = False, nodocs: bool = False, long: bool = False, code: bool = False) -> str:
    config = InspectConfig(short=short, dunder=dunder, nodocs=nodocs, long=long, code=code)
    output: List[str] = []

    str_value = _format_value(obj)
    repr_value: str = repr(obj)
    if repr_value == str(obj) or repr_value == _strip_color(str_value):
        output.append(f'value:{str_value}')
    else:
        output.append(f'str:{str_value}')
        output.append(f'repr:{repr_value}')

    str_type = _format_type(type(obj))
    output.append(f'type:{str_type}')
    parents = _format_parent_types(obj)
    if parents:
        output.append(f'parents:{parents}')

    if isinstance(obj, (list, dict, str, bytes, bytearray, tuple, set, frozenset, range)):
        output.append(f'len:{_format_value(len(obj))}')

    if callable(obj):
        name = getattr(obj, '__name__', '…')
        signature = _get_callable_signature(name, obj)
        output.append(f'signature:{signature}')

    doc = _get_doc(obj, long=True) if not config.nodocs and callable(obj) else None
    if doc:
        output.extend([f'doc:{doc}'])

    if config.code and (std_inspect.isclass(obj) or callable(obj)):
        source = _get_source_code(obj)
        if source:
            output.append(f'source code:{source}')

    if not config.short:
        attributes = sorted(_iter_attributes(obj, config), key=lambda attr: attr.name)
        output.extend(_render_attrs_section(attributes, config))

    if sys.stdout.isatty():  # horizontal bar
        terminal_width = os.get_terminal_size().columns
        output.insert(0, '─' * terminal_width)
        output.append('─' * terminal_width)

    text = '\n'.join(line for line in output if line is not None)
    if not sys.stdout.isatty():
        text = _strip_color(text)
    return text

def _iter_attributes(obj: Any, config: InspectConfig) -> Iterable[InspectAttribute]:...

def _get_attribute_value(obj: Any, key: str) -> Any:...

def _get_callable_signature(name: str, obj: Any) -> Optional[str]:...

def _get_source_code(obj: Any) -> Optional[str]:...

def _get_doc(obj: Any, long: bool) -> Optional[str]:...

def _format_type(type_: Type) -> str:...

def _format_parent_types(obj: Any) -> str:...

def _format_value(value: Any, indent: int = 0) -> str:...

def _strip_color(text: str) -> str:...

class Wat:
    '''Inspector instance to examine unknown objects with short operators'''...
    def __init__(self, **kwargs):...
    def __repr__(self) -> str:...
    def __str__(self) -> str:...
    def _print_help(self):...
    def _react_with(self, other: Any):...
    def __call__(self, *args: Any, **kwargs: Any) -> Union['Wat', None]:...
    def __truediv__(self, other: Any): return self._react_with(other) # /
    def __add__(self, other: Any): return self._react_with(other) # +
    def __lshift__(self, other: Any): return self._react_with(other)  # <<
    def __rshift__(self, other: Any): return self._react_with(other)  # >>
    def __or__(self, other: Any): return self._react_with(other)  # |
    def __lt__(self, other: Any): return self._react_with(other)  # <
    def __getattr__(self, name) -> Union['Wat', None]:...

wat = Wat()