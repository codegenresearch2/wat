import base64
import zlib
from datetime import datetime
from enum import Enum
import re

from pydantic import BaseModel

import wat
from wat.inspection.inspection import inspect_format
from tests.asserts import assert_multiline_match, strip_ansi_colors, StdoutCap


def test_inspect_primitive_var():
    output = inspect_format(None)
    assert strip_ansi_colors(output) == "value: None\ntype: NoneType\nlen: 0"

    output = inspect_format([5])
    assert strip_ansi_colors(output) == "value: [5]\ntype: list\nlen: 1\nPublic attributes: def append(object, /) # Append object to the end of the list.\ndef clear() # Remove all items from list.\ndef copy() # Return a shallow copy of the list.\ndef count(value, /) # Return number of occurrences of value.\ndef extend(iterable, /) # Extend list by appending elements from the iterable.\ndef index(value, start=0, stop=9223372036854775807, /) # Return first index of value.\ndef insert(index, object, /) # Insert object before index.\ndef pop(index=-1, /) # Remove and return item at index (default last).\ndef remove(value, /) # Remove first occurrence of value.\ndef reverse() # Reverse *IN PLACE*.\ndef sort(*, key=None, reverse=False) # Sort the list in ascending order and return None."

    output = inspect_format([5], dunder=True)
    assert re.search(r"def __eq__\(value, /\) # Return self==value.", strip_ansi_colors(output))

    output = inspect_format('poo', short=True)
    assert_multiline_match(output, r"value: 'poo'\ntype: str\nlen: 3")


def test_inspect_instance():
    class Hero:
        """A hero"""
        def __init__(self, name: str):
            self.a = name
        
        def shout(self, loudness: int) -> str:
            """Do something very very very very very very very very very very very very very very very very very stupid"""
            return self.a * loudness
    
    instance = Hero('batman')
    output = inspect_format(instance)
    assert_multiline_match(output, r"value: <test_inspect\.test_inspect_instance\.<locals>\.Hero object at \w+>\ntype: test_inspect\.Hero\n\nPublic attributes: a: str = 'batman'\n\n  def shout\(loudness: int\) -> str # Do something very very very very very very very very very very very very very very very very very stupid")
                           
    output = inspect_format(Hero)
    assert_multiline_match(output, r"value: <class 'test_inspect\.test_inspect_instance\.<locals>\.Hero'>\ntype: type\nsignature: class Hero\(name: str\)\n\"\"\"A hero\"\"\"\n\nPublic attributes: def shout\(self, loudness: int\) -> str # Do something very very very very very very very very very very very very very very very very very stupid")


def test_inspect_function():
    def foo(a: int, b: str = 'bar') -> str:
        """Do something\ndumb"""
        return a * b
  
    output = inspect_format(foo)
    assert_multiline_match(output, r"value: <function test_inspect_function\.<locals>\.foo at \w+>\ntype: function\nsignature: def foo\(a: int, b: str = 'bar'\) -> str\n\"\"\"\nDo something\ndumb\n\"\"\"")


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
    assert_multiline_match(output, r"value: {'a': {'b': {'values': [2, 5, 3]}, 'empty_dict': {}, 'empty_list': [], 40: None, None: 42}}\ntype: dict\nlen: 1")


def test_inspect_datetime_repr():
    output = inspect_format(datetime(2023, 8, 1), short=True)
    assert_multiline_match(output, r"str: 2023-08-01 00:00:00\nrepr: datetime.datetime\(2023, 8, 1, 0, 0\)