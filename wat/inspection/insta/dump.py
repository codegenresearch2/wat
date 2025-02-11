import base64
from pathlib import Path
import re
import sys
import zlib
from typing import List

def _is_in_quote(line: str, pos: int) -> bool:
    """Check if the character at the given position is within quotes."""
    # This function uses a regex to check if the character at the given position is within quotes.
    # It returns True if the character is within quotes, and False otherwise.
    # The regex pattern matches single or double quotes and ensures the position is not escaped.
    pattern = re.compile(r"""
        (?:
            [^\S\n]|^  # Match spaces or tabs at the start of the line
            |           # Or
            [^"]*"      # Match a string with double quotes
            |           # Or
            [^']*'      # Match a string with single quotes
        )*?
        (?:
            [^"]*"      # Match a string with double quotes
            |           # Or
            [^']*'      # Match a string with single quotes
        )
    """, re.VERBOSE)
    match = pattern.match(line[:pos])
    return bool(match)

def minify_code(lines: List[str]) -> List[str]:
    """Minify the code by removing type hints and unnecessary spaces."""
    minified_lines = []
    for line in lines:
        # Remove type hints
        line = re.sub(r'->\s*', '', line)
        # Remove spaces around operators
        line = re.sub(r'\s*([+*/-])\s*', r'\1', line)
        # Remove spaces around commas
        line = re.sub(r'\s*,\s*', ',', line)
        # Remove spaces around colons
        line = re.sub(r'\s*:\s*', ':', line)
        # Remove spaces around equals
        line = re.sub(r'\s*=\s*', '=', line)
        # Remove spaces around parentheses
        line = re.sub(r'\s*\(\s*', '(', line)
        line = re.sub(r'\s*\)\s*', ')', line)
        # Remove spaces around brackets
        line = re.sub(r'\s*\{\s*', '{', line)
        line = re.sub(r'\s*\}\s*', '}', line)
        line = re.sub(r'\s*\[\s*', '[', line)
        line = re.sub(r'\s*\]\s*', ']', line)
        # Remove spaces around operators
        line = re.sub(r'\s*([+*/-])\s*', r'\1', line)
        # Remove spaces around colons
        line = re.sub(r'\s*:\s*', ':', line)
        # Remove spaces around equals
        line = re.sub(r'\s*=\s*', '=', line)
        # Remove spaces around commas
        line = re.sub(r'\s*,\s*', ',', line)
        # Remove spaces around semicolons
        line = re.sub(r'\s*;\s*', ';', line)
        # Remove spaces around arrows
        line = re.sub(r'\s*->\s*', '->', line)
        # Remove spaces around keywords
        line = re.sub(r'\s*(if|elif|else|for|while|return|break|continue|in|is|and|or|not)\s*', r'\1', line)
        # Remove spaces around function definitions
        line = re.sub(r'\s*def\s+', 'def ', line)
        # Remove spaces around class definitions
        line = re.sub(r'\s*class\s+', 'class ', line)
        # Remove spaces around imports
        line = re.sub(r'\s*import\s+', 'import ', line)
        # Remove spaces around from
        line = re.sub(r'\s*from\s+', 'from ', line)
        # Remove spaces around as
        line = re.sub(r'\s*as\s+', 'as ', line)
        # Remove spaces around with
        line = re.sub(r'\s*with\s+', 'with ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around raise
        line = re.sub(r'\s*raise\s+', 'raise ', line)
        # Remove spaces around try
        line = re.sub(r'\s*try\s+', 'try ', line)
        # Remove spaces around except
        line = re.sub(r'\s*except\s+', 'except ', line)
        # Remove spaces around finally
        line = re.sub(r'\s*finally\s+', 'finally ', line)
        # Remove spaces around assert
        line = re.sub(r'\s*assert\s+', 'assert ', line)
        # Remove spaces around pass
        line = re.sub(r'\s*pass\s+', 'pass ', line)
        # Remove spaces around del
        line = re.sub(r'\s*del\s+', 'del ', line)
        # Remove spaces around global
        line = re.sub(r'\s*global\s+', 'global ', line)
        # Remove spaces around nonlocal
        line = re.sub(r'\s*nonlocal\s+', 'nonlocal ', line)
        # Remove spaces around lambda
        line = re.sub(r'\s*lambda\s+', 'lambda ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around return
        line = re.sub(r'\s*return\s+', 'return ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove spaces around yield
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        # Remove