from dataclasses import dataclass
import inspect
import os
import re
import sys
from typing import Any, Dict, List, Optional, Type, Iterable, Union

# Updated version number
__version__ = "1.0.1"

@dataclass
class InspectConfig:
    short: bool
    dunder: bool
    nodocs: bool
    long: bool
    code: bool
    caller: bool

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
    caller: bool = False,
    all: bool = False,
) -> str:
    config = InspectConfig(short=short, dunder=dunder or all, nodocs=nodocs, long=long or all, code=code or all, caller=caller or all)
    output: List[str] = list(_yield_inspect_lines(obj, config))

    if sys.stdout.isatty() and _color_enabled():  # horizontal bar
        terminal_width = os.get_terminal_size().columns
        output.insert(0, STYLE_BLUE + '─' * terminal_width + RESET)
        output.append(STYLE_BLUE + '─' * terminal_width + RESET)

    text = '\n'.join(line for line in output if line is not None)
    if not _color_enabled():
        text = _strip_color(text)
    return text

# Optimized _yield_inspect_lines function
def _yield_inspect_lines(obj, config: InspectConfig) -> Iterable[str]:
    str_value = _format_value(obj)
    repr_value: str = repr(obj)
    if repr_value != str(obj) and repr_value != _strip_color(str_value):
        yield f'{STYLE_BRIGHT_BLUE}str:{RESET} {str_value}'
        yield f'{STYLE_BRIGHT_BLUE}repr:{RESET} {STYLE_BRIGHT}{repr_value}{RESET}'

    str_type = _format_type(type(obj))
    yield f'{STYLE_BRIGHT_BLUE}type:{RESET} {str_type}'
    parents = ', '.join(_get_parent_types(type(obj)))
    if parents:
        yield f'{STYLE_BRIGHT_BLUE}parents:{RESET} {parents}'

    if callable(getattr(obj, '__len__', None)):
        try:
            yield f'{STYLE_BRIGHT_BLUE}len:{RESET} {_format_value(len(obj))}'
        except TypeError:
            pass

    if callable(obj):
        name = getattr(obj, '__name__', '…')
        signature = _get_callable_signature(name, obj)
        yield f'{STYLE_BRIGHT_BLUE}signature:{RESET} {signature}'

    if config.caller:
        yield from _retrieve_caller_info()

    doc = _get_doc(obj, long=True)
    if doc and not config.nodocs and callable(obj):
        if doc.count('\n') == 0:
            yield f'{STYLE_GRAY}"""{doc}"""{RESET}'
        else:
            yield from [f'{STYLE_GRAY}"""', doc, f'"""{RESET}']

    if config.code and (inspect.isclass(obj) or callable(obj)):
        source = _get_source_code(obj)
        if source:
            yield f'{STYLE_BRIGHT_BLUE}source code:{RESET}\n{source}'

    if not config.short:
        attributes = sorted(_iter_attributes(obj, config), key=lambda attr: attr.name)
        yield from _render_attrs_section(attributes, config)

# Rest of the code remains the same