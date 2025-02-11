import os
import re
from datetime import datetime
from enum import Enum
from pydantic import BaseModel
import wat
from wat.inspection.inspection import inspect_format
from tests.asserts import assert_multiline_match, strip_ansi_colors, StdoutCap

def test_inspect_primitive_var():
    output = inspect_format(None).strip()
    assert output == """value: None
type: NoneType""", f"Expected output: {repr('value: None\ntype: NoneType')}"

    output = inspect_format([5]).strip()
    expected_output = """value: [
    5,
]
type: list
len: 1

Public attributes:
  def append(object, /) # Append object to the end of the list.
  def clear() # Remove all items from list.
  def copy() # Return a shallow copy of the list.
  def count(value, /) # Return number of occurrences of value.
  def extend(iterable, /) # Extend list by appending elements from the iterable.
  def index(value, start=0, stop=9223372036854775807, /) # Return first index of value.…
  def insert(index, object, /) # Insert object before index.
  def pop(index=-1, /) # Remove and return item at index (default last).…
  def remove(value, /) # Remove first occurrence of value.…
  def reverse() # Reverse *IN PLACE*.
  def sort(*, key=None, reverse=False) # Sort the list in ascending order and return None.…"""
    assert strip_ansi_colors(output) == strip_ansi_colors(expected_output), f"Expected output: {repr(expected_output)}"

    output = inspect_format([5], dunder=True).strip()
    assert re.match(r"def __eq__\(value, /\) # Return self==value.", output), f"Expected output: {repr('def __eq__(value, /) # Return self==value.')}"

    output = inspect_format('poo', short=True).strip()
    assert output == """value: 'poo'
type: str
len: 3""", f"Expected output: {repr('value: \'poo\'\ntype: str\nlen: 3')}"

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
    output = inspect_format(instance).strip()
    expected_output = """value: <test_inspect.test_inspect_instance.<locals>.Hero object at .*>
type: test_inspect.Hero

Public attributes:
  a: str = 'batman'

  def shout\(loudness: int\) -> str # Do something very very very very very very very very very very very very very very very very very stupid"""
    assert strip_ansi_colors(output) == strip_ansi_colors(expected_output), f"Expected output: {repr(expected_output)}"

    output = inspect_format(Hero).strip()
    expected_output = """value: <class 'test_inspect.test_inspect_instance.<locals>.Hero'>
type: type
signature: class Hero\(name: str\)
"""A hero"""

Public attributes:
  def shout\(self, loudness: int\) -> str # Do something very very very very very very very very very very very very very very very very very stupid"""
    assert strip_ansi_colors(output) == strip_ansi_colors(expected_output), f"Expected output: {repr(expected_output)}"

def test_inspect_function():
    def foo(a: int, b: str = 'bar') -> str:
        """
        Do something
        dumb
        """
        return a * b
  
    output = inspect_format(foo).strip()
    expected_output = """value: <function test_inspect_function.<locals>.foo at .*>
type: function
signature: def foo\(a: int, b: str = 'bar'\) -> str
"""
Do something
dumb
"""
    assert strip_ansi_colors(output) == strip_ansi_colors(expected_output), f"Expected output: {repr(expected_output)}"

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
    }, short=True).strip()
    expected_output = """value: {
    'a': {
        'b': {
            'values': [
                2,
                5,
                3,
            ],
        },
        'empty_dict': {},
        'empty_list': [],
        40: None,
        None: 42,
    },
}
type: dict
len: 1"""
    assert strip_ansi_colors(output) == strip_ansi_colors(expected_output), f"Expected output: {repr(expected_output)}"

def test_inspect_datetime_repr():
    output = inspect_format(datetime(2023, 8, 1), short=True).strip()
    expected_output = """str: 2023-08-01 00:00:00
repr: datetime.datetime(2023, 8, 1, 0, 0)
type: datetime.datetime
parents: datetime.date"""
    assert strip_ansi_colors(output) == strip_ansi_colors(expected_output), f"Expected output: {repr(expected_output)}"

def test_inspect_long():
    output = inspect_format(datetime, long=True, code=True).strip()
    expected_output = """value: <class 'datetime.datetime'>
type: type
signature: class datetime(…)
datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])

