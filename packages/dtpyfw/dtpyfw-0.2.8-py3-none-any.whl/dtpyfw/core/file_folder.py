import os


__all__ = (
    'make_directory',
    'folder_path_of_file',
    'remove_file',
)


def make_directory(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def folder_path_of_file(path: str):
    return os.path.dirname(os.path.realpath(path))


def remove_file(path: str):
    if os.path.exists(path):
        os.remove(path)
