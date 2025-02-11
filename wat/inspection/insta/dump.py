import base64
from pathlib import Path
import re
import sys
import zlib
from typing import List, Any, Dict, Optional, Type, Iterable


def dump_snippet(filename: str) -> str:
    text: str = Path(filename).read_text()
    lines: List[str] = text.splitlines()
    lines = [line for line in lines if line.strip()]  # remove empty lines
    
    # Compile the regex pattern for comments once
    comment_pattern = re.compile(r'  # (.+)$')
    lines = [comment_pattern.sub('', line) for line in lines]  # trim comments
    
    # Minify the code
    minified_text = '\n'.join([minify_code(line) for line in lines])
    
    # Write the minified text to a file in the current directory
    Path('.inspection_minified.py').write_text(minified_text)
    
    # Encode the minified text
    code: str = encode_text(minified_text)
    return code


def minify_code(text: str) -> str:
    """
    Minify the given code by removing comments, type hints, and unnecessary spaces.
    """
    # Remove type hints and spaces
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
    text = re.sub(r': Any,', ',')
    
    # Replace type assignments with direct assignments
    if ': bool = ' in text:
        text = text.replace(': bool = ', '=')
    if ': int = ' in text:
        text = text.replace(': int = ', '=')
    if ': List[str] = ' in text:
        text = text.replace(': List[str] = ', '=')
    if ': str, ' in text:
        text = text.replace(': str, ', ',')
    
    # Remove unnecessary spaces around operators and assignments
    text = re.sub(r'= ', '=', text)
    text = re.sub(r' \+', '+', text)
    text = re.sub(r' \*', '*', text)
    
    # Remove type hints if not in quotes
    if not text.endswith(': str'):
        text = text.replace(': str', '')
    
    return text


def encode_text(text: str) -> str:
    """
    Compress and encode the given text using base64.
    """
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


if __name__ == '__main__':
    print(dump_snippet(sys.argv[1]))