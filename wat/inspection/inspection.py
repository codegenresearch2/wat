from dataclasses import dataclass
import inspect as std_inspect
import os
import re
import sys
from typing import Any, Dict, List, Optional, Type, Iterable, Union

# Environment variable check for color configuration
COLOR_ENABLED = os.environ.get('PYTHON_WAT_DISABLECOLOR', 'false').lower() != 'true'

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

def inspect_format(obj: Any, **config) -> str:
    output: List[str] = []

    str_value = _format_value(obj)
    repr_value: str = repr(obj)
    output.append(f'{"\033[1;34m" if COLOR_ENABLED else ""}value:{"\033[0m" if COLOR_ENABLED else ""} {str_value}')
    if repr_value != str(obj) and repr_value != _strip_color(str_value):
        output.append(f'{"\033[1;34m" if COLOR_ENABLED else ""}repr:{"\033[0m" if COLOR_ENABLED else ""} {"\033[1m" if COLOR_ENABLED else ""}{repr_value}{"\033[0m" if COLOR_ENABLED else ""}')

    str_type = _format_type(type(obj))
    output.append(f'{"\033[1;34m" if COLOR_ENABLED else ""}type:{"\033[0m" if COLOR_ENABLED else ""} {str_type}')
    parents = _format_parent_types(obj)
    if parents:
        output.append(f'{"\033[1;34m" if COLOR_ENABLED else ""}parents:{"\033[0m" if COLOR_ENABLED else ""} {parents}')

    if isinstance(obj, (list, dict, str, bytes, bytearray, tuple, set, frozenset, range)):
        output.append(f'{"\033[1;34m" if COLOR_ENABLED else ""}len:{"\033[0m" if COLOR_ENABLED else ""} {_format_value(len(obj))}')

    if callable(obj):
        name = getattr(obj, '__name__', '…')
        signature = _get_callable_signature(name, obj)
        output.append(f'{"\033[1;34m" if COLOR_ENABLED else ""}signature:{"\033[0m" if COLOR_ENABLED else ""} {signature}')

    doc = _get_doc(obj, long=True)
    if doc and not config.get('nodocs', False) and callable(obj):
        output.extend(_format_doc(doc))

    if config.get('code', False) and (std_inspect.isclass(obj) or callable(obj)):
        source = _get_source_code(obj)
        if source:
            output.append(f'{"\033[1;34m" if COLOR_ENABLED else ""}source code:{"\033[0m" if COLOR_ENABLED else ""}\n{source}')

    if not config.get('short', False):
        attributes = sorted(_iter_attributes(obj, config), key=lambda attr: attr.name)
        output.extend(_render_attrs_section(attributes, config))

    if sys.stdout.isatty() and COLOR_ENABLED:  # horizontal bar
        terminal_width = os.get_terminal_size().columns
        output.insert(0, f'\033[0;34m{"─" * terminal_width}\033[0m')
        output.append(f'\033[0;34m{"─" * terminal_width}\033[0m')

    text = '\n'.join(line for line in output if line is not None)
    if not sys.stdout.isatty() or not COLOR_ENABLED:
        text = _strip_color(text)
    return text

# Rest of the code remains the same as it is already optimized and readable