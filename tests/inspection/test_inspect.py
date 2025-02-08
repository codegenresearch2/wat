import re
from datetime import datetime
from enum import Enum

from pydantic import BaseModel

from wat import wat
from wat.inspection.inspection import inspect_format
from tests.asserts import assert_multiline_match, strip_ansi_colors, StdoutCap


def test_inspect_primitive_var():
    output = inspect_format(None)
    assert strip_ansi_colors(output) == "\n    value: None\n    type: NoneType\n    "

    output = inspect_format([5])
    assert strip_ansi_colors(output) == "\n    value: [5]\n    type: list\n    len: 1\n\n    Public attributes:...\n    "

    output = inspect_format([5], dunder=True)
    assert re.search(r'def __eq__', strip_ansi_colors(output))

    output = inspect_format('poo', short=True)
    assert_multiline_match(output, "\n    value: 'poo'\n    type: str\n    len: 3\n    ")


def test_inspect_instance():
    class Hero:
        """\n            A hero\n        """
        def __init__(self, name: str):
            self.a = name

        def shout(self, loudness: int) -> str:
            """Do something very very very very very very very very very very very very very very very very very stupid"""
            return self.a * loudness

    instance = Hero('batman')
    output = inspect_format(instance)
    assert_multiline_match(output, "\n    value: <test_inspect.test_inspect_instance.<locals>.Hero object at .*>\n    type: test_inspect.Hero\n\n    Public attributes:...\n    ")

    output = inspect_format(Hero)
    assert_multiline_match(output, "\n    value: <class 'test_inspect.Hero'>\n    type: type\n    signature: class Hero(name: str)\n    \"""A hero"""\n\n    Public attributes:...\n    """)


def test_inspect_function():
    def foo(a: int, b: str = 'bar') -> str:
        """\n            Do something\n            dumb\n        """
        return a * b

    output = inspect_format(foo)
    assert_multiline_match(output, "\n    value: <function test_inspect_function.<locals>.foo at .*>\n    type: function\n    signature: def foo(a: int, b: str = 'bar') -> str\n    \"""\n    Do something\n    dumb\n    """\n    """)


def test_inspect_nested_dict():
    output = inspect_format({
        'a': {
            'b': {
                'values': [2,5,3],
            },
            "empty_dict": {}, "empty_list": [],\n            40: None,\n            None: 42,\n        },\n    }, short=True)
    assert_multiline_match(output, "\n    value: {...}\n    type: dict\n    len: 1\n\n    Public attributes:...\n    """)


def test_inspect_datetime_repr():
    output = inspect_format(datetime(2023, 8, 1), short=True)
    assert_multiline_match(output, "\n    str: 2023-08-01 00:00:00\n    repr: datetime.datetime(2023, 8, 1, 0, 0)\n    type: datetime.datetime\n    parents: datetime.date\n    """)


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
    assert_multiline_match(output, "\n    value: <function test_inspect_async_def.<locals>.looper at .*>\n    type: function\n    signature: async def looper()\n    """)


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


global_var = 23


def test_wat_globals():
    with StdoutCap() as capture:
        wat.globals
    assert 'value: <wat.inspection.inspection.globals object' in capture.uncolor()
    assert 'global_var: int = 23' in capture.uncolor()


def test_wat_with_object():
    with StdoutCap() as capture:
        wat(short=True) / 'moo'
    assert_multiline_match(capture.output(), "\n    value: 'moo'\n    type: str\n    len: 3\n    """)

    with StdoutCap() as capture:
        wat('moo', short=True)
    assert_multiline_match(capture.output(), "\n    value: 'moo'\n    type: str\n    len: 3\n    """)


def test_wat_with_short_long_modifiers():
    with StdoutCap() as capture:
        wat.short('moo')
    assert_multiline_match(capture.output(), "\n    value: 'moo'\n    type: str\n    len: 3\n    """)

    with StdoutCap() as capture:
        wat.long / 'moo2'
    assert re.search(r'def capitalize', capture.output())


def test_wat_with_multiple_modifiers():
    with StdoutCap() as capture:
        wat.dunder.code / re.match

    assert 'Dunder attributes:' in capture.output()
    assert '  def __eq__' in capture.output()
    assert 'source code:' in capture.output()
    assert 'def match(pattern, string, flags=0):' in capture.output()


def test_wat_modifiers_all_but_nodocs():
    with StdoutCap() as capture:
        wat.all.short.nodocs / re.match
    assert_multiline_match(capture.output(), "\n    value: <function match at .*>\n    type: function\n    signature: def match(pattern, string, flags=0)\n    source code: ...\n    """)


def test_list_parent_classes():
    class Parent(str, Enum):
        FIRST = 'first'

    output = inspect_format(Parent.FIRST, short=True)
    assert_multiline_match(output, "\n    str: '(Parent.FIRST|first)'\n    repr: <Parent.FIRST: 'first'>\n    type: test_inspect.Parent\n    parents: str, enum.Enum\n    len: 5\n    """)


def test_list_deep_mro_classes():
    class Grand(object):
        pass

    class Father(Grand):
        pass

    class Son(Father):
        pass

    output = inspect_format(Son(), short=True)
    assert_multiline_match(output, "\n    value: <test_inspect.test_list_deep_mro_classes.<locals>.Son object at .*>\n    type: test_inspect.Son\n    parents: test_inspect.Father, test_inspect.Grand\n    """)


def test_pydantic_class():
    class Person(BaseModel):
        name: str

    output = inspect_format(Person(name='george'), short=True)
    assert_multiline_match(output, "\n    str: name='george'\n    repr: Person(name='george')\n    type: test_inspect.Person\n    parents: pydantic.main.BaseModel\n    """)
