from datetime import datetime
from enum import Enum
import os
import re

from pydantic import BaseModel

from wat import Wat
from wat.inspection.inspection import InspectConfig, InspectAttribute, _produce_inspect_lines, _iter_attributes, _render_attrs_section, _color_enabled

wat = Wat(caller=True)

def inspect_format(obj, **kwargs):
    config = InspectConfig(caller=True, **kwargs)
    output = list(_produce_inspect_lines(obj, config))

    if _color_enabled():
        output.insert(0, '\033[1;34m─' * os.get_terminal_size().columns + '\033[0m')
        output.append('\033[1;34m─' * os.get_terminal_size().columns + '\033[0m')

    text = '\n'.join(line for line in output if line is not None)
    if not _color_enabled():
        text = _strip_color(text)
    return text

def _produce_inspect_lines(obj, config: InspectConfig):
    yield f'value: {_format_value(obj)}'
    yield f'type: {_format_type(type(obj))}'

    if config.caller:
        yield from _get_caller_info()

    if not config.short:
        attributes = sorted(_iter_attributes(obj, config), key=lambda attr: attr.name)
        yield from _render_attrs_section(attributes, config)

def _iter_attributes(obj, config: InspectConfig):
    for key in dir(obj):
        dunder = key.startswith('__') and key.endswith('__')
        if dunder and not config.dunder:
            continue
        private = key.startswith('_') and not dunder
        try:
            value = getattr(obj, key)
        except BaseException as e:
            value = e
        _callable = callable(value)
        yield InspectAttribute(name=key, value=value, type=type(value), callable=_callable, dunder=dunder, private=private)

def _format_value(value):
    if isinstance(value, str):
        return f"\033[0;32m'{value}'\033[0m"
    if value is None:
        return '\033[0;35mNone\033[0m'
    if value is True:
        return '\033[1;32mTrue\033[0m'
    if value is False:
        return '\033[1;31mFalse\033[0m'
    if isinstance(value, (int, float)):
        return f'\033[0;31m{value}\033[0m'
    str_val = str(value)
    angle_bracket_match = re.fullmatch(r'<(.*)>', str_val)
    if angle_bracket_match:
        return f'\033[0;33m<{angle_bracket_match.group(1)}>\033[0m'
    return f'\033[0;32m{str_val}\033[0m'

def _format_type(type_):
    return f'\033[0;33m{type_.__name__}\033[0m'

def _get_caller_info():
    frame = inspect.currentframe()
    try:
        for _ in range(5):
            if frame is not None:
                frame = frame.f_back
        if frame:
            frameinfo = inspect.getframeinfo(frame)
            if frameinfo.code_context:
                code = '\n'.join(frameinfo.code_context).strip()
                yield f'\033[1;34mcaller expression:\033[0m {code}'
                yield f'\033[1;34mcaller file:\033[0m {frameinfo.filename}:{frameinfo.lineno}'
        return None
    finally:
        del frame

def _strip_color(text: str):
    return re.sub(r'\x1b\[\d+(;\d+)?m', '', text)

# The rest of the code remains the same as it does not have to be changed according to the rules provided.