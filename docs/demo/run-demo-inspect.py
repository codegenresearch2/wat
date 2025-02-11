#!/usr/bin/env python3
from livekey import animate_commands

commands = [
    'python',
    'from wat import wat',
    'wat / {7}',
    'wat.short / (1,)',
    'import re',
    'wat()',
    'wat / re',
    'wat.code / re.match',
    'wat.short / locals()',
]

class Wat:
    def __init__(self, code=None):
        self.code = code

    def __call__(self, *args, **kwargs):
        if self.code:
            return self.code(*args, **kwargs)

wat = Wat()
wat.code = re.match
wat.short = locals()

if __name__ == '__main__':
    animate_commands(commands, key_delay=0.1, line_delay=1.0)