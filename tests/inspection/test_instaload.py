import base64
import zlib
import io
import sys

from wat.inspection.insta.instaload import code
from tests.asserts import assert_multiline_match, StdoutCap

def test_load_instaload_snippet():
    compressed_and_encoded_snippet = code
    snippet = zlib.decompress(base64.b64decode(compressed_and_encoded_snippet)).decode()
    assert '\nwat = Wat()\n' in snippet
    
    exec(snippet, globals())
    with StdoutCap() as capture:
        wat.short / 'moo'
    assert_multiline_match(capture.output(), r'''
value: 'moo'
type: str
len: 3
''')