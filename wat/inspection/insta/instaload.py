import base64
import zlib
import sys

def decode_and_exec(code: str):
    b64: bytes = code.encode()
    compressed = base64.b64decode(b64)
    decompressed = zlib.decompress(compressed).decode()
    exec(decompressed, globals())

if __name__ == '__main__':
    code = sys.argv[1]
    decode_and_exec(code)