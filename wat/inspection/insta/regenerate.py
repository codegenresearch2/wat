from pathlib import Path
import sys

from wat.inspection.insta.dump import dump_snippet
from wat.inspection.insta.instaload import code


def _regenerate(src_filename: str, dst_filenames: list[str]):
    old_code: str = code.decode()
    new_code: str = dump_snippet(src_filename)
    
    if old_code == new_code:
        print('Insta-Load code is up to date')
        return
    
    for dst_filename in dst_filenames:
        content = Path(dst_filename).read_text()
        assert old_code in content, f'Old Insta-Load code not found in {dst_filename}'
        assert content.count(old_code) == 1, 'Old Insta-Load code appears more than once in the content'
        replaced_content = content.replace(old_code, new_code)
        assert replaced_content.count(new_code) == 1, 'New Insta-Load code does not appear exactly once after replacement'
        Path(dst_filename).write_text(replaced_content)
        print(f'Code replaced in {dst_filename}')


if __name__ == '__main__':
    _regenerate(sys.argv[1], sys.argv[2:])