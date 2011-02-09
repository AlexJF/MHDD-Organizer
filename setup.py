import sys
from cx_Freeze import setup, Executable
from appinfo import *

script = "main.py"
target = "MHDDOrganizer"
base = None
packages = ["wx", "sqlite3"]
includefiles = ['README', 'NEWS', 'COPYING', 'AUTHORS', 'gui/images/']

if sys.platform == "win32":
    target="MHDDOrganizer.exe"
    base = "Win32GUI"
    includefiles.append(('extras/build/MHDDOrganizer_debug.bat',
                         'MHDDOrganizer_debug.bat'))

exe = Executable(
    script=script,
    targetName=target,
    packages=packages,
    base=base)
 
setup(
    name = appInfo['name'],
    version = appInfo['version'],
    description = appInfo['description'],
    executables = [exe],
    options = {'build_exe': {'include_files':includefiles}},
)
