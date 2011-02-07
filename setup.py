import sys
from cx_Freeze import setup, Executable
from appinfo import *

script = "main.py"
target = "MHDDOrganizer"
base = None
packages = ["wx", "sqlite3"]

if sys.platform == "win32":
    target="MHDDOrganizer.exe"
    base = "Win32GUI"

exe = Executable(
    script=script,
    targetName=target,
    packages=packages,
    base=base)

includefiles = ['README', 'NEWS', 'COPYING', 'AUTHORS', 'gui/images/']
 
setup(
    name = appInfo['name'],
    version = appInfo['version'],
    description = appInfo['description'],
    executables = [exe],
    options = {'build_exe': {'include_files':includefiles}},
)
