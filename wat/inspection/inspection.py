from dataclasses import dataclass
import inspect
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


def _yield_inspect_lines(obj, config: InspectConfig) -> Iterable[str]:
    str_value = _format_value(obj)
    repr_value: str = repr(obj)
    if repr_value == str(obj) or repr_value == _strip_color(str_value):
        yield f'value: {str_value}'
    else:
        yield f'str: {str_value}'
        yield f'repr: {repr_value}'

    str_type = _format_type(type(obj))
    yield f'type: {str_type}'
    parents = ', '.join(_get_parent_types(type(obj)))
    if parents:
        yield f'parents: {parents}'

    if callable(getattr(obj, '__len__', None)):
        try:
            yield f'len: {_format_value(len(obj))}'
        except TypeError:
            pass
 
    if callable(obj):
        name = getattr(obj, '__name__', '…')
        signature = _get_callable_signature(name, obj)
        yield f'signature: {signature}'
    
    if config.caller:
        yield from _retrieve_caller_info()

    doc = _get_doc(obj, long=True)
    if doc and not config.nodocs and callable(obj):
        if doc.count('\n') == 0:
            yield f'"""{doc}"""'
        else:
            yield from [f'"""', doc, f'"""']

    if config.code and (inspect.isclass(obj) or callable(obj)):
        source = _get_source_code(obj)
        if source:
            yield f'source code:\n{source}'

    if not config.short:
        attributes = sorted(_iter_attributes(obj, config), key=lambda attr: attr.name)
        yield from _render_attrs_section(attributes, config)


def _iter_attributes(obj, config: InspectConfig) -> Iterable[InspectAttribute]:
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
        signature = _get_callable_signature(key, value) if _callable else None
        doc = _get_doc(value, long=config.long) if _callable else None
        yield InspectAttribute(
            name=key, value=value, type=type(value), callable=_callable, dunder=dunder,
            private=private, signature=signature, doc=doc,
        )


def _get_callable_signature(name: str, obj) -> Optional[str]:
    try:
        _signature = str(inspect.signature(obj))
    except (ValueError, TypeError):
        _signature = '(…)'
    
    if inspect.isclass(obj):
        prefix = 'class '
    elif inspect.iscoroutinefunction(obj):
        prefix = 'async def '
    elif inspect.isfunction(obj) or inspect.ismethod(obj) or inspect.isbuiltin(obj) or hasattr(obj, '__name__'):
        prefix = 'def '
    else:
        prefix = ''
    return f'{prefix}{name}{_signature}'


def _get_source_code(obj) -> Optional[str]:
    try:
        return inspect.getsource(obj)
    except (OSError, TypeError, IndentationError) as e:
        return f'failed to get source code: {type(e)}: {e}'


def _get_doc(obj, long: bool) -> Optional[str]:
    doc = inspect.getdoc(obj)
    if doc is None:
        return None
    doc = doc.strip()
    return doc if long else _shorten_string(doc)


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
            return f'  {attr.signature}:\n"""\n{attr.doc}\n"""'
    else:
        return f'  {attr.signature}'


def _format_short_value(value, long: bool) -> str:
    value_str = _format_value(value)
    if long:
        return value_str
    return _shorten_string(value_str)


def _format_value(value, indent: int = 0) -> str:
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
    str_val = str(value)
    angle_bracket_match = re.fullmatch(r'<(.*)>', str_val)
    if angle_bracket_match:
        return f'<{angle_bracket_match.group(1)}>'
    return str_val


def _format_dict_value(dic: Dict, indent: int) -> str:
    if indent > 30:
        return 'ERROR: too deeply nested'
    lines: List[str] = []
    indentation = '    ' * indent
    for key, value in dic.items():
        key_str = _format_value(key, indent)
        value_str = _format_value(value, indent)
        lines.append(f'{indentation}{key_str}: {value_str},')
    if lines:
        small_indent = '    ' * (indent-1)
        middle_lines = '\n'.join(lines)
        return f'{{{RESET}\n{middle_lines}\n{small_indent}{RESET}}}'
    else:
        return '{}'


