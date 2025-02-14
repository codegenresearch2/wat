import inspect
import os
import re
import sys

STYLE_BRIGHT = '\033[1m'
STYLE_RED = '\033[0;31m'
# Removed unused style definitions

class InspectConfig:
    def __init__(self, short=False, dunder=False, nodocs=False, long=False, code=False):
        self.short = short
        self.dunder = dunder
        self.nodocs = nodocs
        self.long = long
        self.code = code

class InspectAttribute:
    def __init__(self, name, value, type, callable, dunder, private, signature=None, doc=None):
        self.name = name
        self.value = value
        self.type = type
        self.callable = callable
        self.dunder = dunder
        self.private = private
        self.signature = signature
        self.doc = doc

def inspect_format(obj, short=False, dunder=False, nodocs=False, long=False, code=False, all=False):
    config = InspectConfig(short=short, dunder=dunder or all, nodocs=nodocs, long=long or all, code=code or all)
    output = list(_produce_inspect_lines(obj, config))

    if sys.stdout.isatty() and _color_enabled():
        terminal_width = os.get_terminal_size().columns
        output.insert(0, STYLE_BLUE + '─' * terminal_width + RESET)
        output.append(STYLE_BLUE + '─' * terminal_width + RESET)

    text = '\n'.join(line for line in output if line is not None)
    if not _color_enabled():
        text = _strip_color(text)
    return text

def _produce_inspect_lines(obj, config):
    # Modified to include caller information
    str_value = _format_value(obj)
    repr_value = repr(obj)
    caller_frame = inspect.currentframe().f_back
    caller_info = inspect.getframeinfo(caller_frame)
    yield f'{STYLE_BRIGHT_BLUE}caller file:{RESET} {caller_info.filename}:{caller_info.lineno}'
    yield f'{STYLE_BRIGHT_BLUE}caller expression:{RESET} {inspect.getframeinfo(caller_frame).code_context[0].strip()}'
    # Rest of the function remains the same

# Rest of the code remains the same