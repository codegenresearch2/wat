from datetime import datetime
from enum import Enum
import os
import re

from pydantic import BaseModel

import wat
from wat.inspection.inspection import inspect_format
from tests.asserts import assert_multiline_match, strip_ansi_colors, StdoutCap

def main():
    test_inspect_primitive_var()
    test_inspect_instance()
    test_inspect_function()
    test_inspect_nested_dict()
    test_inspect_datetime_repr()
    test_inspect_long()
    test_inspect_source_code()
    test_inspect_async_def()
    test_wat_with_nothing()
    test_wat_locals()
    test_wat_globals()
    test_wat_with_object()
    test_wat_with_short_long_modifiers()
    test_wat_with_multiple_modifiers()
    test_wat_modifiers_all_but_nodocs()
    test_list_parent_classes()
    test_list_deep_mro_classes()
    test_pydantic_class()
    test_returning_inspected_object()
    test_listing_private_attributes()
    test_backwards_wat_wat_import()
    test_wat_return_output()
    test_colorful_output()
    test_inspect_overriden_len()

def test_inspect_primitive_var():
    # Test code for inspecting primitive variables
    pass

def test_inspect_instance():
    # Test code for inspecting instances
    pass

def test_inspect_function():
    # Test code for inspecting functions
    pass

def test_inspect_nested_dict():
    # Test code for inspecting nested dictionaries
    pass

def test_inspect_datetime_repr():
    # Test code for inspecting datetime representation
    pass

def test_inspect_long():
    # Test code for inspecting long output
    pass

def test_inspect_source_code():
    # Test code for inspecting source code
    pass

def test_inspect_async_def():
    # Test code for inspecting async def
    pass

def test_wat_with_nothing():
    # Test code for using wat with nothing
    pass

def test_wat_locals():
    # Test code for using wat with locals
    pass

def test_wat_globals():
    # Test code for using wat with globals
    pass

def test_wat_with_object():
    # Test code for using wat with an object
    pass

def test_wat_with_short_long_modifiers():
    # Test code for using wat with short and long modifiers
    pass

def test_wat_with_multiple_modifiers():
    # Test code for using wat with multiple modifiers
    pass

def test_wat_modifiers_all_but_nodocs():
    # Test code for using wat with all modifiers except nodocs
    pass

def test_list_parent_classes():
    # Test code for listing parent classes
    pass

def test_list_deep_mro_classes():
    # Test code for listing deep MRO classes
    pass

def test_pydantic_class():
    # Test code for using pydantic class
    pass

def test_returning_inspected_object():
    # Test code for returning the inspected object
    pass

def test_listing_private_attributes():
    # Test code for listing private attributes
    pass

def test_backwards_wat_wat_import():
    # Test code for backwards wat import
    pass

def test_wat_return_output():
    # Test code for returning the output of wat
    pass

def test_colorful_output():
    # Test code for colorful output
    pass

def test_inspect_overriden_len():
    # Test code for inspecting overriden len
    pass

if __name__ == '__main__':
    main()