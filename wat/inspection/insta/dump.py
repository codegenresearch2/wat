import base64
from pathlib import Path
import re
import zlib
import sys

def _is_in_quote(line: str, index: int) -> bool:
    """Helper function to check if a character is within quotes."""
    quotes = ['"', "'"]
    while index >= 0:
        if line[index] in quotes:
            return True
        index -= 1
    return False

def _remove_comments(line: str) -> str:
    """Remove comments from a single line of code."""
    comment_start = line.find('  # ')
    if comment_start != -1 and not _is_in_quote(line, comment_start):
        return line[:comment_start]
    return line

def minify_code(text: str) -> str:
    """Minify the given code by removing comments and unnecessary spaces."""
    lines = text.splitlines()
    lines = [line.strip() for line in lines if line.strip()]  # Remove empty lines and strip whitespace
    lines = [_remove_comments(line) for line in lines]
    
    # Remove type hints and other patterns
    pattern = re.compile(r'->\s*\w+|,\s*|\s*=\s*|\s*:\s*|\s*==\s*|\s*\+\s*|\s*\*\s*')
    minified_lines = [pattern.sub('', line) for line in lines]
    
    return '\n'.join(minified_lines)

def encode_text(text: str) -> str:
    """Compress and encode the given text using base64."""
    compressed = zlib.compress(text.encode())
    encoded = base64.b64encode(compressed).decode()
    return encoded

def dump_snippet(filename: str) -> str:
    """Read, minify, and encode the code snippet from the given file."""
    text = Path(filename).read_text()
    minified_text = minify_code(text)
    encoded_text = encode_text(minified_text)
    return encoded_text

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(dump_snippet(sys.argv[1]))
    else:
        print("Usage: python script.py <filename>")