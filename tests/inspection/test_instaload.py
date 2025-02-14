import base64
import zlib
import re
from typing import List

def decode_text(code: str) -> str:
    b64: bytes = code.encode()
    compressed = base64.b64decode(b64)
    decompressed: bytes = zlib.decompress(compressed)
    return decompressed.decode()

def minify_code(text: str) -> str:
    text = re.sub(r'\) -> \'Wat\':$', '):', text)
    text = re.sub(r'\) -> Union\[.+\]:$', '):', text)
    text = text.replace(': bool = ', '=')
    text = text.replace(': int = ', '=')
    text = text.replace(': List[str] = ', '=')
    text = text.replace(': str, ', ',')
    text = text.replace(': bool)', ')')
    text = text.replace(': int)', ')')
    text = text.replace(': InspectAttribute', '')
    text = text.replace(': InspectConfig', '')
    text = re.sub(r'\) -> str:$', '):', text)
    text = re.sub(r'\) -> bool:$', '):', text)
    text = re.sub(r'\) -> Optional\[.+\]:$', '):', text)
    text = re.sub(r'\) -> Dict\[.+\]:$', '):', text)
    text = re.sub(r'\) -> Iterable\[.+\]:$', '):', text)
    text = re.sub(r': Dict(\[.+\])?', '', text)
    text = re.sub(r': List(\[.+\])?', '', text)
    text = text.replace(': Type)', ')')
    if not text.endswith(': str'):
        text = text.replace(': str', '')
    if text.count(' = ') == 1:
        if not _is_in_quote(text, ' = '):
            text = text.replace(' = ', '=')
    return text

def encode_text(text: str) -> str:
    compressed = zlib.compress(text.encode())
    b64: bytes = base64.b64encode(compressed)
    return b64.decode()

def _is_in_quote(line: str, part: str) -> bool:
    index = line.index(part)
    before = line[:index]
    after = line[index + len(part):]
    before_quotes = before.count('"') + before.count("'")
    after_quotes = after.count('"') + after.count("'")
    return before_quotes % 2 == 1 and after_quotes % 2 == 1

import base64
import zlib
from wat.inspection.insta.instaload import code
from tests.asserts import assert_multiline_match, StdoutCap

def test_load_instaload_snippet():
    snippet = zlib.decompress(base64.b64decode(code)).decode()
    snippet = minify_code(snippet)
    assert '\nwat = Wat()\n' in snippet
    
    exec(snippet, globals())
    with StdoutCap() as capture:
        wat.short / 'moo'
    assert_multiline_match(capture.output(), r'''\nvalue: 'moo'\ntype: str\nlen: 3\n''')