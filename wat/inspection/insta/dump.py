import base64
from pathlib import Path
import re
import zlib
from typing import List

def minify_code(text: str) -> str:
    # Remove comments
    pattern = re.compile(r'  # .+$')
    text = pattern.sub('', text)
    
    # Remove type hints
    pattern = re.compile(r'->\s*\w+')
    text = pattern.sub(lambda m: m.group(0).replace('->', '->'), text)
    
    # Remove spaces around commas
    pattern = re.compile(r'\s*,\s*')
    text = pattern.sub(',', text)
    
    # Remove spaces around equals
    pattern = re.compile(r'\s*=\s*')
    text = pattern.sub('=', text)
    
    # Remove spaces around colons
    pattern = re.compile(r'\s*:\s*')
    text = pattern.sub(':', text)
    
    # Remove spaces around double equals
    pattern = re.compile(r'\s*==\s*')
    text = pattern.sub('==', text)
    
    # Remove spaces around plus
    pattern = re.compile(r'\s*\+\s*')
    text = pattern.sub('+', text)
    
    # Remove spaces around asterisk
    pattern = re.compile(r'\s*\*\s*')
    text = pattern.sub('*', text)
    
    return text

def encode_text(text: str) -> str:
    compressed = zlib.compress(text.encode())
    encoded = base64.b64encode(compressed).decode()
    return encoded

def dump_snippet(filename: str) -> str:
    text = Path(filename).read_text()
    minified_text = minify_code(text)
    encoded_text = encode_text(minified_text)
    return encoded_text

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(dump_snippet(sys.argv[1]))
    else:
        print("Usage: python script.py <filename>")