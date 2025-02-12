import base64
from pathlib import Path
import re
import sys
import zlib
from typing import List, Union, Optional, Dict, Iterable, Type


def dump_snippet(filename: str) -> str:
    text: str = Path(filename).read_text()
    lines: List[str] = text.splitlines()
    lines = [line for line in lines if line.strip()]  # remove empty lines
    minified_lines = [minify_code(line) for line in lines]  # apply minification to each line
    minified_text = '\n'.join(minified_lines)  # join the minified lines

    # Write the minified text to a file with the correct path
    Path('.inspection_minified.py').write_text(minified_text)

    code: str = encode_text(minified_text)
    return code


def minify_code(text: str) -> str:
    """
    Minifies the given Python code by removing comments and unnecessary whitespace.
    """
    # Remove comments
    text = re.sub(r'  # .+$', '', text)
    
    # Remove type hints and unnecessary spaces
    text = re.sub(r'\) -> \'Wat\':$', '):', text)
    text = re.sub(r'\) -> Union\[.+\]:$', '):', text)
    text = re.sub(r'\) -> str:$', '):', text)
    text = re.sub(r'\) -> bool:$', '):', text)
    text = re.sub(r'\) -> Optional\[.+\]:$', '):', text)
    text = re.sub(r'\) -> Dict\[.+\]:$', '):', text)
    text = re.sub(r'\) -> Iterable\[.+\]:$', '):', text)
    text = re.sub(r': Dict(\[.+\])?', '', text)
    text = re.sub(r': List(\[.+\])?', '', text)
    text = re.sub(r': Type)', ')')
    text = re.sub(r'= ', '=', text)
    text = re.sub(r', ', ',', text)
    text = re.sub(r' \(', '(', text)
    text = re.sub(r' \)', ')', text)
    text = re.sub(r' :', ':', text)
    if not text.endswith(': str'):
        text = re.sub(r': str$', '', text)
    
    return text


def encode_text(text: str) -> str:
    compressed = zlib.compress(text.encode())
    b64: bytes = base64.b64encode(compressed)
    return b64.decode()


if __name__ == '__main__':
    print(dump_snippet(sys.argv[1]))