Public attributes:
  def __new__(cls, year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]) # Create a new datetime object.
  def __init__(self, year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]) # Initialize datetime object.
  def __repr__(self) # Return the representation of the datetime object.
  def __str__(self) # Return the string representation of the datetime object.
  def __hash__(self) # Return hash(self).
  def __eq__(self, value) # Compare this datetime to another datetime.
  def __ne__(self, value) # Compare this datetime to another datetime.
  def __lt__(self, value) # Compare this datetime to another datetime.
  def __le__(self, value) # Compare this datetime to another datetime.
  def __gt__(self, value) # Compare this datetime to another datetime.
  def __ge__(self, value) # Compare this datetime to another datetime.
  def __add__(self, value) # Add a datetime and a timedelta.
  def __sub__(self, value) # Subtract a datetime from a datetime or a timedelta from a datetime.
  def __mul__(self, value) # Multiply a datetime by a number.
  def __truediv__(self, value) # Divide a datetime by a number.
  def __floordiv__(self, value) # Floor divide a datetime by a number.
  def __mod__(self, value) # Modulo a datetime by a number.
  def __divmod__(self, value) # Return the tuple (quotient, remainder) for integer division of a datetime by a number.
  def __round__(self, *args) # Round the datetime to the nearest second or timedelta.
  def __ceil__(self) # Return the smallest datetime greater than or equal to the datetime.
  def __floor__(self) # Return the largest datetime less than or equal to the datetime.
  def __abs__(self) # Return the absolute value of the datetime.
  def __sizeof__(self) # Return the size of the datetime object in bytes.
  def __format__(self, format_spec) # Format the datetime object according to the format_spec.
  def astimezone(self, tz) # Convert the datetime to another timezone.
  def combine(self, date, time) # Combine a date and a time into a datetime.
  def ctime() # Return the time formatted as a string.
  def date() # Return the date part of the datetime.
  def day_name(self) # Return the name of the day of the week.
  def dst(self) # Return the daylight saving time (DST) adjustment, if any.
  def fromisocalendar(year, week, day) # Return a datetime from the ISO calendar date.
  def isocalendar(self) # Return the ISO calendar date as a named tuple.
  def isoformat(self, timespec='auto') # Return the ISO 8601 formatted string.
  def isoweekday(self) # Return the day of the week as an integer (Monday is 1, Sunday is 7).
  def max(self) # Return the maximum datetime.
  def min(self) # Return the minimum datetime.
  def replace(self, year=None, month=None, day=None, hour=None, minute=None, second=None, microsecond=None, tzinfo=None) # Return a datetime with the specified fields replaced.
  def strftime(self, format) # Format the datetime object according to the format string.
  def time(self) # Return the time part of the datetime.
  def timestamp(self) # Return POSIX timestamp as float.
  def timetuple(self) # Return the time tuple.
  def to_pydatetime(self) # Return the datetime as a native Python datetime object.
  def toordinal(self) # Return the date's ordinal, where January 1, 1 is 1.
  def weekday(self) # Return the day of the week as an integer (Monday is 0, Sunday is 6).
  def year_name(self) # Return the name of the year.
"""
    assert strip_ansi_colors(output) == strip_ansi_colors(expected_output), f"Expected output: {repr(expected_output)}"

def test_inspect_source_code():
    class Sorcerer:
        def __init__(self):
            self.level = 1
        def level_up(self):
            self.level += 1

    output = inspect_format(Sorcerer, code=True).strip()
    expected_output = """value: <class 'test_inspect.test_inspect_source_code.<locals>.Sorcerer'>
type: type
signature: class Sorcerer()
source code:
    class Sorcerer:
        def __init__(self):
            self.level = 1
        def level_up(self):
            self.level += 1
"""
    assert strip_ansi_colors(output) == strip_ansi_colors(expected_output), f"Expected output: {repr(expected_output)}"

def test_inspect_async_def():
    async def looper():
        pass
    output = inspect_format(looper, short=True).strip()
    expected_output = """value: <function test_inspect_async_def.<locals>.looper at .*>
type: function
signature: async def looper()"""
    assert strip_ansi_colors(output) == strip_ansi_colors(expected_output), f"Expected output: {repr(expected_output)}"

def test_wat_with_nothing():
    assert str(wat) == '<WAT Inspector object>'
    with StdoutCap() as capture:
        assert repr(wat) == ''
    assert 'Try wat / object or wat.modifiers / object to inspect an object. Modifiers are:' in capture.uncolor().strip()

def test_wat_locals():
    _local_var = 23
    output = wat.str.gray.locals.strip().splitlines()
    expected_output = """Local variables:
  _local_var: int = 23"""
    assert output == expected_output, f"Expected output: {repr(expected_output)}"

    with StdoutCap() as capture:
        wat()
    assert 'Local variables' in capture.uncolor().strip()
    assert '  _local_var: int = 23' in capture.uncolor().strip()

def test_wat_globals():
    global_var = 23
    output = wat.str.gray.globals.strip().splitlines()
    expected_output = """Global variables:
  global_var: int = 23
  __name__: str = 'test_inspect'"""
    assert output == expected_output, f"Expected output: {repr(expected_output)}"

def test_wat_with_object():
    with StdoutCap() as capture:
        wat(short=True) / 'moo'
    assert_multiline_match(capture.output().strip(), r'''
value: 'moo'
type: str
len: 3
''')

    with StdoutCap() as capture:
        wat('moo', short=True)
    assert_multiline_match(capture.output().strip(), r'''
value: 'moo'
type: str
len: 3
''')

def test_wat_with_short_long_modifiers():
    with StdoutCap() as capture:
        wat.short('moo')
    assert_multiline_match(capture.output().strip(), r'''
value: 'moo'
type: str
len: 3
''')

    with StdoutCap() as capture:
        wat.long / 'moo2'
    assert re.match(r'""".*"""', capture.output().strip(), re.DOTALL)

def test_wat_with_multiple_modifiers():
    with StdoutCap() as capture:
        wat.dunder.code / re.match

    assert 'Dunder attributes:' in capture.output().strip()
    assert '  def __eq__(value, /)' in capture.output().strip()
    
    assert 'source code:' in capture.output().strip()
    assert re.match(r'def match\(pattern, string, flags=0\).*"""', capture.output().strip(), re.DOTALL)
    
    with StdoutCap() as capture:
        wat.all.short.nodocs / re.match
    assert_multiline_match(capture.stripped().strip(), r'''
value: <function match at .*>
type: function
signature: def match(pattern, string, flags=0)
caller expression: wat.all.short.nodocs / re.match
caller file: .*/tests/inspection/test_inspect.py:\d+
source code:
def match(pattern, string, flags=0):
    """.*"""
    .*
''')

