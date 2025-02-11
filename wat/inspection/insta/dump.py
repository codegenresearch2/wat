import base64
from pathlib import Path
import re
import sys
import zlib

def dump_snippet(filename: str) -> str:
    """Minify the code by removing type hints and unnecessary spaces."""
    text: str = Path(filename).read_text()
    lines = text.splitlines()
    lines = [line for line in lines if line.strip()]  # Remove empty lines

    # Remove comments
    pattern = re.compile(r'#.*')
    lines = [pattern.sub('', line) for line in lines]

    # Remove type hints
    pattern = re.compile(r'->\s*')
    lines = [pattern.sub('', line) for line in lines]

    # Remove spaces around operators
    pattern = re.compile(r'\s*([+*/-])\s*')
    lines = [pattern.sub(r'\1', line) for line in lines]

    # Remove spaces around commas
    pattern = re.compile(r'\s*,\s*')
    lines = [pattern.sub(',', line) for line in lines]

    # Remove spaces around colons
    pattern = re.compile(r'\s*:\s*')
    lines = [pattern.sub(':', line) for line in lines]

    # Remove spaces around equals
    pattern = re.compile(r'\s*=\s*')
    lines = [pattern.sub('=', line) for line in lines]

    # Remove spaces around parentheses
    pattern = re.compile(r'\s*\(\s*')
    lines = [pattern.sub('(', line) for line in lines]
    pattern = re.compile(r'\s*\)\s*')
    lines = [pattern.sub(')', line) for line in lines]

    # Remove spaces around brackets
    pattern = re.compile(r'\s*\{\s*')
    lines = [pattern.sub('{', line) for line in lines]
    pattern = re.compile(r'\s*\}\s*')
    lines = [pattern.sub('}', line) for line in lines]
    pattern = re.compile(r'\s*\[\s*')
    lines = [pattern.sub('[', line) for line in lines]
    pattern = re.compile(r'\s*\]\s*')
    lines = [pattern.sub(']', line) for line in lines]

    # Remove spaces around operators
    pattern = re.compile(r'\s*([+*/-])\s*')
    lines = [pattern.sub(r'\1', line) for line in lines]

    # Remove spaces around colons
    pattern = re.compile(r'\s*:\s*')
    lines = [pattern.sub(':', line) for line in lines]

    # Remove spaces around equals
    pattern = re.compile(r'\s*=\s*')
    lines = [pattern.sub('=', line) for line in lines]

    # Remove spaces around commas
    pattern = re.compile(r'\s*,\s*')
    lines = [pattern.sub(',', line) for line in lines]

    # Remove spaces around semicolons
    pattern = re.compile(r'\s*;\s*')
    lines = [pattern.sub(';', line) for line in lines]

    # Remove spaces around arrows
    pattern = re.compile(r'\s*->\s*')
    lines = [pattern.sub('->', line) for line in lines]

    # Remove spaces around keywords
    pattern = re.compile(r'\s*(if|elif|else|for|while|return|break|continue|in|is|and|or|not)\s*')
    lines = [pattern.sub(r'\1', line) for line in lines]

    # Remove spaces around function definitions
    pattern = re.compile(r'\s*def\s+')
    lines = [pattern.sub('def ', line) for line in lines]

    # Remove spaces around class definitions
    pattern = re.compile(r'\s*class\s+')
    lines = [pattern.sub('class ', line) for line in lines]

    # Remove spaces around imports
    pattern = re.compile(r'\s*import\s+')
    lines = [pattern.sub('import ', line) for line in lines]

    # Remove spaces around from
    pattern = re.compile(r'\s*from\s+')
    lines = [pattern.sub('from ', line) for line in lines]

    # Remove spaces around as
    pattern = re.compile(r'\s*as\s+')
    lines = [pattern.sub('as ', line) for line in lines]

    # Remove spaces around with
    pattern = re.compile(r'\s*with\s+')
    lines = [pattern.sub('with ', line) for line in lines]

    # Remove spaces around yield
    pattern = re.compile(r'\s*yield\s+')
    lines = [pattern.sub('yield ', line) for line in lines]

    # Remove spaces around raise
    pattern = re.compile(r'\s*raise\s+')
    lines = [pattern.sub('raise ', line) for line in lines]

    # Remove spaces around try
    pattern = re.compile(r'\s*try\s+')
    lines = [pattern.sub('try ', line) for line in lines]

    # Remove spaces around except
    pattern = re.compile(r'\s*except\s+')
    lines = [pattern.sub('except ', line) for line in lines]

    # Remove spaces around finally
    pattern = re.compile(r'\s*finally\s+')
    lines = [pattern.sub('finally ', line) for line in lines]

    # Remove spaces around assert
    pattern = re.compile(r'\s*assert\s+')
    lines = [pattern.sub('assert ', line) for line in lines]

    # Remove spaces around pass
    pattern = re.compile(r'\s*pass\s+')
    lines = [pattern.sub('pass ', line) for line in lines]

    # Remove spaces around del
    pattern = re.compile(r'\s*del\s+')
    lines = [pattern.sub('del ', line) for line in lines]

    # Remove spaces around global
    pattern = re.compile(r'\s*global\s+')
    lines = [pattern.sub('global ', line) for line in lines]

    # Remove spaces around nonlocal
    pattern = re.compile(r'\s*nonlocal\s+')
    lines = [pattern.sub('nonlocal ', line) for line in lines]

    # Remove spaces around lambda
    pattern = re.compile(r'\s*lambda\s+')
    lines = [pattern.sub('lambda ', line) for line in lines]

    # Remove spaces around yield
    pattern = re.compile(r'\s*yield\s+')
    lines = [pattern.sub('yield ', line) for line in lines]

    # Remove spaces around return
    pattern = re.compile(r'\s*return\s+')
    lines = [pattern.sub('return ', line) for line in lines]

    # Join the lines back into a single string
    minified_code = '\n'.join(lines)

    # Compress and encode the text
    compressed = zlib.compress(minified_code.encode())
    encoded = base64.b64encode(compressed).decode()

    return encoded

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    encoded_text = dump_snippet(filename)
    print(encoded_text)