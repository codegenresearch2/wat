import base64
import zlib
import sys

def decode_text(code: str) -> str:
    b64: bytes = code.encode()
    compressed = base64.b64decode(b64)
    decompressed: bytes = zlib.decompress(compressed)
    return decompressed.decode()

def load_snippet(code: str):
    text: str = decode_text(code)
    exec(text, globals())

if __name__ == '__main__':
    code = sys.argv[1]
    print(load_snippet(code))