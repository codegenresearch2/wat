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
    replaced_contents: list[str] = []
    for dst_filename in dst_filenames:
        content = Path(dst_filename).read_text()
        assert old_code in content, f'cannot find current Insta-Load code in {dst_filename}'
        replaced_content = content.replace(old_code, new_code)
        assert old_code not in replaced_content, 'old code still exists in the replaced content'
        assert new_code in replaced_content, 'new code does not exist in the replaced content'
        replaced_contents.append(replaced_content)

    for i, dst_filename in enumerate(dst_filenames):
        Path(dst_filename).write_text(replaced_contents[i])
        print(f'Code replaced in {dst_filename}')


if __name__ == '__main__':
    _regenerate(sys.argv[1], sys.argv[2:])