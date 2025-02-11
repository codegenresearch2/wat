import base64
import zlib
import io
import sys

from wat.inspection.insta.instaload import code
from tests.asserts import assert_multiline_match, StdoutCap

def test_load_instaload_snippet():
    compressed_snippet = base64.b64decode(code)
    snippet = zlib.decompress(compressed_snippet).decode()
    assert '\nwat = Wat()\n' in snippet
    
    exec(snippet, globals())
    captured_output = io.StringIO()
    sys.stdout = captured_output
    try:
        wat.short / 'moo'
    finally:
        sys.stdout = sys.__stdout__
    assert_multiline_match(captured_output.getvalue(), r'''
value: 'moo'
type: str
len: 3
''')