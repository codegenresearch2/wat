from datetime import datetime
from enum import Enum
import math
import os
import re

from pydantic import BaseModel

from wat import Wat
from wat.inspection.inspection import inspect_format
from tests.asserts import assert_multiline_match, strip_ansi_colors, StdoutCap

wat = Wat()

def test_inspect_primitive_var():
    output = inspect_format(None)
    assert strip_ansi_colors(output) == """\nvalue: None\ntype: NoneType\n""".strip()

    output = inspect_format([5])
    assert strip_ansi_colors(output) == """\nvalue: [\n    5,\n]\ntype: list\nlen: 1\n\nPublic attributes:\n  def append(object, /) # Append object to the end of the list.\n  def clear() # Remove all items from list.\n  def copy() # Return a shallow copy of the list.\n  def count(value, /) # Return number of occurrences of value.\n  def extend(iterable, /) # Extend list by appending elements from the iterable.\n  def index(value, start=0, stop=9223372036854775807, /) # Return first index of value.…\n  def insert(index, object, /) # Insert object before index.\n  def pop(index=-1, /) # Remove and return item at index (default last).…\n  def remove(value, /) # Remove first occurrence of value.…\n  def reverse() # Reverse *IN PLACE*.\n  def sort(*, key=None, reverse=False) # Sort the list in ascending order and return None.…\n""".strip()

    output = inspect_format([5], dunder=True)
    assert "def __eq__(value, /) # Return self==value." in strip_ansi_colors(output)

    output = inspect_format('poo', short=True)
    assert_multiline_match(output, r'''\nvalue: 'poo'\ntype: str\nlen: 3\n''')

def test_inspect_instance():
    class Hero:
        """\n        A hero\n        """
        def __init__(self, name: str):
            self.a = name

        def shout(self, loudness: int) -> str:
            """Do something very very very very very very very very very very very very very very very very very stupid"""
            return self.a * loudness

    instance = Hero('batman')
    output = inspect_format(instance)
    assert_multiline_match(output, r'''\nvalue: <test_inspect\.test_inspect_instance\.<locals>\.Hero object at .*>\ntype: test_inspect\.Hero\n\nPublic attributes:\n  a: str = 'batman'\n\n  def shout\(loudness: int\) -> str \# Do something very very very very very very very very very very very very very very very very very st…\n''')

    output = inspect_format(Hero)
    assert_multiline_match(output, r'''\nvalue: <class 'test_inspect\.test_inspect_instance\.<locals>\.Hero'>\ntype: type\nsignature: class Hero\(name: str\)\n"""A hero"""\n\nPublic attributes:\n  def shout\(self, loudness: int\) -> str \# Do something very very very very very very very very very very very very very very very very very st…\n''')

def test_inspect_function():
    def foo(a: int, b: str = 'bar') -> str:
        """\n        Do something\n        dumb\n        """
        return a * b

    output = inspect_format(foo)
    print(output)
    assert_multiline_match(output, r'''\nvalue: <function test_inspect_function\.<locals>\.foo at .*>\ntype: function\nsignature: def foo\(a: int, b: str = 'bar'\) -> str\n"""\nDo something\ndumb\n"""\n''')

def test_inspect_nested_dict():
    output = inspect_format({
        'a': {
            'b': {
                'values': [2,5,3],
            },
            "empty_dict": {},
            "empty_list": [],
            40: None,
            None: 42,
        },
    }, short=True)
    assert_multiline_match(output, r'''\nvalue: {\n    'a': {\n        'b': {\n            'values': \[\n                2,\n                5,\n                3,\n            \],\n        },\n        'empty_dict': {},\n        'empty_list': \[\],\n        40: None,\n        None: 42,\n    },\n}\ntype: dict\nlen: 1\n''')

def test_inspect_datetime_repr():
    output = inspect_format(datetime(2023, 8, 1), short=True)
    assert_multiline_match(output, r'''\nstr: 2023-08-01 00:00:00\nrepr: datetime.datetime\(2023, 8, 1, 0, 0\)\ntype: datetime.datetime\nparents: datetime\.date\n''')

def test_inspect_long():
    output = inspect_format(datetime, long=True, code=True)
    lines = output.splitlines()
    assert "value: <class 'datetime.datetime'>" in lines
    assert "type: type" in lines
    assert "signature: class datetime(…)" in lines
    assert "datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])" in lines

def test_inspect_source_code():
    class Sorcerer:
        def __init__(self):
            self.level = 1
        def level_up(self):
            self.level += 1

    output = inspect_format(Sorcerer, code=True)
    lines = output.splitlines()
    assert "value: <class 'test_inspect.test_inspect_source_code.<locals>.Sorcerer'>" in lines
    assert "type: type" in lines
    assert "signature: class Sorcerer()" in lines
    assert "source code:" in lines
    assert "    class Sorcerer:" in lines
    assert "            self.level += 1" in lines

def test_inspect_async_def():
    async def looper():
        pass
    output = inspect_format(looper, short=True)
    assert_multiline_match(output, r'''\nvalue: <function test_inspect_async_def.<locals>.looper at .*>\ntype: function\nsignature: async def looper\(\)\n''')

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
    assert_multiline_match(capture.stripped(), r'''\nvalue: <function match at .*>\ntype: function\nsignature: def match\(pattern, string, flags=0\)\ncaller expression: wat\.all\.short\.nodocs / re\.match\ncaller file: .*/tests/inspection/test_inspect.py:\d+\nsource code:\ndef match\(pattern, string, flags=0\):\n    """.*\n    .*"""\n    .*\n''')

def test_list_parent_classes():
    class Parent(str, Enum):
        FIRST = 'first'

    output = inspect_format(Parent.FIRST, short=True)
    assert_multiline_match(output, r'''\nstr: '(Parent\.FIRST|first)'\nrepr: <Parent\.FIRST: 'first'>\ntype: test_inspect\.Parent\nparents: str, enum\.Enum\nlen: 5\n''')

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
    assert_multiline_match(output, r'''\nstr: name='george'\nrepr: Person\(name='george'\)\ntype: test_inspect\.Person\nparents: pydantic\.main\.BaseModel\n''')

def test_returning_inspected_object():
    assert wat.short.ret / 'hello' == 'hello'

def test_listing_private_attributes():
    class Foo:
        def __init__(self, name: str):
            self._name = name

        def _private_method(self):
            pass

    output = inspect_format(Foo('bar'))
    assert_multiline_match(output, r'''\nvalue: <test_inspect\.test_listing_private_attributes\.<locals>\.Foo object at .*>\ntype: test_inspect\.Foo\n\nPrivate attributes:\n  _name: str = 'bar'\n\n  def _private_method\(\)\n''')

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
    assert_multiline_match(output, r'''\nvalue: <test_inspect\.test_inspect_overriden_len\.<locals>\.Foo object at .*>\ntype: test_inspect\.Foo\nlen: 4\n''')

def test_catch_len_on_str_type():
    output = (wat.str.short / str).splitlines()
    assert "value: <class 'str'>" in output
    assert "type: type" in output
    assert "signature: class str(…)" in output

def test_retrieve_caller_info_type():
    output = wat.caller.short.str / math.sqrt(2+2)
    assert_multiline_match(output, r'''\nvalue: 2.0\ntype: float\ncaller expression: output = wat\.caller\.short\.str / math\.sqrt\(2\+2\)\ncaller file: .*/tests/inspection/test_inspect.py:\d+\n''')