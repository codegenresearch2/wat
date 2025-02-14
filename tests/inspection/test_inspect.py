from datetime import datetime
from enum import Enum
import re

from pydantic import BaseModel

from wat import wat
from wat.inspection.inspection import inspect_format
from tests.asserts import assert_multiline_match, strip_ansi_colors, StdoutCap


def test_inspect_primitive_var():
    output = inspect_format(None)
    assert strip_ansi_colors(output) == """\nvalue: None\ntype: NoneType\n"""

    output = inspect_format([5])
    assert strip_ansi_colors(output) == """\nvalue: [\n    5,\n]\ntype: list\nlen: 1\n\nPublic attributes:\n  def append(object, /) # Append object to the end of the list.\n  def clear() # Remove all items from list.\n  def copy() # Return a shallow copy of the list.\n  def count(value, /) # Return number of occurrences of value.\n  def extend(iterable, /) # Extend list by appending elements from the iterable.\n  def index(value, start=0, stop=9223372036854775807, /) # Return first index of value.…\n  def insert(index, object, /) # Insert object before index.\n  def pop(index=-1, /) # Remove and return item at index (default last).…\n  def remove(value, /) # Remove first occurrence of value.…\n  def reverse() # Reverse *IN PLACE*.\n  def sort(*, key=None, reverse=False) # Sort the list in ascending order and return None.…\n"""

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
    assert_multiline_match(output, r'''\nvalue: <function test_inspect_function.<locals>.foo at .*>\ntype: function\nsignature: def foo\(a: int, b: str = 'bar'\) -> str\n"""\nDo something\ndumb\n"""\n''')


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
    assert str(wat) == '<Wat Inspector object>'
    with StdoutCap() as capture:
        assert repr(wat) == ''
    assert 'Try wat / object or wat.modifiers / object to inspect an object. Modifiers are:' in capture.uncolor().splitlines()


def test_wat_locals():
    _local_var = 23
    with StdoutCap() as capture:
        wat()
    assert 'value: <wat.inspection.inspection.locals object' in capture.uncolor()
    assert '_local_var: int = 23' in capture.uncolor()

    with StdoutCap() as capture:
        wat.locals
    assert 'value: <wat.inspection.inspection.locals object' in capture.uncolor()
    assert '_local_var: int = 23' in capture.uncolor()


global_var = 23

def test_wat_globals():
    with StdoutCap() as capture:
        wat.globals
    assert 'value: <wat.inspection.inspection.globals object' in capture.uncolor()
    assert 'global_var: int = 23' in capture.uncolor()


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
    assert_multiline_match(capture.output(), r'''\nvalue: <function match at .*>\ntype: function\nsignature: def match\(pattern, string, flags=0\)\nsource code:\ndef match\(pattern, string, flags=0\):\n    """.*\n    .*"""\n    .*\n''')


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