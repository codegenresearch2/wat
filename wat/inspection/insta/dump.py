import base64
from pathlib import Path
import re
import sys
import zlib
from typing import List

def _is_in_quote(line: str, index: int) -> bool:
    # Check if the character at the given index is within quotes
    quotes = ['"', "'"]
    inside_quotes = False
    for i, char in enumerate(line):
        if char in quotes:
            if i <= index < i + len(char):
                inside_quotes = not inside_quotes
            elif i == index:
                return inside_quotes
    return False

def minify_code(text: str) -> str:
    lines: List[str] = text.splitlines()
    minified_lines = []
    for line in lines:
        # Remove comments
        line = re.sub(r'  # .+$', '', line)
        
        # Remove type hints
        line = re.sub(r'->\s*\w+', '', line)
        line = re.sub(r':\s*\w+', '', line)
        
        # Remove unnecessary spaces
        line = re.sub(r'\s*,\s*', ',', line)
        line = re.sub(r'\s*=\s*', '=', line)
        line = re.sub(r'\s*:\s*', ':', line)
        line = re.sub(r'\s*==\s*', '==', line)
        line = re.sub(r'\s*\+\s*', '+', line)
        line = re.sub(r'\s*\*\s*', '*', line)
        
        # Remove spaces around operators
        line = re.sub(r'\s*,\s*', ',', line)
        line = re.sub(r'\s*=\s*', '=', line)
        line = re.sub(r'\s*:\s*', ':', line)
        line = re.sub(r'\s*==\s*', '==', line)
        line = re.sub(r'\s*\+\s*', '+', line)
        line = re.sub(r'\s*\*\s*', '*', line)
        
        # Remove spaces around parentheses
        line = re.sub(r'\s*\(\s*', '(', line)
        line = re.sub(r'\s*\)\s*', ')', line)
        
        # Remove spaces around brackets
        line = re.sub(r'\s*\{\s*', '{', line)
        line = re.sub(r'\s*\}\s*', '}', line)
        line = re.sub(r'\s*\[\s*', '[', line)
        line = re.sub(r'\s*\]\s*', ']', line)
        
        # Remove spaces around operators
        line = re.sub(r'\s*<\s*', '<', line)
        line = re.sub(r'\s*>\s*', '>', line)
        line = re.sub(r'\s*<=\s*', '<=', line)
        line = re.sub(r'\s*>=\s*', '>=', line)
        line = re.sub(r'\s*!=\s*', '!=', line)
        
        # Remove spaces around assignment operators
        line = re.sub(r'\s*=\s*=', line)
        
        # Remove spaces around logical operators
        line = re.sub(r'\s*&&\s*', '&&', line)
        line = re.sub(r'\s*\|\|\s*', '||', line)
        
        # Remove spaces around arithmetic operators
        line = re.sub(r'\s*-\s*', '-', line)
        
        # Remove spaces around bitwise operators
        line = re.sub(r'\s*&\s*', '&', line)
        line = re.sub(r'\s*|\s*', '|', line)
        line = re.sub(r'\s*^\s*', '^', line)
        
        # Remove spaces around unary operators
        line = re.sub(r'\s*\+\+\s*', '++', line)
        line = re.sub(r'\s*--\s*', '--', line)
        line = re.sub(r'\s*-\s*', '-', line)
        line = re.sub(r'\s*!\s*', '!', line)
        
        # Remove spaces around function call parentheses
        line = re.sub(r'\s*\(\s*', '(', line)
        line = re.sub(r'\s*\)\s*', ')', line)
        
        # Remove spaces around return statement
        line = re.sub(r'\s*return\s+', 'return ', line)
        
        # Remove spaces around yield statement
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        
        # Remove spaces around import statement
        line = re.sub(r'\s*import\s+', 'import ', line)
        
        # Remove spaces around from statement
        line = re.sub(r'\s*from\s+', 'from ', line)
        
        # Remove spaces around class statement
        line = re.sub(r'\s*class\s+', 'class ', line)
        
        # Remove spaces around def statement
        line = re.sub(r'\s*def\s+', 'def ', line)
        
        # Remove spaces around if statement
        line = re.sub(r'\s*if\s+', 'if ', line)
        
        # Remove spaces around elif statement
        line = re.sub(r'\s*elif\s+', 'elif ', line)
        
        # Remove spaces around else statement
        line = re.sub(r'\s*else\s+', 'else ', line)
        
        # Remove spaces around while statement
        line = re.sub(r'\s*while\s+', 'while ', line)
        
        # Remove spaces around for statement
        line = re.sub(r'\s*for\s+', 'for ', line)
        
        # Remove spaces around try statement
        line = re.sub(r'\s*try\s+', 'try ', line)
        
        # Remove spaces around except statement
        line = re.sub(r'\s*except\s+', 'except ', line)
        
        # Remove spaces around finally statement
        line = re.sub(r'\s*finally\s+', 'finally ', line)
        
        # Remove spaces around with statement
        line = re.sub(r'\s*with\s+', 'with ', line)
        
        # Remove spaces around raise statement
        line = re.sub(r'\s*raise\s+', 'raise ', line)
        
        # Remove spaces around assert statement
        line = re.sub(r'\s*assert\s+', 'assert ', line)
        
        # Remove spaces around break statement
        line = re.sub(r'\s*break\s+', 'break ', line)
        
        # Remove spaces around continue statement
        line = re.sub(r'\s*continue\s+', 'continue ', line)
        
        # Remove spaces around pass statement
        line = re.sub(r'\s*pass\s+', 'pass ', line)
        
        # Remove spaces around global statement
        line = re.sub(r'\s*global\s+', 'global ', line)
        
        # Remove spaces around nonlocal statement
        line = re.sub(r'\s*nonlocal\s+', 'nonlocal ', line)
        
        # Remove spaces around del statement
        line = re.sub(r'\s*del\s+', 'del ', line)
        
        # Remove spaces around exec statement
        line = re.sub(r'\s*exec\s+', 'exec ', line)
        
        # Remove spaces around await statement
        line = re.sub(r'\s*await\s+', 'await ', line)
        
        # Remove spaces around yield statement
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        
        # Remove spaces around print statement
        line = re.sub(r'\s*print\s+', 'print ', line)
        
        # Remove spaces around input statement
        line = re.sub(r'\s*input\s+', 'input ', line)
        
        # Remove spaces around format specifiers
        line = re.sub(r'%\s*\(\s*', '%(', line)
        line = re.sub(r'%\s*\)\s*', '%)', line)
        
        # Remove spaces around f-string syntax
        line = re.sub(r'f\s*\'\s*', 'f\'', line)
        line = re.sub(r'f\s*\"\s*', 'f\"', line)
        line = re.sub(r'f\s*`\s*', 'f`', line)
        
        # Remove spaces around braces
        line = re.sub(r'{\s*', '{', line)
        line = re.sub(r'\s*}', '}', line)
        
        # Remove spaces around brackets
        line = re.sub(r'\[\s*', '[', line)
        line = re.sub(r'\s*\]', ']', line)
        
        # Remove spaces around parentheses
        line = re.sub(r'\(\s*', '(', line)
        line = re.sub(r'\s*\)', ')', line)
        
        # Remove spaces around commas
        line = re.sub(r',\s*', ',', line)
        
        # Remove spaces around semicolons
        line = re.sub(r';\s*', ';', line)
        
        # Remove spaces around colons
        line = re.sub(r':\s*', ':', line)
        
        # Remove spaces around dots
        line = re.sub(r'\.\s*', '.', line)
        
        # Remove spaces around at symbols
        line = re.sub(r'@\s*', '@', line)
        
        # Remove spaces around hash symbols
        line = re.sub(r'#\s*', '#', line)
        
        # Remove spaces around exclamation marks
        line = re.sub(r'!\s*', '!', line)
        
        # Remove spaces around question marks
        line = re.sub(r'\?\s*', '?', line)
        
        # Remove spaces around ampersands
        line = re.sub(r'&\s*', '&', line)
        
        # Remove spaces around vertical bars
        line = re.sub(r'|\s*', '|', line)
        
        # Remove spaces around caret symbols
        line = re.sub(r'\^\s*', '^', line)
        
        # Remove spaces around asterisks
        line = re.sub(r'\*\s*', '*', line)
        
        # Remove spaces around plus signs
        line = re.sub(r'\+\s*', '+', line)
        
        # Remove spaces around minus signs
        line = re.sub(r'-\s*', '-', line)
        
        # Remove spaces around equals signs
        line = re.sub(r'=\s*', '=', line)
        
        # Remove spaces around less than signs
        line = re.sub(r'<\s*', '<', line)
        
        # Remove spaces around greater than signs
        line = re.sub(r'>\s*', '>', line)
        
        # Remove spaces around less than or equal to signs
        line = re.sub(r'<\=\s*', '<=', line)
        
        # Remove spaces around greater than or equal to signs
        line = re.sub(r'>=\s*', '>=', line)
        
        # Remove spaces around not equal to signs
        line = re.sub(r'\!\=\s*', '!=', line)
        
        # Remove spaces around logical AND operators
        line = re.sub(r'&&\s*', '&&', line)
        
        # Remove spaces around logical OR operators
        line = re.sub(r'\|\|\s*', '||', line)
        
        # Remove spaces around assignment operators
        line = re.sub(r'=\s*=', line)
        
        # Remove spaces around arithmetic operators
        line = re.sub(r'\+\s*', '+', line)
        line = re.sub(r'\-\s*', '-', line)
        line = re.sub(r'\*\s*', '*', line)
        line = re.sub(r'/\s*', '/', line)
        line = re.sub(r'%\s*', '%', line)
        
        # Remove spaces around bitwise AND operators
        line = re.sub(r'&\s*', '&', line)
        
        # Remove spaces around bitwise OR operators
        line = re.sub(r'|\s*', '|', line)
        
        # Remove spaces around bitwise XOR operators
        line = re.sub(r'\^\s*', '^', line)
        
        # Remove spaces around bitwise NOT operators
        line = re.sub(r'!\s*', '!', line)
        
        # Remove spaces around unary plus operators
        line = re.sub(r'\+\s*', '+', line)
        
        # Remove spaces around unary minus operators
        line = re.sub(r'-\s*', '-', line)
        
        # Remove spaces around increment operators
        line = re.sub(r'\+\+\s*', '++', line)
        line = re.sub(r'--\s*', '--', line)
        
        # Remove spaces around function call parentheses
        line = re.sub(r'\(\s*', '(', line)
        line = re.sub(r'\s*\)', ')', line)
        
        # Remove spaces around return statement
        line = re.sub(r'\s*return\s+', 'return ', line)
        
        # Remove spaces around yield statement
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        
        # Remove spaces around import statement
        line = re.sub(r'\s*import\s+', 'import ', line)
        
        # Remove spaces around from statement
        line = re.sub(r'\s*from\s+', 'from ', line)
        
        # Remove spaces around class statement
        line = re.sub(r'\s*class\s+', 'class ', line)
        
        # Remove spaces around def statement
        line = re.sub(r'\s*def\s+', 'def ', line)
        
        # Remove spaces around if statement
        line = re.sub(r'\s*if\s+', 'if ', line)
        
        # Remove spaces around elif statement
        line = re.sub(r'\s*elif\s+', 'elif ', line)
        
        # Remove spaces around else statement
        line = re.sub(r'\s*else\s+', 'else ', line)
        
        # Remove spaces around while statement
        line = re.sub(r'\s*while\s+', 'while ', line)
        
        # Remove spaces around for statement
        line = re.sub(r'\s*for\s+', 'for ', line)
        
        # Remove spaces around try statement
        line = re.sub(r'\s*try\s+', 'try ', line)
        
        # Remove spaces around except statement
        line = re.sub(r'\s*except\s+', 'except ', line)
        
        # Remove spaces around finally statement
        line = re.sub(r'\s*finally\s+', 'finally ', line)
        
        # Remove spaces around with statement
        line = re.sub(r'\s*with\s+', 'with ', line)
        
        # Remove spaces around raise statement
        line = re.sub(r'\s*raise\s+', 'raise ', line)
        
        # Remove spaces around assert statement
        line = re.sub(r'\s*assert\s+', 'assert ', line)
        
        # Remove spaces around break statement
        line = re.sub(r'\s*break\s+', 'break ', line)
        
        # Remove spaces around continue statement
        line = re.sub(r'\s*continue\s+', 'continue ', line)
        
        # Remove spaces around pass statement
        line = re.sub(r'\s*pass\s+', 'pass ', line)
        
        # Remove spaces around global statement
        line = re.sub(r'\s*global\s+', 'global ', line)
        
        # Remove spaces around nonlocal statement
        line = re.sub(r'\s*nonlocal\s+', 'nonlocal ', line)
        
        # Remove spaces around del statement
        line = re.sub(r'\s*del\s+', 'del ', line)
        
        # Remove spaces around exec statement
        line = re.sub(r'\s*exec\s+', 'exec ', line)
        
        # Remove spaces around await statement
        line = re.sub(r'\s*await\s+', 'await ', line)
        
        # Remove spaces around yield statement
        line = re.sub(r'\s*yield\s+', 'yield ', line)
        
        # Remove spaces around print statement
        line = re.sub(r'\s*print\s+', 'print ', line)
        
        # Remove spaces around input statement
        line = re.sub(r'\s*input\s+', 'input ', line)
        
        # Remove spaces around format specifiers
        line = re.sub(r'%\s*\(\s*', '%(', line)
        line = re.sub(r'%\s*\)\s*', '%)', line)
        
        # Remove spaces around f-string syntax
        line = re.sub(r'f\s*\'\s*', 'f\'', line)
        line = re.sub(r'f\s*\"\s*', 'f\"', line)
        line = re.sub(r'f\s*`\s*', 'f`', line)
        
        # Remove spaces around braces
        line = re.sub(r'{\s*', '{', line)
        line = re.sub(r'\s*}', '}', line)
        
        # Remove spaces around brackets
        line = re.sub(r'\[\s*', '[', line)
        line = re.sub(r'\s*\]', ']', line)
        
        # Remove spaces around parentheses
        line = re.sub(r'\(\s*', '(', line)
        line = re.sub(r'\s*\)', ')', line)
        
        # Remove spaces around commas
        line = re.sub(r',\s*', ',', line)
        
        # Remove spaces around semicolons
        line = re.sub(r';\s*', ';', line)
        
        # Remove spaces around colons
        line = re.sub(r':\s*', ':', line)
        
        # Remove spaces around dots
        line = re.sub(r'\.\s*', '.', line)
        
        # Remove spaces around at symbols
        line = re.sub(r'@\s*', '@', line)
        
        # Remove spaces around hash symbols
        line = re.sub(r'#\s*', '#', line)
        
        # Remove spaces around exclamation marks
        line = re.sub(r'!\s*', '!', line)
        
        # Remove spaces around question marks
        line = re.sub(r'\?\s*', '?', line)
        
        # Remove spaces around ampersands
        line = re.sub(r'&\s*', '&', line)
        
        # Remove spaces around vertical bars
        line = re.sub(r'|\s*', '|', line)
        
        # Remove spaces around caret symbols
        line = re.sub(r'\^\s*', '^', line)
        
        # Remove spaces around asterisks
        line = re.sub(r'\*\s*', '*', line)
        
        # Remove spaces around plus signs
        line = re.sub(r'\+\s*', '+', line)
        
        # Remove spaces around minus signs
        line = re.sub(r'-\s*', '-', line)
        
        # Remove spaces around equals signs
        line = re.sub(r'=\s*', '=', line)
        
        # Remove spaces around less than signs
        line = re.sub(r'<\s*', '<', line)
        
        # Remove spaces around greater than signs
        line = re.sub(r'>\s*', '>', line)
        
        # Remove spaces around less than or equal to signs
        line = re.sub(r'<\=\s*', '<=', line)
        
        # Remove spaces around greater than or equal to signs
        line