"""
生成 requirements 文件
"""
import contextlib
import subprocess
from pathlib import Path

if __name__ == '__main__':
    status: int = 0
    dev_dir: Path = Path(__file__).parent.resolve()

    for i in ('requirements', 'requirements-dev'):
        output_file: str = f'../{i}' if i == 'requirements' else i
        status += subprocess.call(['pip-compile', f'{i}.in',
                                   '--output-file', f'{output_file}.txt',
                                   '--annotation-style=line'], cwd=dev_dir)
        with contextlib.suppress(FileNotFoundError):
            with open(f'{output_file}.txt', 'r') as f:
                lines = f.readlines()
            with open(f'{output_file}.txt', 'w') as f:
                for line in lines:
                    if line.startswith('--index-url'):
                        f.write('--index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple\n')
                        continue
                    f.write(line)

    exit(status != 0)
