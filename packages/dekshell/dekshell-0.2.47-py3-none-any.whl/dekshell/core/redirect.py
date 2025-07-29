import os
import sys
import shutil
from dektools.sys import sys_paths_relative
from dektools.file import normal_path
from ..utils.shell import shell_name


def search_bin_by_path_tree(filepath, bin_name, skip_self=True):
    filepath = normal_path(filepath)
    cursor = os.path.dirname(filepath) if os.path.isfile(filepath) else filepath
    while True:
        for venv_name in ('venv', 'env', '.venv'):
            path_venv = os.path.join(cursor, venv_name)
            if os.path.isdir(path_venv):
                if skip_self and sys.prefix == path_venv:
                    return
                else:
                    path_scripts = sys_paths_relative(path_venv)['scripts']
                    path_exe = shutil.which(bin_name, path=path_scripts)
                    if path_exe:
                        return path_exe
        dir_cursor = os.path.dirname(cursor)
        if dir_cursor == cursor:
            break
        cursor = dir_cursor


def redirect_shell_by_path_tree(filepath):
    return search_bin_by_path_tree(filepath, shell_name)
