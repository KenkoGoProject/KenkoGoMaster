import logging
import sys
from datetime import date
from logging import FileHandler, Handler, Logger
from pathlib import Path

from rich.logging import RichHandler

logging.basicConfig(
    level=logging.NOTSET,
    handlers=[]
)
log: Logger = logging.getLogger('KenkoGo')

# 添加控制台输出
rich_handler: Handler = RichHandler(show_path=False, log_time_format='%Y/%m/%d %X.%f', show_time=False,
                                    rich_tracebacks=True, tracebacks_show_locals=True)
rich_handler.setFormatter(logging.Formatter('%(asctime)s.%(msecs)03d | %(message)s', datefmt='%Y/%m/%d %H:%M:%S'))
log.addHandler(rich_handler)

# 添加文件输出
log_file_dir: Path = Path('log')
log_file_dir.mkdir(exist_ok=True)
log_file: Path = log_file_dir / f'{date.today()}.log'

file_handler: Handler = FileHandler(log_file, encoding='utf-8')
file_formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)-8s | %(message)s', datefmt='%Y/%m/%d %X')
file_handler.setFormatter(file_formatter)

log.addHandler(file_handler)

# 让PyCharm调试输出的信息换行
if sys.gettrace() is not None:
    print('Debug Mode')
