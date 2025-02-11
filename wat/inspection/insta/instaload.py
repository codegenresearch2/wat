import base64
import zlib
import sys

# Read the base64 encoded code argument from the command line
code_arg = sys.argv[1]

# Ensure the base64 string is properly padded
padding = len(code_arg) % 4
if padding != 0:
    code_arg += '=' * (4 - padding)

# Decode the base64 encoded string and execute the decompressed code
exec(zlib.decompress(base64.b64decode(code_arg.encode())).decode(), globals())