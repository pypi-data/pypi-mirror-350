import os
import sys


def fix_pyinstaller_workdir():
    try:
        os.chdir(sys._MEIPASS)  # type: ignore
    except AttributeError:
        pass
