#! /usr/bin/env python

"""
File: main.py
Author: Revolt
--------------------------
Desc:
    This file initializes the wx application and starts the main
    application loop.
--------------------------
Copyright (C) 2010 Revolt 

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import wx, os, sys, logging
from appinfo import *
from gui.frames.MainFrame import *

class MainApp(wx.App):
    """ Our main application class """

    __logger = logging.getLogger("main")

    def OnInit(self):
        """ What to do on application load """

        global appInfo

        self.__logger.setLevel(logging.DEBUG)
        h1 = logging.StreamHandler()
        h1.setLevel(logging.DEBUG)
        f = logging.Formatter("%(levelname)s %(asctime)s %(funcName)s %(message)s")
        h1.setFormatter(f)
        self.__logger.addHandler(h1)

        if "unicode" not in wx.PlatformInfo:
            self.__logger.warning("wxPython isn't built as unicode")

        self.SetAppName(appInfo['name'])
        self.SetClassName(appInfo['class'])

        #wx.Image.AddHandler(wx.PNGHandler())
        #wx.Image.AddHandler(wx.JPEGHandler())
        stdPaths = wx.StandardPaths.Get()
        appDataFolder = stdPaths.GetUserLocalDataDir()

        if not os.path.isdir(appDataFolder):
            os.mkdir(appDataFolder)


        self.config = wx.FileConfig(localFilename = os.path.join(appDataFolder, "config"),
                                    style = wx.CONFIG_USE_LOCAL_FILE)
        wx.Config.Set(self.config)

        self.frame = MainFrame(None, "MHDD Organizer")
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True;

scriptDir = os.path.dirname(sys.argv[0])

if scriptDir:
    os.chdir(scriptDir)

app = MainApp(False)
app.MainLoop()
