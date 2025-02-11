import base64
from pathlib import Path
import re
import sys
import zlib
from typing import List


def get_snippet(filename: str) -> str:
    text: str = Path(filename).read_text()
    lines: List[str] = text.splitlines()
    lines = [line for line in lines if line.strip()]  # remove empty lines
    lines = [re.sub(r'  # (.+)$', '', line) for line in lines]  # trim comments
    lines = [minify_code(line) for line in lines]
    text = '\n'.join(lines)

    code: str = compress_and_encode(text)
    return code


def minify_code(text: str) -> str:
    text = re.sub(r'\) -> \'Wat\':$', '):', text)
    text = re.sub(r'\) -> Union\[.+\]:$', '):', text)
    if ': bool = ' in text:
        text = text.replace(': bool = ', '=')
    if ': int = ' in text:
        text = text.replace(': int = ', '=')
    if ': List[str] = ' in text:
        text = text.replace(': List[str] = ', '=')
    if ': str, ' in text:
        text = text.replace(': str, ', ',')
    if ': Any, ' in text:
        text = text.replace(': Any,', ',')
    if ': bool)' in text:
        text = text.replace(': bool)', ')')
    if ': int)' in text:
        text = text.replace(': int)', ')')
    if ': InspectAttribute' in text:
        text = text.replace(': InspectAttribute', '')
    if ': InspectConfig' in text:
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
    if text.count(' = ') == 1 and not _is_in_quote(text, ' = '):
        text = text.replace(' = ', '=')
    text = text.replace('from typing import Any, Dict, List, Optional, Type, Iterable, Union', 'from typing import Any, Optional, Type')
    return text


def compress_and_encode(text: str) -> str:
    compressed = zlib.compress(text.encode(), 9)
    b64: bytes = base64.b64encode(compressed)
    return b64.decode()


def _is_in_quote(line: str, part: str) -> bool:
    index = line.index(part)
    before = line[:index]
    after = line[index + len(part):]
    before_quotes = before.count('"') + before.count("'")
    after_quotes = after.count('"') + after.count("'")
    return before_quotes % 2 == 1 and after_quotes % 2 == 1


if __name__ == '__main__':
    print(get_snippet(sys.argv[1]))