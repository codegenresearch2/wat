import base64
import zlib
import sys
from pathlib import Path
from typing import List
import re

def dump_snippet(filename: str) -> str:
    text: str = Path(filename).read_text()
    lines: List[str] = text.splitlines()
    lines = [line for line in lines if line.strip()]  # remove empty lines
    comment_pattern = re.compile(r'  # (.+)$')
    lines = [comment_pattern.sub('', line) for line in lines]  # trim comments
    text = '\n'.join(lines)
    code: str = encode_text(text)
    return code

def encode_text(text: str) -> str:
    compressed = zlib.compress(text.encode())
    b64: bytes = base64.b64encode(compressed)
    return b64.decode()

if __name__ == '__main__':
    print(dump_snippet(sys.argv[1]))

def load_snippet(code: str):
    text: str = decode_text(code)
    exec(text, globals())

def decode_text(code: str) -> str:
    b64: bytes = code.encode()
    compressed = base64.b64decode(b64)
    decompressed: bytes = zlib.decompress(compressed)
    return decompressed.decode()