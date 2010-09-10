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

import wx, os, sys
from gui.MainFrame import *

class MainApp(wx.App):
    """ Our main application class """

    def OnInit(self):
        """ What to do on application load """

        self.SetAppName("MHDD Organizer")

        #wx.Image.AddHandler(wx.PNGHandler())
        #wx.Image.AddHandler(wx.JPEGHandler())

        self.config = wx.FileConfig(style=wx.CONFIG_USE_LOCAL_FILE)
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
