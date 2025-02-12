from pathlib import Path
import sys

from wat.inspection.insta.dump import dump_snippet
from wat.inspection.insta.instaload import code


def _regenerate(src_filename: str, dst_filenames: list[str]):
    old_code_length = len(code.decode())
    new_code = dump_snippet(src_filename)
    new_code_length = len(new_code)
    print(f'Insta-Load code ({new_code_length} characters):\n{new_code}\n')
    
    replaced_contents: list[str] = []
    
    for dst_filename in dst_filenames:
        content = Path(dst_filename).read_text()
        assert content.count(code.decode()) == 1, f'cannot find current Insta-Load code in {dst_filename}'
        replaced_content = content.replace(code.decode(), new_code)
        assert replaced_content.count(new_code) == 1
        replaced_contents.append(replaced_content)

    if code.decode() == new_code:
        print('Insta-Load code is already up to date')
        return

    for i, dst_filename in enumerate(dst_filenames):
        Path(dst_filename).write_text(replaced_contents[i])
        print(f'Code replaced in {dst_filename}')

    char_count_change = new_code_length - old_code_length
    print(f'Character count change: {"+" if char_count_change >= 0 else ""}{char_count_change} characters')


if __name__ == '__main__':
    _regenerate(sys.argv[1], sys.argv[2:])