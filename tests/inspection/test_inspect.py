import datetime
from enum import Enum
import re

from pydantic import BaseModel

import wat
from wat.inspection.inspection import inspect_format
from tests.asserts import assert_multiline_match, strip_ansi_colors, StdoutCap

__all__ = ['test_inspect_primitive_var', 'test_inspect_instance', 'test_inspect_function', 'test_inspect_nested_dict',
           'test_inspect_datetime_repr', 'test_inspect_long', 'test_inspect_source_code', 'test_inspect_async_def',
           'test_wat_with_nothing', 'test_wat_locals', 'test_wat_globals', 'test_wat_with_object',
           'test_wat_with_short_long_modifiers', 'test_wat_with_multiple_modifiers', 'test_wat_modifiers_all_but_nodocs',
           'test_list_parent_classes', 'test_list_deep_mro_classes', 'test_pydantic_class']

# Rest of the code remains the same