def _format_list_value(lst: List, indent: int) -> str:
    lines: List[str] = []
    for value in lst:
        value_str = _format_value(value, indent)
        lines.append('    ' * indent + f'{value_str},')
    if lines:
        small_indent = '    ' * (indent-1)
        middle_lines = '\n'.join(lines)
        return f'[{RESET}\n{middle_lines}\n{small_indent}{RESET}]'
    else:
        return '[]'


def _format_type(type_: Type) -> str:
    module = type_.__module__
    if module is None or module == str.__class__.__module__:  # built-in type
        return type_.__name__
    return f'{module}.{type_.__name__}'


def _get_parent_types(type_: Type) -> Iterable[str]:
    if hasattr(type_, '__mro__'):
        for index, base_type in enumerate(type_.__mro__):
            if index == 0 or base_type is object:
                continue
            yield _format_type(base_type)


def _retrieve_caller_info() -> Iterable[str]:
    frame = _caller_stack_frame(6)
    if frame:
        frameinfo = inspect.getframeinfo(frame)
        if frameinfo.code_context:
            code = '\n'.join(frameinfo.code_context).strip()
            yield f'caller expression: {code}'
        if frameinfo.filename:
            yield f'caller file: {frameinfo.filename}:{frameinfo.lineno}'


def _shorten_string(text: str) -> str:
    first_line, _, rest = text.partition('\n')
    if rest:
        first_line = first_line + '…'
    if len(first_line) > 100:
        first_line = first_line[:100] + '…'
    return first_line


def _render_attrs_section(attributes: List[InspectAttribute], config: InspectConfig) -> Iterable[str]:
    public_vars = [a for a in attributes if not a.private and not a.dunder and not a.callable]
    private_vars = [a for a in attributes if a.private and not a.callable]
    dunder_vars = [a for a in attributes if a.dunder and not a.callable]
    public_methods = [a for a in attributes if not a.private and not a.dunder and a.callable]
    private_methods = [a for a in attributes if a.private and a.callable]
    dunder_methods = [a for a in attributes if a.dunder and a.callable]

    if public_vars or public_methods:
        yield ''
        yield 'Public attributes:'
        for attr in public_vars:
            yield _render_attr_variable(attr, config)
        if public_vars and public_methods:
            yield ''
        for attr in public_methods:
            yield _render_attr_method(attr)
    
    if private_vars or private_methods:
        yield ''
        yield 'Private attributes:'
        for attr in private_vars:
            yield _render_attr_variable(attr, config)
        if private_vars and private_methods:
            yield ''
        for attr in private_methods:
            yield _render_attr_method(attr)

    if config.dunder and (dunder_vars or dunder_methods):
        yield ''
        yield 'Dunder attributes:'
        for attr in dunder_vars:
            yield _render_attr_variable(attr, config)
        if dunder_vars and dunder_methods:
            yield ''
        for attr in dunder_methods:
            yield _render_attr_method(attr)


def _caller_stack_frame(depth: int):
    frame = inspect.currentframe()
    for _ in range(depth):  # back to caller frame
        if frame is not None:
            frame = frame.f_back
    return frame


def _render_variables(variables: Dict[str, Any], title: str) -> Iterable[str]:
    yield f'{title}:'
    for name in sorted(variables.keys()):
        value = variables[name]
        value_str = _format_short_value(value, long=False)
        type_str = _format_type(type(value))
        yield f'  {name}: {type_str} = {value_str}'


def _color_enabled() -> bool:
    env_color = {
        'false': False,
        'true': True,
    }.get(os.environ.get('WAT_COLOR', '').lower())
    if env_color is not None:
        return env_color
    return sys.stdout.isatty()


def _strip_color(text: str) -> str:
    return re.sub(r'\x1b\[\d+(;\d+)?m', '', text)


