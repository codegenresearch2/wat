from typing import Any, Dict, List, Optional, Type, Iterable
import inspect
import os
import re
import sys


class InspectConfig:
    def __init__(self, short: bool, dunder: bool, nodocs: bool, long: bool, code: bool):
        self.short = short
        self.dunder = dunder
        self.nodocs = nodocs
        self.long = long
        self.code = code


class InspectAttribute:
    def __init__(self, name: str, value: Any, type_: Type, callable: bool, dunder: bool, private: bool, signature: Optional[str] = None, doc: Optional[str] = None):
        self.name = name
        self.value = value
        self.type = type_
        self.callable = callable
        self.dunder = dunder
        self.private = private
        self.signature = signature
        self.doc = doc


def inspect_format(obj, **kwargs) -> str:
    config = InspectConfig(short=kwargs.get('short', False), dunder=kwargs.get('dunder', False), nodocs=kwargs.get('nodocs', False), long=kwargs.get('long', False), code=kwargs.get('code', False))
    output = list(_produce_inspect_lines(obj, config))

    if sys.stdout.isatty() and _color_enabled():
        terminal_width = os.get_terminal_size().columns
        output.insert(0, '─' * terminal_width)
        output.append('─' * terminal_width)

    text = '\n'.join(line for line in output if line is not None)
    if not _color_enabled():
        text = _strip_color(text)
    return text


def _produce_inspect_lines(obj, config: InspectConfig) -> Iterable[str]:
    str_value = _format_value(obj)
    repr_value = repr(obj)
    if repr_value == str_value:
        yield f'value: {str_value}'
    else:
        yield f'str: {str_value}'
        yield f'repr: {repr_value}'

    type_str = _format_type(type(obj))
    yield f'type: {type_str}'
    if callable(getattr(obj, '__len__', None)):
        try:
            yield f'len: {_format_value(len(obj))}'
        except TypeError:
            pass

    if callable(obj):
        signature = _get_callable_signature(obj)
        yield f'signature: {signature}'

    doc = _get_doc(obj)
    if doc and not config.nodocs and callable(obj):
        yield doc

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
        callable_ = callable(value)
        signature = _get_callable_signature(value) if callable_ else None
        doc = _get_doc(value) if callable_ else None
        yield InspectAttribute(name=key, value=value, type_=type(value), callable=callable_, dunder=dunder, private=private, signature=signature, doc=doc)


def _get_callable_signature(obj) -> Optional[str]:
    try:
        signature = str(inspect.signature(obj))
    except (ValueError, TypeError):
        signature = '(…)'
    prefix = ''
    if inspect.isclass(obj):
        prefix = 'class '
    elif inspect.iscoroutinefunction(obj):
        prefix = 'async def '
    elif inspect.isfunction(obj) or inspect.ismethod(obj) or inspect.isbuiltin(obj) or hasattr(obj, '__name__'):
        prefix = 'def '
    return f'{prefix}{signature}'


def _get_source_code(obj) -> Optional[str]:
    try:
        return inspect.getsource(obj)
    except (OSError, TypeError, IndentationError) as e:
        return f'failed to get source code: {type(e)}: {e}'


def _get_doc(obj) -> Optional[str]:
    doc = inspect.getdoc(obj)
    if doc is None:
        return None
    return doc.strip()


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
    return str_val


def _format_dict_value(dic: Dict, indent: int) -> str:
    if indent > 30:
        return 'ERROR: too deeply nested'
    lines = []
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
    lines = []
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
    if module is None or module == str.__class__.__module__:
        return type_.__name__
    return f'{module}.{type_.__name__}'


def _shorten_string(text: str) -> str:
    first_line, _, rest = text.partition('\n')
    if rest:
        first_line = first_line + '…'
    if len(first_line) > 100:
        first_line = first_line[:100] + '…'
    return first_line


def _render_attrs_section(attributes: List[InspectAttribute], config: InspectConfig) -> Iterable[str]:
    for attr in attributes:
        if attr.private or attr.dunder or attr.callable:
            continue
        yield _render_attr_variable(attr, config)
    for attr in attributes:
        if not (attr.private or attr.dunder or attr.callable):
            continue
        yield _render_attr_method(attr)


def _list_local_variables() -> Dict[str, Any]:
    frame = inspect.currentframe()
    try:
        for _ in range(2):
            frame = frame.f_back
        return frame.f_locals if frame is not None else {}
    finally:
        del frame


def _list_global_variables() -> Dict[str, Any]:
    frame = inspect.currentframe()
    try:
        for _ in range(2):
            frame = frame.f_back
        return frame.f_globals if frame is not None else {}
    finally:
        del frame


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
        text = f'''Try wat / object or wat.modifiers / object to inspect an object. Modifiers are:\n  .short or .s to hide attributes (variables and methods)\n  .dunder to print dunder attributes\n  .code to print source code of a function, method or class\n  .long to print non-abbreviated values and documentation\n  .nodocs to hide documentation for functions and classes\n  .all to include all information\n  .ret to return the inspected object\n  .str to return the output string instead of printing\n  .gray to disable colorful output in the console\nCall wat.locals or wat() to inspect local variables.\nCall wat.globals to inspect global variables.'''
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
            return self._print_variables(_list_local_variables(), 'Local variables')
    
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

    def __truediv__(self, other): return self.inspect(other)
    def __add__(self, other): return self.inspect(other)
    def __lshift__(self, other): return self.inspect(other)
    def __rshift__(self, other): return self.inspect(other)
    def __or__(self, other): return self.inspect(other)
    def __ror__(self, other): return self.inspect(other)
    def __lt__(self, other): return self.inspect(other)

    def __getattr__(self, name) -> Union['Wat', str, None]:
        new_wat = self.copy() 
        if name in {'short', 's'}:
            new_wat._inspect_kwargs['short'] = True
        elif name == 'long':
            new_wat._inspect_kwargs['long'] = True
        elif name == 'dunder':
            new_wat._inspect_kwargs['dunder'] = True
        elif name == 'code':
            new_wat._inspect_kwargs['code'] = True
        elif name == 'nodocs':
            new_wat._inspect_kwargs['nodocs'] = True
        elif name == 'all':
            new_wat._inspect_kwargs['all'] = True
        elif name == 'ret':
            new_wat._config['ret'] = True
        elif name == 'str':
            new_wat._config['str'] = True
        elif name == 'gray':
            new_wat._config['gray'] = True
        elif name == 'locals':
            return self._print_variables(_list_local_variables(), 'Local variables')
        elif name == 'globals':
            return self._print_variables(_list_global_variables(), 'Global variables')
        elif name == 'wat':
            return self
        else:
            raise AttributeError
        return new_wat


wat = Wat()