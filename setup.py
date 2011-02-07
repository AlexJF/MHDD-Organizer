from cx_Freeze import setup, Executable
from appinfo import *
 
exe = Executable(
    script="main.py",
    targetName="MHDDOrganizer",
    packages=["wxpython", "sqlite3"]
)

includefiles = ['README', 'NEWS', 'COPYING', 'AUTHORS', 'gui/images/']
 
setup(
    name = appInfo['name'],
    version = appInfo['version'],
    description = appInfo['description'],
    executables = [exe],
    options = {'build_exe': {'include_files':includefiles}},
    data_files=[('images', ['gui/images/*'])]
)
