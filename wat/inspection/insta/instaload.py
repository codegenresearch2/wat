import base64
import zlib
import sys

# Read the code argument from the command line
code_arg = sys.argv[1]

# Decode the base64 encoded code
b64_code = code_arg.encode()
compressed_code = base64.b64decode(b64_code)
decompressed_code = zlib.decompress(compressed_code).decode()

# Execute the decompressed code
exec(decompressed_code, globals())