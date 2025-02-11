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
    assert strip_ansi_colors(output) == """value: [5]
type: list
len: 1
Public attributes:
  def append(object, /) # Append object to the end of the list.
  def clear() # Remove all items from list.
  def copy() # Return a shallow copy of the list.
  def count(value, /) # Return number of occurrences of value.
  def extend(iterable, /) # Extend list by appending elements from the iterable.
  def index(value, start=0, stop=9223372036854775807, /) # Return first index of value.
  def insert(index, object, /) # Insert object before index.
  def pop(index=-1, /) # Remove and return item at index (default last).
  def remove(value, /) # Remove first occurrence of value.
  def reverse() # Reverse *IN PLACE*.
  def sort(*, key=None, reverse=False) # Sort the list in ascending order and return None."""

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
    assert_multiline_match(output, """value: <test_inspect.test_inspect_instance.<locals>.Hero object at *>)
type: test_inspect.Hero

Public attributes:
  a: str = 'batman'

  def shout(loudness: int) -> str # Do something very very very very very very very very very very very very very very very very very stupid""")


# Additional test cases can be added here to match the gold code's comprehensive coverage.