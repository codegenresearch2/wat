from datetime import datetime
from enum import Enum
import re

from pydantic import BaseModel

from wat import wat
from wat.inspection.inspection import inspect_format
from tests.asserts import assert_multiline_match, strip_ansi_colors, StdoutCap


def test_inspect_primitive_var():
    output = inspect_format(None)
    assert strip_ansi_colors(output) == """
value: None
type: NoneType
"""

    output = inspect_format([5])
    assert_multiline_match(output, r"""
value: \[
    5,
\]
type: list
len: 1

Public attributes:
  def append\(object, /\): # Append object to the end of the list.
  def clear\(\): # Remove all items from list.
  def copy\(\): # Return a shallow copy of the list.
  def count\(value, /\): # Return number of occurrences of value.
  def extend\(iterable, /\): # Extend list by appending elements from the iterable.
  def index\(value, start=0, stop=9223372036854775807, /\): # Return first index of value.…
  def insert\(index, object, /\): # Insert object before index.
  def pop\(index=-1, /\): # Remove and return item at index (default last).…
  def remove\(value, /\): # Remove first occurrence of value.…
  def reverse\(\): # Reverse *IN PLACE*.
  def sort\(\*\*, key=None, reverse=False\): # Sort the list in ascending order and return None.…
""")

    output = inspect_format([5], dunder=True)
    assert "def __eq__(value, /) # Return self==value." in strip_ansi_colors(output)

    output = inspect_format('poo', short=True)
    assert_multiline_match(output, r"""
value: 'poo'
type: str
len: 3
""")


def test_inspect_instance():
    class Hero:
        """
        A hero
        """
        def __init__(self, name: str):
            self.a = name
        
        def shout(self, loudness: int) -> str:
            """Do something very very very very very very very very very very very very very very very very very stupid"""
            return self.a * loudness
    
    instance = Hero('batman')
    output = inspect_format(instance)
    assert_multiline_match(output, r"""
value: <test_inspect.test_inspect_instance.<locals>.Hero object at .*>
type: test_inspect.Hero

Public attributes:
  a: str = 'batman'

  def shout\(loudness: int\) -> str \# Do something very very very very very very very very very very very very very very very very very st…
""")
                           
    output = inspect_format(Hero)
    assert_multiline_match(output, r"""
value: <class 'test_inspect.test_inspect_instance.<locals>.Hero'>
type: type
signature: class Hero\(name: str\)
'A hero'

Public attributes:
  def shout\(self, loudness: int\) -> str \# Do something very very very very very very very very very very very very very very very very very st…
""")


def test_inspect_function():
    def foo(a: int, b: str = 'bar') -> str:
        """
        Do something
        dumb
        """
        return a * b
  
    output = inspect_format(foo)
    assert_multiline_match(output, r"""
value: <function test_inspect_function.<locals>.foo at .*>
type: function
signature: def foo\(a: int, b: str = 'bar'\) -> str
'Do something\ndumb'
""")


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
    assert_multiline_match(output, r"""
value: {
    'a': {
        'b': {
            'values': \[
                2,
                5,
                3,
            \],
        },
        'empty_dict': {},
        'empty_list': \[\],
        40: None,
        None: 42,
    },
}
type: dict
len: 1
""")


def test_inspect_datetime_repr():
    output = inspect_format(datetime(2023, 8, 1), short=True)
    assert_multiline_match(output, r"""
str: 2023-08-01 00:00:00
repr: datetime.datetime\(2023, 8, 1, 0, 0\)
type: datetime.datetime
parents: datetime.date
""")


def test_inspect_long():
    output = inspect_format(datetime, long=True, code=True)
    lines = output.splitlines()
    assert "value: <class 'datetime.datetime'>" in lines
    assert "type: type" in lines
    assert "signature: class datetime\(…\)" in lines
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
    assert "signature: class Sorcerer\(\)" in lines
    assert "source code:" in lines
    assert "    class Sorcerer:" in lines
    assert "            self.level += 1" in lines


def test_inspect_async_def():
    async def looper():
        pass
    output = inspect_format(looper, short=True)
    assert_multiline_match(output, r"""
value: <function test_inspect_async_def.<locals>.looper at .*>
type: function
signature: async def looper\(\)"