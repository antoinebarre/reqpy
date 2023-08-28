from io import TextIOWrapper
from pathlib import Path


def safe_open_w(path: Path) -> TextIOWrapper:
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    path.parent.mkdir(exist_ok=True)
    return open(path, 'w+')
