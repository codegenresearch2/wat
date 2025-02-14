from datetime import datetime
from enum import Enum
import re

from pydantic import BaseModel

from wat import wat
from wat.inspection.inspection import inspect_format
from tests.asserts import assert_multiline_match, strip_ansi_colors, StdoutCap


def test_inspect_primitive_var():
    output = inspect_format(None)
    assert strip_ansi_colors(output) == "value: None\ntype: NoneType"

    output = inspect_format([5])
    assert strip_ansi_colors(output) == "value: [\n    5,\n]\ntype: list\nlen: 1\n\nPublic attributes: def append(object, /) # Append object to the end of the list.\ndef clear() # Remove all items from list.\ndef copy() # Return a shallow copy of the list.\ndef count(value, /) # Return number of occurrences of value.\ndef extend(iterable, /) # Extend list by appending elements from the iterable.\ndef index(value, start=0, stop=9223372036854775807, /) # Return first index of value.…\ndef insert(index, object, /) # Insert object before index.\ndef pop(index=-1, /) # Remove and return item at index (default last).…\ndef remove(value, /) # Remove first occurrence of value.…\ndef reverse() # Reverse *IN PLACE*.\ndef sort(*, key=None, reverse=False) # Sort the list in ascending order and return None.…"

    output = inspect_format([5], dunder=True)
    assert "def __eq__(value, /) # Return self==value." in strip_ansi_colors(output)

    output = inspect_format('poo', short=True)
    assert_multiline_match(output, "value: 'poo'\ntype: str\nlen: 3\n")


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
    assert_multiline_match(output, "value: <test_inspect.test_inspect_instance.<locals>.Hero object at *>