class Wat:
    '''Inspector instance to examine unknown objects with short operators'''
    def __init__(self, **inspect_kwargs):
        self._inspect_kwargs = inspect_kwargs
        self._config = {}
        self._inspect_in_progress = False

    def __repr__(self) -> str:
        if not wat._inspect_in_progress:
            self._print_help()
        return ''
        
    def __str__(self) -> str:
        return '<WAT Inspector object>'
    
    def _print_help(self):
        text = f'''Try wat / object or wat.modifiers / object to inspect an object. Modifiers are:\n  .short or .s to hide attributes (variables and methods)\n  .dunder to print dunder attributes\n  .code to print source code of a function, method or class\n  .long to print non-abbreviated values and documentation\n  .nodocs to hide documentation for functions and classes\n  .caller to show how and where the inspection was called\n  .all to include all information\n  .ret to return the inspected object\n  .str to return the output string instead of printing\n  .gray to disable colorful output in the console\nCall wat.locals or wat() to inspect local variables.\nCall wat.globals to inspect global variables.'''
        if not _color_enabled():
            text = _strip_color(text)
        print(text)
    
    def __call__(self, *args, **kwargs):
        if args:
            inspect_kwargs = self._inspect_kwargs.copy()
            inspect_kwargs.update(kwargs)
            return Wat(**inspect_kwargs).inspect(*args)
        elif kwargs:
            return Wat(**kwargs)
        else:
            frame = _caller_stack_frame(2)
            local_vars = frame.f_locals if frame else {}
            return self._print_variables(local_vars, 'Local variables')
    
    def inspect(self, other):
        wat._inspect_in_progress = True
        try:
            output = inspect_format(other, **self._inspect_kwargs)
            output_return = self._display_output(output)
            if output_return:
                return output_return
            if self._config.get('ret', False):
                return other
            return None
        finally:
            wat._inspect_in_progress = False
    
    def copy(self) -> 'Wat':
        new_wat = Wat(**self._inspect_kwargs)
        new_wat._config = self._config.copy()
        return new_wat
    
    def _display_output(self, output: str) -> Optional[str]:
        if self._config.get('gray', False) or not _color_enabled():
            output = _strip_color(output)
        if self._config.get('str', False):
            return output
        print(output)
        return None

    def _print_variables(self, variables: Dict[str, Any], title: str) -> Optional[str]:
        lines = list(_render_variables(variables, title))
        output = '\n'.join(line for line in lines if line is not None)
        return self._display_output(output)

    def __truediv__(self, other): return self.inspect(other)  # /
    def __add__(self, other): return self.inspect(other)  # +
    def __lshift__(self, other): return self.inspect(other)  # <<
    def __rshift__(self, other): return self.inspect(other)  # >>
    def __or__(self, other): return self.inspect(other)  # wat |
    def __ror__(self, other): return self.inspect(other)  # | wat
    def __lt__(self, other): return self.inspect(other)  # <

    def __getattr__(self, name) -> Union['Wat', str, None]:
        new_wat = self.copy() 
        if name in {'short', 's'}:
            new_wat._inspect_kwargs['short'] = True
        elif name in {'long', 'dunder', 'code', 'nodocs', 'caller', 'all'}:
            new_wat._inspect_kwargs[name] = True
        elif name in {'ret', 'str', 'gray'}:
            new_wat._config[name] = True
        elif name == 'locals':
            frame = _caller_stack_frame(2)
            local_vars = frame.f_locals if frame else {}
            return self._print_variables(local_vars, 'Local variables')
        elif name == 'globals':
            frame = _caller_stack_frame(2)
            global_vars = frame.f_globals if frame else {}
            return self._print_variables(global_vars, 'Global variables')
        elif name == 'wat':
            return self
        else:
            raise AttributeError
        return new_wat


RESET = '\033[0m'
STYLE_BRIGHT = '\033[1m'
STYLE_RED = '\033[0;31m'
STYLE_BRIGHT_RED = '\033[1;31m'
STYLE_GREEN = '\033[0;32m'
STYLE_BRIGHT_GREEN = '\033[1;32m'
STYLE_YELLOW = '\033[0;33m'
STYLE_BRIGHT_YELLOW = '\033[1;33m'
STYLE_BLUE = '\033[0;34m'
STYLE_BRIGHT_BLUE = '\033[1;34m'
STYLE_MAGENTA = '\033[0;35m'
STYLE_CYAN = '\033[0;36m'
STYLE_GRAY = '\033[2;37m'

wat = Wat()