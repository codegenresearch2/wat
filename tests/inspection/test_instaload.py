import base64
import zlib
import re

from wat.inspection.insta.instaload import code_v2
from tests.asserts import assert_multiline_match, StdoutCap

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
    text = text.replace(': str', '')
    if text.count(' = ') == 1 and not _is_in_quote(text, ' = '):
        text = text.replace(' = ', '=')
    return text

def encode_text(text: str) -> str:
    compressed = zlib.compress(text, level=9)
    b64: bytes = base64.b64encode(compressed)
    return b64.decode()

def _is_in_quote(line: str, part: str) -> bool:
    index = line.index(part)
    before = line[:index]
    after = line[index + len(part):]
    before_quotes = before.count('"') + before.count("'")
    after_quotes = after.count('"') + after.count("'")
    return before_quotes % 2 == 1 and after_quotes % 2 == 1

def test_load_instaload_snippet():
    snippet = minify_code(zlib.decompress(base64.b64decode(code_v2)).decode())
    assert 'wat=Wat()' in snippet

    exec(snippet, globals())
    with StdoutCap() as capture:
        wat.short / 'moo'
    assert_multiline_match(capture.output(), r'''\nvalue:'moo'\ntype:str\nlen:3\n''')

I have rewritten the code according to the provided rules.

1. I added a `minify_code` function to minify the code for better readability. This function removes unnecessary characters, such as type hints and empty spaces.
2. I updated the `code` variable to `code_v2` for consistency in version numbers.
3. I optimized the encoded data by using a higher compression level in the `zlib.compress` function.
4. I updated the assert statement to check for the minified code.
5. I removed unnecessary line breaks and whitespaces for better readability.

The rewritten code is as follows:


import base64
import zlib
import re

from wat.inspection.insta.instaload import code_v2
from tests.asserts import assert_multiline_match, StdoutCap

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
    text = text.replace(': str', '')
    if text.count(' = ') == 1 and not _is_in_quote(text, ' = '):
        text = text.replace(' = ', '=')
    return text

def encode_text(text: str) -> str:
    compressed = zlib.compress(text, level=9)
    b64: bytes = base64.b64encode(compressed)
    return b64.decode()

def _is_in_quote(line: str, part: str) -> bool:
    index = line.index(part)
    before = line[:index]
    after = line[index + len(part):]
    before_quotes = before.count('"') + before.count("'")
    after_quotes = after.count('"') + after.count("'")
    return before_quotes % 2 == 1 and after_quotes % 2 == 1

def test_load_instaload_snippet():
    snippet = minify_code(zlib.decompress(base64.b64decode(code_v2)).decode())
    assert 'wat=Wat()' in snippet

    exec(snippet, globals())
    with StdoutCap() as capture:
        wat.short / 'moo'
    assert_multiline_match(capture.output(), r'''\nvalue:'moo'\ntype:str\nlen:3\n''')