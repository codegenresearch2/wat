import base64
from pathlib import Path
import re
import sys
import zlib
from typing import List


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
    Minify the given code by removing comments and unnecessary spaces.
    """
    # Remove type hints and spaces
    text = re.sub(r'\) -> \w+:$', '):', text)  # Remove type hints
    text = re.sub(r' -> \w+$', '', text)  # Remove return types
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    
    return text


def encode_text(text: str) -> str:
    """
    Compress and encode the given text using base64.
    """
    compressed = zlib.compress(text.encode())
    b64: bytes = base64.b64encode(compressed)
    return b64.decode()


if __name__ == '__main__':
    print(dump_snippet(sys.argv[1]))