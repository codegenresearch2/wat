from dataclasses import dataclass
import inspect as std_inspect
import os
import re
import sys
from typing import Any, Dict, List, Optional, Type, Iterable, Union

# Added environment variable handling for color
COLOR_ENABLED = os.getenv('WAT_COLOR', 'true').lower() != 'false'

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
        output.append(f'{"value:" if COLOR_ENABLED else "value:"} {str_value}')
    else:
        output.append(f'{"str:" if COLOR_ENABLED else "str:"} {str_value}')
        output.append(f'{"repr:" if COLOR_ENABLED else "repr:"} {repr_value}')

    str_type = _format_type(type(obj))
    output.append(f'{"type:" if COLOR_ENABLED else "type:"} {str_type}')
    parents = _format_parent_types(obj)
    if parents:
        output.append(f'{"parents:" if COLOR_ENABLED else "parents:"} {parents}')

    if isinstance(obj, (list, dict, str, bytes, bytearray, tuple, set, frozenset, range)):
        output.append(f'{"len:" if COLOR_ENABLED else "len:"} {float(len(obj))}')

    if callable(obj):
        name = getattr(obj, '__name__', '…')
        signature = _get_callable_signature(name, obj)
        output.append(f'{"signature:" if COLOR_ENABLED else "signature:"} {signature}')

    doc = _get_doc(obj, long=True)
    if doc and not config.nodocs and callable(obj):
        if doc.count('\n') == 0:
            output.append(f'"""{doc}"""')
        else:
            output.extend([f'"""', doc, f'"""'])

    if config.code and (std_inspect.isclass(obj) or callable(obj)):
        source = _get_source_code(obj)
        if source:
            output.append(f'{"source code:" if COLOR_ENABLED else "source code:"}\n{source}')

    if not config.short:
        attributes = sorted(_iter_attributes(obj, config), key=lambda attr: attr.name)
        output.extend(_render_attrs_section(attributes, config))

    if sys.stdout.isatty() and COLOR_ENABLED:
        terminal_width = os.get_terminal_size().columns
        output.insert(0, '─' * terminal_width)
        output.append('─' * terminal_width)

    text = '\n'.join(line for line in output if line is not None)
    if not sys.stdout.isatty() or not COLOR_ENABLED:
        text = _strip_color(text)
    return text

# Rest of the code remains the same as it follows the provided rules