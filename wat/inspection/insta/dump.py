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
    minified_lines = [re.sub(r'  # .+$', '', line) for line in lines]  # trim comments
    minified_lines = [re.sub(r'->\s*\w+', '', line) for line in minified_lines]  # remove type hints
    minified_lines = [re.sub(r'\s*,\s*', ',', line) for line in minified_lines]  # remove spaces around commas
    minified_lines = [re.sub(r'\s*=\s*', '=', line) for line in minified_lines]  # remove spaces around equals
    minified_lines = [re.sub(r'\s*:\s*', ':', line) for line in minified_lines]  # remove spaces around colons
    minified_lines = [re.sub(r'\s*==\s*', '==', line) for line in minified_lines]  # remove spaces around double equals
    minified_lines = [re.sub(r'\s*\+\s*', '+', line) for line in minified_lines]  # remove spaces around plus
    minified_lines = [re.sub(r'\s*\*\s*', '*', line) for line in minified_lines]  # remove spaces around asterisk
    minified_text = '\n'.join(minified_lines)
    compressed = zlib.compress(minified_text.encode())
    encoded = base64.b64encode(compressed).decode()
    return encoded

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(dump_snippet(sys.argv[1]))
    else:
        print("Usage: python script.py <filename>")