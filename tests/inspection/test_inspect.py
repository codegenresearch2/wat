from datetime import datetime
from enum import Enum
import os
import re

from pydantic import BaseModel

from wat import wat
from wat.inspection.inspection import inspect_format
from tests.asserts import assert_multiline_match, strip_ansi_colors, StdoutCap

def test_inspect_primitive_var():
    output = inspect_format(None, caller=True)
    assert strip_ansi_colors(output) == """\nvalue: None\ntype: NoneType\n""".strip()

    output = inspect_format([5], caller=True)
    assert strip_ansi_colors(output) == """\nvalue: [\n    5,\n]\ntype: list\nlen: 1\n\nPublic attributes:\n  def append(object, /) # Append object to the end of the list.\n  def clear() # Remove all items from list.\n  def copy() # Return a shallow copy of the list.\n  def count(value, /) # Return number of occurrences of value.\n  def extend(iterable, /) # Extend list by appending elements from the iterable.\n  def index(value, start=0, stop=9223372036854775807, /) # Return first index of value.…\n  def insert(index, object, /) # Insert object before index.\n  def pop(index=-1, /) # Remove and return item at index (default last).…\n  def remove(value, /) # Remove first occurrence of value.…\n  def reverse() # Reverse *IN PLACE*.\n  def sort(*, key=None, reverse=False) # Sort the list in ascending order and return None.…\n\ncaller expression: [5]\ncaller file: test_inspect.py:123\n""".strip()

    output = inspect_format([5], dunder=True, caller=True)
    assert "def __eq__(value, /) # Return self==value." in strip_ansi_colors(output)

    output = inspect_format('poo', short=True, caller=True)
    assert_multiline_match(output, r'''\nvalue: 'poo'\ntype: str\nlen: 3\n\ncaller expression: 'poo'\ncaller file: test_inspect.py:123\n''')

# Rest of the code remains the same as it follows the rules provided.