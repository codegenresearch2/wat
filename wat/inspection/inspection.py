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

def inspect_format(
    obj: Any,
    *,
    short: bool = False,
    dunder: bool = False,
    nodocs: bool = False,
    long: bool = False,
    code: bool = False,
    all: bool = False,
) -> str:
    config = InspectConfig(short=short, dunder=dunder or all, nodocs=nodocs, long=long or all, code=code or all)
    output: List[str] = []

    str_value = _format_value(obj)
    repr_value: str = repr(obj)
    if repr_value == str(obj) or repr_value == _strip_color(str_value):
        output.append(f'value: {str_value}')
    else:
        output.append(f'str: {str_value}')
        output.append(f'repr: {repr_value}')

    str_type = _format_type(type(obj))
    output.append(f'type: {str_type}')
    parents = _format_parent_types(obj)
    if parents:
        output.append(f'parents: {parents}')

    if isinstance(obj, (list, dict, str, bytes, bytearray, tuple, set, frozenset, range)):
        output.append(f'len: {_format_value(len(obj))}')
 
    if callable(obj):
        name = getattr(obj, '__name__', '…')
        signature = _get_callable_signature(name, obj)
        output.append(f'signature: {signature}')

    doc = _get_doc(obj, long=True)
    if doc and not config.nodocs and callable(obj):
        if doc.count('\n') == 0:
            output.append(f'"""{doc}"""')
        else:
            output.extend([f'"""', doc, f'"""'])

    if config.code and (std_inspect.isclass(obj) or callable(obj)):
        source = _get_source_code(obj)
        if source:
            output.append(f'source code:\n{source}')

    if not config.short:
        attributes = sorted(_iter_attributes(obj, config), key=lambda attr: attr.name)
        output.extend(_render_attrs_section(attributes, config))

    if sys.stdout.isatty():
        terminal_width = os.get_terminal_size().columns
        if not ("PYTHON_WAT_DISABLECOLOR" in os.environ and os.environ["PYTHON_WAT_DISABLECOLOR"] == 'true'):
            output.insert(0, '─' * terminal_width)
            output.append('─' * terminal_width)

    text = '\n'.join(line for line in output if line is not None)
    if (not sys.stdout.isatty()) or ("PYTHON_WAT_DISABLECOLOR" in os.environ and os.environ["PYTHON_WAT_DISABLECOLOR"] == 'true'):
        text = _strip_color(text)
    return text

def _iter_attributes(obj: Any, config: InspectConfig) -> Iterable[InspectAttribute]:
    keys = dir(obj)
    for key in keys:
        dunder = key.startswith('__') and key.endswith('__')
        if dunder and not config.dunder:
            continue
        private = key.startswith('_') and not dunder
        value = _get_attribute_value(obj, key)
        callable_ = callable(value)
        signature = _get_callable_signature(key, value) if callable_ else None
        doc = _get_doc(value, long=config.long) if callable_ else None
        yield InspectAttribute(
            name=key,
            value=value,
            type=type(value),
            callable=callable_,
            dunder=dunder,
            private=private,
            signature=signature,
            doc=doc,
        )

def _get_attribute_value(obj: Any, key: str) -> Any:
    try:
        return getattr(obj, key)
    except BaseException as e:
        return e

def _get_callable_signature(name: str, obj: Any) -> Optional[str]:
    try:
        _signature = str(std_inspect.signature(obj))
    except (ValueError, TypeError):
        _signature = "(…)"
    
    if std_inspect.isclass(obj):
        prefix = "class "
    elif std_inspect.iscoroutinefunction(obj):
        prefix = "async def "
    elif std_inspect.isfunction(obj):
        prefix = "def "
    elif std_inspect.ismethod(obj):
        prefix = "def "
    elif std_inspect.isbuiltin(obj):
        prefix = "def "
    elif hasattr(obj, '__name__'):
        prefix = "def "
    else:
        prefix = ""
    return f'{prefix}{name}{_signature}'

def _get_source_code(obj: Any) -> Optional[str]:
    try:
        return std_inspect.getsource(obj)
    except (OSError, TypeError, IndentationError) as e:
        return f'failed to get source code: {type(e)}: {e}'

def _get_doc(obj: Any, long: bool) -> Optional[str]:
    doc = std_inspect.getdoc(obj)
    if doc is None:
        return None
    doc = doc.strip()
    if long:
        return doc
    else:
        return _shorten_string(doc)

def _render_attr_variable(attr: InspectAttribute, config: InspectConfig) -> str:
    value_str = _format_short_value(attr.value, long=config.long)
    type_str = _format_type(attr.type)
    return f'  {attr.name}: {type_str} = {value_str}'

def _render_attr_method(attr: InspectAttribute) -> str:
    if not attr.signature:
        return f'  {attr.name}(…)'
    if attr.doc:
        if attr.doc.count('\n') == 0:
            return f'  {attr.signature}  # {attr.doc}'
        else:
            return f'  {attr.signature}:\n  """\n{attr.doc}\n  """'
    else:
        return f'  {attr.signature}'

def _format_short_value(value: Any, long: bool) -> str:
    value_str = _format_value(value)
    if long:
        return value_str
    return _shorten_string(value_str)

def _format_value(value: Any, indent: int = 0) -> str:
    if isinstance(value, str):
        return f"'{value}'"
    if value is None:
        return 'None'
    if value is True:
        return 'True'
    if value is False:
        return 'False'
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, dict):
        return _format_dict_value(value, indent=indent+1)
    if isinstance(value, list):
        return _format_list_value(value, indent=indent+1)
    return str(value)

def _format_dict_value(dic: Dict, indent: int) -> str:
    lines: List[str] = []
    indentation = '    ' * indent
    for key, value in dic.items():
        key_str = _format_value(key, indent)
        value_str = _format_value(value, indent)
        lines.append(f'{indentation}{key_str}: {value_str},')
    if lines:
        small_indent = "    " * (indent-1)
        middle_lines = '\n'.join(lines)
        return f'{{{RESET}\n{middle_lines}\n{small_indent}}}{RESET}'
    else:
        return '{}'

def _format_list_value(lst: List, indent: int) -> str:
    lines: List[str] = []
    for value in lst:
        value_str = _format_value(value, indent)
        lines.append('    ' * indent + f'{value_str},')
    if lines:
        small_indent = "    " * (indent-1)
        middle_lines = '\n'.join(lines)
        return f'[