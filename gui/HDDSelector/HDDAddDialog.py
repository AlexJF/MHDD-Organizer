#! /usr/bin/env python

"""
File: HDDAddDialog.py
Author: Revolt
Date: 27-08-2010
--------------------------
Desc:
    This file contains the definition and implementation of the dialog
    that allows you to add a new HDD to the selector
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

class HDDAddDialog(wx.Dialog):
    """ The HDD Add Dialog class """

    def __init__(self, parent):
        """ Constructor """

        # -- Panel Initialization --
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "Adding a new HDD")

        # -- Control Initialization --
        self.szrBaseVert = wx.BoxSizer(wx.VERTICAL)

        self.szrLabel = wx.BoxSizer(wx.HORIZONTAL)
        self.szrPath = wx.BoxSizer(wx.HORIZONTAL)

        self.lblLabel = wx.StaticText(self, label="Label:")
        self.txtLabel = wx.TextCtrl(self)

        self.dirPath = wx.DirPickerCtrl(self)
        self.dirPath.SetPath("/")

        self.szrLabel.Add(self.lblLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.szrLabel.Add(self.txtLabel, 1, wx.ALL, 5)

        self.szrPath.Add(self.dirPath, 1, wx.ALL, 5)

        self.szrDialogButtons = self.CreateButtonSizer(wx.OK | wx.CANCEL)

        self.szrBaseVert.Add(self.szrLabel, 0, wx.EXPAND | wx.ALL, 5)
        self.szrBaseVert.Add(self.szrPath, 0, wx.EXPAND | wx.ALL, 5)
        self.szrBaseVert.Add(self.szrDialogButtons, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(self.szrBaseVert)
        self.Layout()

    def GetHDDLabel(self):
        """ Returns the label of the newly created HDD """

        return self.txtLabel.GetValue()

    def GetHDDPath(self):
        """ Returns the path of the newly created HDD """

        return self.dirPath.GetPath()
