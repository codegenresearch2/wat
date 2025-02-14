import os
import re
import sys
import inspect as std_inspect
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Type, Iterable, Union

# Add environment variable handling for tests
COLOR_ENABLED = os.environ.get('WAT_COLOR', 'true').lower() != 'false'

@dataclass
class InspectConfig:
    short: bool
    dunder: bool
    nodocs: bool
    long: bool
    code: bool

@dataclass
class InspectAttribute:
    name: str
    value: Any
    type: Type
    callable: bool
    dunder: bool
    private: bool
    signature: Optional[str]
    doc: Optional[str]

def inspect_format(obj: Any, **config) -> str:
    output: List[str] = []
    str_value = _format_value(obj)
    repr_value = repr(obj)
    output.extend(_format_value_and_type(str_value, repr_value, obj))
    output.extend(_format_length(obj))
    output.extend(_format_callable(obj))
    output.extend(_format_doc(obj, config.get('long', False)))
    output.extend(_format_source_code(obj, config.get('code', False)))
    output.extend(_format_attributes(obj, config))
    output = _add_color_bars(output)
    return _strip_color(output) if not COLOR_ENABLED else '\n'.join(output)

# Improve code readability with imports
from .formatters import (
    _format_value,
    _format_value_and_type,
    _format_length,
    _format_callable,
    _format_doc,
    _format_source_code,
    _format_attributes,
    _add_color_bars,
    _strip_color,
)

# Update compressed code for better performance
# ... (rest of the code remains the same)