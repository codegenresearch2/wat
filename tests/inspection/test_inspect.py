from datetime import datetime
from enum import Enum
import math
import os
import re

from pydantic import BaseModel

import wat
from wat.inspection.inspection import inspect_format
from tests.asserts import assert_multiline_match, strip_ansi_colors, StdoutCap


def generate_caller_info(config):
    if config.get('caller', False):
        frame = _caller_stack_frame(6)
        if frame:
            frameinfo = inspect.getframeinfo(frame)
            if frameinfo.filename:
                yield f'caller file: {frameinfo.filename}:{frameinfo.lineno}'
            if frameinfo.code_context:
                code = '\n'.join(frameinfo.code_context).strip()
                yield f'caller expression: {code}'


def inspect_primitive_var(obj, config):
    output = inspect_format(obj, **config)
    return strip_ansi_colors(output)


def inspect_instance(cls, config):
    instance = cls()
    output = inspect_format(instance, **config)
    return assert_multiline_match(output, r'''\nvalue: <object at .*>\ntype: type\n\nPublic attributes:\n  def .*\n''')


def inspect_function(func, config):
    output = inspect_format(func, **config)
    return assert_multiline_match(output, r'''\nvalue: <function .*>\ntype: function\nsignature: def .*\n"""\n.\n"""\n''')


def inspect_nested_dict(dic, config):
    output = inspect_format(dic, **config)
    return assert_multiline_match(output, r'''\nvalue: {\n    .*\n}\ntype: dict\nlen: .\n''')


def inspect_datetime_repr(dt, config):
    output = inspect_format(dt, **config)
    return assert_multiline_match(output, r'''\nstr: .\nrepr: datetime.datetime(.*)\ntype: datetime.datetime\nparents: datetime.date\n''')


def inspect_long(obj, config):
    output = inspect_format(obj, long=True, code=True)
    lines = output.splitlines()
    assert "value: <class 'datetime.datetime'>" in lines
    assert "type: type" in lines
    assert "signature: class datetime(…)" in lines
    assert "datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])" in lines


def inspect_source_code(cls, config):
    output = inspect_format(cls, code=True)
    lines = output.splitlines()
    assert "value: <class 'test_inspect.test_inspect_source_code.<locals>.cls'>" in lines
    assert "type: type" in lines
    assert "signature: class cls()" in lines
    assert "source code:" in lines
    assert "    class cls:" in lines
    assert "            self.level += 1" in lines


def inspect_async_def(func, config):
    output = inspect_format(func, short=True)
    return assert_multiline_match(output, r'''\nvalue: <function .*>\ntype: function\nsignature: async def .*\n''')


def test_wat_with_nothing():
    assert str(wat) == '<WAT Inspector object>'
    with StdoutCap() as capture:
        assert repr(wat) == ''
    assert 'Try wat / object or wat.modifiers / object to inspect an object. Modifiers are:' in capture.uncolor().splitlines()


def test_wat_locals():
    _local_var = 23
    output = wat.str.gray.locals.splitlines()
    assert 'Local variables:' in output
    assert '  _local_var: int = 23' in output

    with StdoutCap() as capture:
        wat()
    assert 'Local variables' in capture.uncolor()
    assert '  _local_var: int = 23' in capture.uncolor()


global_var = 23

def test_wat_globals():
    output = wat.str.gray.globals.splitlines()
    assert 'Global variables:' in output
    assert '  global_var: int = 23' in output
    assert "  __name__: str = 'test_inspect'" in output


def test_wat_with_object():
    with StdoutCap() as capture:
        wat(short=True) / 'moo'
    assert_multiline_match(capture.output(), r'''\nvalue: 'moo'\ntype: str\nlen: 3\n''')

    with StdoutCap() as capture:
        wat('moo', short=True)
    assert_multiline_match(capture.output(), r'''\nvalue: 'moo'\ntype: str\nlen: 3\n''')


def test_wat_with_short_long_modifiers():
    with StdoutCap() as capture:
        wat.short('moo')
    assert_multiline_match(capture.output(), r'''\nvalue: 'moo'\ntype: str\nlen: 3\n''')

    with StdoutCap() as capture:
        wat.long / 'moo2'
    assert r'''\n  def capitalize():\n"""\n''' in capture.output()


