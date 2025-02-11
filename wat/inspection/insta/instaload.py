import base64
import zlib
import sys
from pathlib import Path

def dump_snippet(filename: str) -> str:
    text: str = Path(filename).read_text()
    lines = [line for line in text.splitlines() if line.strip()]  # remove empty lines
    lines = [re.sub(r'  # (.+)$', '', line) for line in lines]  # trim comments
    text = '\n'.join(lines)
    compressed = zlib.compress(text.encode())
    b64 = base64.b64encode(compressed).decode()
    return b64

def load_snippet(code: str):
    b64 = code.encode()
    compressed = base64.b64decode(b64)
    decompressed = zlib.decompress(compressed).decode()
    exec(decompressed, globals())

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(dump_snippet(sys.argv[1]))