#! /usr/bin/env python

"""
File: MainFrame.py
Author: Revolt
Date: 15-08-2010
--------------------------
Desc:
    This file contains the definition and implementation of the main
    frame of the application
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


import wx, os
from ObjectDetailsPanel import *

# --------------------- Main frame Class -----------------------

class MainFrame(wx.Frame):
    """ The main frame of the application """

    def __init__(self, parent, title):
        """ Constructor """

        # -- Frame Initialization --
        wx.Frame.__init__(self, parent, title=title, size=(600,400))

        # -- Control Initialization --
        self.sptMain = wx.SplitterWindow(self)

        self.pnlObjList = wx.Panel(self.sptMain)
        self.pnlObjDetails = ObjectDetailsPanel(self.sptMain)
        
        self.sptMain.SplitVertically(self.pnlObjList, self.pnlObjDetails, 150)
        self.sptMain.SetSashPosition(150)

        self.lstObj = wx.ListView(self.pnlObjList, style = wx.LC_REPORT | wx.LC_NO_HEADER | wx.LC_SINGLE_SEL | wx.LC_SORT_ASCENDING)
        self.szrBaseObjList = wx.BoxSizer(wx.VERTICAL)
        self.szrBaseObjList.Add(self.lstObj, 1, wx.ALL | wx.EXPAND, 5)

        self.scrObjDetails = wx.ScrolledWindow(self.pnlObjDetails)
        self.szrBaseObjDetails = wx.BoxSizer(wx.VERTICAL)
        self.szrBaseObjDetails.Add(self.scrObjDetails, 1, wx.ALL | wx.EXPAND, 5)

        self.pnlObjList.SetSizer(self.szrBaseObjList)
        self.pnlObjDetails.SetSizer(self.szrBaseObjDetails)

        self.Layout()

        # -- Event Binding -- 
        #self.frm.Bind(wx.EVT_TOOL, self.OnVidAdd, id=xrc.XRCID('tlbItemVidAdd'))

        #self.btnUndo.Bind(wx.EVT_BUTTON, self.OnUndo)