def test_list_parent_classes():
    class Parent(str, Enum):
        FIRST = 'first'

    output = inspect_format(Parent.FIRST, short=True).strip()
    expected_output = """str: '(Parent.FIRST|first)'
repr: <Parent.FIRST: 'first'>
type: test_inspect.Parent
parents: str, enum.Enum
len: 5"""
    assert strip_ansi_colors(output) == strip_ansi_colors(expected_output), f"Expected output: {repr(expected_output)}"
    
    class Grand(object):
        pass

    class Father(Grand):
        pass

    class Son(Father):
        pass

    output = inspect_format(Son(), short=True).strip()
    expected_output = """value: <test_inspect.test_list_deep_mro_classes.<locals>.Son object at .*>
type: test_inspect.Son
parents: test_inspect.Father, test_inspect.Grand"""
    assert strip_ansi_colors(output) == strip_ansi_colors(expected_output), f"Expected output: {repr(expected_output)}"

def test_pydantic_class():
    class Person(BaseModel):
        name: str

    output = inspect_format(Person(name='george'), short=True).strip()
    expected_output = """str: name='george'
repr: Person(name='george')
type: test_inspect.Person
parents: pydantic.main.BaseModel"""
    assert strip_ansi_colors(output) == strip_ansi_colors(expected_output), f"Expected output: {repr(expected_output)}"

def test_returning_inspected_object():
    assert wat.short.ret / 'hello' == 'hello'

def test_listing_private_attributes():
    class Foo:
        def __init__(self, name: str):
            self._name = name
        
        def _private_method(self):
            pass
    
    output = inspect_format(Foo('bar')).strip()
    expected_output = """value: <test_inspect.test_listing_private_attributes.<locals>.Foo object at .*>
type: test_inspect.Foo

Private attributes:
  _name: str = 'bar'

  def _private_method()"""
    assert strip_ansi_colors(output) == strip_ansi_colors(expected_output), f"Expected output: {repr(expected_output)}"

def test_backwards_wat_wat_import():
    from wat import wat
    assert wat.ret / 'foo' == 'foo'

def test_wat_return_output():
    result = wat.short.str / 'foo'
    expected_output = """value: 'foo'
type: str
len: 3"""
    assert strip_ansi_colors(result) == strip_ansi_colors(expected_output), f"Expected output: {repr(expected_output)}"

def test_colorful_output():
    try:
        os.environ['WAT_COLOR'] = 'false'
        output = inspect_format(None).strip()
        assert output == """value: None
type: NoneType"""

        os.environ['WAT_COLOR'] = 'true'
        output = inspect_format(None).strip()
        assert output == """\x1b[1;34mvalue:\x1b[0m \x1b[0;35mNone\x1b[0m
\x1b[1;34mtype:\x1b[0m \x1b[0;33mNoneType\x1b[0m"""
    finally:
        os.environ['WAT_COLOR'] = ''

def test_inspect_overriden_len():
    class Foo:
        def __len__(self):
            return 4

    output = inspect_format(Foo()).strip()
    expected_output = """value: <test_inspect.test_inspect_overriden_len.<locals>.Foo object at .*>
type: test_inspect.Foo
len: 4"""
    assert strip_ansi_colors(output) == strip_ansi_colors(expected_output), f"Expected output: {repr(expected_output)}"

def test_catch_len_on_str_type():
    output = (wat.str.short / str).strip().splitlines()
    expected_output = """value: <class 'str'>
type: type
signature: class str(…)"""
    assert strip_ansi_colors(output) == strip_ansi_colors(expected_output), f"Expected output: {repr(expected_output)}"

def test_retrieve_caller_info_type():
    output = wat.caller.short.str / math.sqrt(2+2)
    expected_output = """value: 2.0
type: float
caller expression: output = wat.caller.short.str / math.sqrt(2+2)
caller file: .*/tests/inspection/test_inspect.py:\d+"""
    assert strip_ansi_colors(output) == strip_ansi_colors(expected_output), f"Expected output: {repr(expected_output)}"