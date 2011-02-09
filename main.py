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

import wx, os, sys, logging, logging.handlers, traceback
from appinfo import *
from gui.frames.MainFrame import *

class MainApp(wx.App):
    """ Our main application class """

    def OnInit(self):
        """ What to do on application load """

        global appInfo

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

        LEVELS = {'debug': logging.DEBUG,
                  'info': logging.INFO,
                  'warning': logging.WARNING,
                  'error': logging.ERROR,
                  'critical': logging.CRITICAL}

        if len(sys.argv) > 1:
            level_name = sys.argv[1]
            level = LEVELS.get(level_name, logging.ERROR)
            logging.basicConfig(level=level)

        logFolder = os.path.join(appDataFolder, "logs")

        if not os.path.isdir(logFolder):
            os.mkdir(logFolder)

        logger = logging.getLogger("mhdd")
        fileHandler = logging.handlers.RotatingFileHandler(os.path.join(logFolder,
                                                  "mhddorganizer.log"),
                                                  maxBytes = 20*1024,
                                                  backupCount = 2)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s (%(funcName)s)")
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)

        self.config = wx.FileConfig(localFilename = os.path.join(appDataFolder, "config"),
                                    style = wx.CONFIG_USE_LOCAL_FILE)
        wx.Config.Set(self.config)

        self.frame = MainFrame(None, "MHDD Organizer")
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True;

def exceptionHandler(type, value, tb):
    try:
        message = "Unhandled exception: " + ''.join(traceback.format_exception(type, value, tb))
        print >> sys.stderr, message
        logger = logging.getLogger("mhdd")
        logger.error(message)
        wx.MessageBox(message, "Unhandled Exception", wx.OK | wx.ICON_ERROR)
    except Exception, e:
        pass
    sys.exit(1)

scriptDir = os.path.dirname(sys.argv[0])

if scriptDir:
    os.chdir(scriptDir)

sys.excepthook = exceptionHandler

app = MainApp(False)

app.MainLoop()
