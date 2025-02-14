from datetime import datetime
from enum import Enum
import math
import os
import re

from pydantic import BaseModel

from wat import wat
from wat.inspection.inspection import inspect_format, _caller_stack_frame, _strip_color, _color_enabled
from tests.asserts import assert_multiline_match, strip_ansi_colors, StdoutCap

def test_inspect_primitive_var():
    frame = _caller_stack_frame(1)
    frameinfo = inspect.getframeinfo(frame)
    caller_info = f'caller file: {frameinfo.filename}:{frameinfo.lineno}\ncaller expression: {frameinfo.code_context[0].strip()}' if frameinfo.filename else ''

    output = inspect_format(None)
    assert _strip_color(output) == f"""\n{caller_info}\nvalue: None\ntype: NoneType\n""".strip()

    output = inspect_format([5])
    assert _strip_color(output) == f"""\n{caller_info}\nvalue: [\n    5,\n]\ntype: list\nlen: 1\n\nPublic attributes:\n  def append(object, /) # Append object to the end of the list.\n  def clear() # Remove all items from list.\n  def copy() # Return a shallow copy of the list.\n  def count(value, /) # Return number of occurrences of value.\n  def extend(iterable, /) # Extend list by appending elements from the iterable.\n  def index(value, start=0, stop=9223372036854775807, /) # Return first index of value.…\n  def insert(index, object, /) # Insert object before index.\n  def pop(index=-1, /) # Remove and return item at index (default last).…\n  def remove(value, /) # Remove first occurrence of value.…\n  def reverse() # Reverse *IN PLACE*.\n  def sort(*, key=None, reverse=False) # Sort the list in ascending order and return None.…\n""".strip()

    output = inspect_format([5], dunder=True)
    assert "def __eq__(value, /) # Return self==value." in _strip_color(output)

    output = inspect_format('poo', short=True)
    assert_multiline_match(output, r'''\n{caller_info}\nvalue: 'poo'\ntype: str\nlen: 3\n''')

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
    assert_multiline_match(output, r'''\ncaller file: .*/tests/inspection/test_inspect.py:\d+\ncaller expression: instance = Hero\('batman'\)\nvalue: <test_inspect\.test_inspect_instance\.<locals>\.Hero object at .*>\ntype: test_inspect\.Hero\n\nPublic attributes:\n  a: str = 'batman'\n\n  def shout\(loudness: int\) -> str \# Do something very very very very very very very very very very very very very very very very very st…\n''')

    output = inspect_format(Hero)
    assert_multiline_match(output, r'''\ncaller file: .*/tests/inspection/test_inspect.py:\d+\ncaller expression: output = inspect_format\(Hero\)\nvalue: <class 'test_inspect\.test_inspect_instance\.<locals>\.Hero'>\ntype: type\nsignature: class Hero\(name: str\)\n"""A hero"""\n\nPublic attributes:\n  def shout\(self, loudness: int\) -> str \# Do something very very very very very very very very very very very very very very very very very st…\n''')

def test_inspect_function():
    def foo(a: int, b: str = 'bar') -> str:
        """\n        Do something\n        dumb\n        """
        return a * b

    output = inspect_format(foo)
    print(output)
    assert_multiline_match(output, r'''\ncaller file: .*/tests/inspection/test_inspect.py:\d+\ncaller expression: output = inspect_format\(foo\)\nvalue: <function test_inspect_function\.<locals>\.foo at .*>\ntype: function\nsignature: def foo\(a: int, b: str = 'bar'\) -> str\n"""\nDo something\ndumb\n"""\n''')

# Rest of the code remains the same as it is already following the rules provided.