from datetime import datetime
from enum import Enum
import os
import re

from pydantic import BaseModel

import wat
from wat.inspection.inspection import inspect_format
from tests.asserts import assert_multiline_match, strip_ansi_colors, StdoutCap

def main():
    def test_inspect_primitive_var():
        output = inspect_format(None)
        assert strip_ansi_colors(output) == """\n        value: None\n        type: NoneType\n        """.strip()

        # ... rest of the function ...

    def test_inspect_instance():
        # ... rest of the function ...

    # ... rest of the functions ...

    def test_colorful_output():
        try:
            os.environ['WAT_COLOR'] = 'false'
            output = inspect_format(None)
            assert output == """value: None\n            type: NoneType"""

            os.environ['WAT_COLOR'] = 'true'
            output = inspect_format(None)
            assert output == """\x1b[1;34mvalue:\x1b[0m \x1b[0;35mNone\x1b[0m\n            \x1b[1;34mtype:\x1b[0m \x1b[0;33mNoneType\x1b[0m"""
        finally:
            os.environ['WAT_COLOR'] = ''

    def test_inspect_overriden_len():
        class Foo:
            def __len__(self):
                return 4

        output = inspect_format(Foo())
        assert_multiline_match(output, r'''\n        value: <test_inspect\.test_inspect_overriden_len\.<locals>\.Foo object at .*>\n        type: test_inspect\.Foo\n        len: 4\n        ''')

    # Check for updates after processing files
    # No specific update check provided in the original code

if __name__ == '__main__':
    main()