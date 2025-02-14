import inspect as std_inspect
import os
import re
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Type, Iterable, Union

# Added environment variable check for color configuration
COLOR_ENABLED = os.environ.get("PYTHON_WAT_DISABLECOLOR", "false") != "true"

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
    short: bool = False,
    dunder: bool = False,
    nodocs: bool = False,
    long: bool = False,
    code: bool = False,
    all: bool = False,
) -> str:
    config = InspectConfig(short=short, dunder=dunder or all, nodocs=nodocs, long=long or all, code=code or all)
    output = []
    output.append(format_value(obj, config))
    output.append(format_type(obj))
    output.append(format_parent_types(obj))
    output.append(format_length(obj))
    output.append(format_callable_signature(obj))
    output.append(format_doc(obj, config))
    output.append(format_source_code(obj, config))
    output.append(format_attributes(obj, config))
    output = [line for line in output if line is not None]
    if COLOR_ENABLED:
        output = add_color_bars(output)
    return strip_color(''.join(output)) if not COLOR_ENABLED else ''.join(output)

def format_value(obj: Any, config: InspectConfig) -> str:
    str_value = _format_value(obj)
    repr_value = repr(obj)
    if repr_value == str(obj) or repr_value == strip_color(str_value):
        return f'value: {str_value}'
    else:
        return f'str: {str_value}\nrepr: {repr_value}'

def format_type(obj: Any) -> str:
    return f'type: {_format_type(type(obj))}'

def format_parent_types(obj: Any) -> Optional[str]:
    parents = _format_parent_types(obj)
    return f'parents: {parents}' if parents else None

def format_length(obj: Any) -> Optional[str]:
    if isinstance(obj, (list, dict, str, bytes, bytearray, tuple, set, frozenset, range)):
        return f'len: {_format_value(len(obj))}'
    return None

def format_callable_signature(obj: Any) -> Optional[str]:
    if callable(obj):
        name = getattr(obj, '__name__', '…')
        signature = _get_callable_signature(name, obj)
        return f'signature: {signature}'
    return None

def format_doc(obj: Any, config: InspectConfig) -> Optional[str]:
    if callable(obj) and not config.nodocs:
        doc = _get_doc(obj, long=config.long)
        if doc:
            return f'doc: """\n{doc}\n"""' if doc.count('\n') > 0 else f'doc: """{doc}"""'
    return None

def format_source_code(obj: Any, config: InspectConfig) -> Optional[str]:
    if config.code and (std_inspect.isclass(obj) or callable(obj)):
        source = _get_source_code(obj)
        if source:
            return f'source code:\n{source}'
    return None

def format_attributes(obj: Any, config: InspectConfig) -> Optional[str]:
    if not config.short:
        attributes = sorted(_iter_attributes(obj, config), key=lambda attr: attr.name)
        return '\n'.join(_render_attrs_section(attributes, config))
    return None

def add_color_bars(output: List[str]) -> List[str]:
    if sys.stdout.isatty():
        terminal_width = os.get_terminal_size().columns
        output.insert(0, STYLE_BLUE + '─' * terminal_width + RESET)
        output.append(STYLE_BLUE + '─' * terminal_width + RESET)
    return output

# ... Rest of the code remains the same ...


In this refactored version, I've added an environment variable check to determine whether to use colored output or not. I've also simplified the `inspect_format` function by extracting the formatting logic into separate functions, reducing complexity. The `format_attributes` function now only returns the formatted attributes if `config.short` is False, and the `add_color_bars` function has been moved outside of the `inspect_format` function to improve readability.