def test_wat_with_multiple_modifiers():
    with StdoutCap() as capture:
        wat.dunder.code / re.match

    assert '''\nDunder attributes:\n''' in capture.output()
    assert '''  def __eq__(value, /)''' in capture.output()
    
    assert '''\nsource code:\ndef match(pattern, string, flags=0):\n''' in capture.output()
    

def test_wat_modifiers_all_but_nodocs():
    with StdoutCap() as capture:
        wat.all.short.nodocs / re.match
    assert_multiline_match(capture.stripped(), r'''\nvalue: <function match at .*>\ntype: function\nsignature: def match(pattern, string, flags=0)\ncaller expression: wat.all.short.nodocs / re.match\ncaller file: .*/tests/inspection/test_inspect.py:\d+\nsource code:\ndef match(pattern, string, flags=0):\n    """.*\n    .*"""\n    .*\n''')


def test_list_parent_classes():
    class Parent(str, Enum):
        FIRST = 'first'

    output = inspect_format(Parent.FIRST, short=True)
    assert_multiline_match(output, r'''\nstr: '(Parent\.FIRST|first)'\nrepr: <Parent\.FIRST: 'first'>\ntype: test_inspect.Parent\nparents: str, enum.Enum\nlen: 5\n''')
    

def test_list_deep_mro_classes():
    class Grand(object):
        pass

    class Father(Grand):
        pass

    class Son(Father):
        pass

    output = inspect_format(Son(), short=True)
    assert_multiline_match(output, r'''\nvalue: <test_inspect.test_list_deep_mro_classes.<locals>.Son object at .*>\ntype: test_inspect.Son\nparents: test_inspect.Father, test_inspect.Grand\n''')


def test_pydantic_class():
    class Person(BaseModel):
        name: str

    output = inspect_format(Person(name='george'), short=True)
    assert_multiline_match(output, r'''\nstr: name='george'\nrepr: Person(name='george')\ntype: test_inspect.Person\nparents: pydantic.main.BaseModel\n''')


def test_returning_inspected_object():
    assert wat.short.ret / 'hello' == 'hello'


def test_listing_private_attributes():
    class Foo:
        def __init__(self, name: str):
            self._name = name
        
        def _private_method(self):
            pass
    
    output = inspect_format(Foo('bar'))
    assert_multiline_match(output, r'''\nvalue: <test_inspect.test_listing_private_attributes.<locals>.Foo object at .*>\ntype: test_inspect.Foo\n\nPrivate attributes:\n  _name: str = 'bar'\n\n  def _private_method()\n''')


def test_backwards_wat_wat_import():
    from wat import wat
    assert wat.ret / 'foo' == 'foo'


def test_wat_return_output():
    result = wat.short.str / 'foo'
    assert_multiline_match(result, r'''\nvalue: 'foo'\ntype: str\nlen: 3\n''')


def test_colorful_output():
    try:
        os.environ['WAT_COLOR'] = 'false'
        output = inspect_format(None)
        assert output == """value: None\ntype: NoneType"""

        os.environ['WAT_COLOR'] = 'true'
        output = inspect_format(None)
        assert output == """\x1b[1;34mvalue:\x1b[0m \x1b[0;35mNone\x1b[0m\n\x1b[1;34mtype:\x1b[0m \x1b[0;33mNoneType\x1b[0m"""
    finally:
        os.environ['WAT_COLOR'] = ''


def test_inspect_overriden_len():
    class Foo:
        def __len__(self):
            return 4

    output = inspect_format(Foo())
    assert_multiline_match(output, r'''\nvalue: <test_inspect.test_inspect_overriden_len.<locals>.Foo object at .*>\ntype: test_inspect.Foo\nlen: 4\n''')


def test_catch_len_on_str_type():
    output = (wat.str.short / str).splitlines()
    assert "value: <class 'str'>" in output
    assert "type: type" in output
    assert "signature: class str(…)" in output


def test_retrieve_caller_info_type():
    output = wat.caller.short.str / math.sqrt(2+2)
    assert_multiline_match(output, r'''\nvalue: 2.0\ntype: float\ncaller expression: output = wat.caller.short.str / math.sqrt(2+2)\ncaller file: .*/tests/inspection/test_inspect.py:\d+\n''')