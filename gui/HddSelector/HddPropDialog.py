#! /usr/bin/env python

"""
File: HddPropDialog.py
Author: Revolt
--------------------------
Desc:
    This file contains the definition and implementation of the dialog
    that allows you to add a new Hdd to the selector or edit the props
    of an already added Hdd.
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


import wx, os, ConfigParser
from classes.Category import *
from classes.HardDrive import *

class HddPropDialog(wx.Dialog):
    """ The Hdd Prop Dialog class """

    def __init__(self, parent, hardDrive = None):
        """
        Constructor 
        ---
        Params:
            @ hardDrive - Hard Drive to edit or None
        """

        # -- Private Variables Initialization --
        self.originalHardDrive = hardDrive
        self.hardDriveDirty = True
        self.categoryList = []
        label = ""
        path = ""

        if hardDrive:
            label = hardDrive.GetLabel()
            path = hardDrive.GetPath()
            hardDrive.LoadCategoryList()
            self.categoryList = list(hardDrive.GetCategoryList())
            self.hardDriveDirty = False

        # -- Panel Initialization --
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "HDD Editor")

        # -- Control Initialization --
        self.szrBaseVert = wx.BoxSizer(wx.VERTICAL)

        self.szrLabel = wx.BoxSizer(wx.HORIZONTAL)
        self.szrPath = wx.BoxSizer(wx.HORIZONTAL)
        self.szrCat = wx.BoxSizer(wx.HORIZONTAL)
        self.szrCatButtons = wx.BoxSizer(wx.VERTICAL)

        self.lblLabel = wx.StaticText(self, label="Label:")
        self.txtLabel = wx.TextCtrl(self, value=label)

        self.dirPath = wx.DirPickerCtrl(self)

        if path:
            self.dirPath.SetPath(path)
        else:
            self.dirPath.SetPath("/")

        self.lblCat = wx.StaticText(self, label="Categories")

        self.lstCat = wx.ListView(self, style = wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_SORT_ASCENDING | wx.SIMPLE_BORDER, size=(600, 200))
        self.lstCat.InsertColumn(0, "Name")
        self.lstCat.SetColumnWidth(0, 180)
        self.lstCat.InsertColumn(1, "Type")
        self.lstCat.SetColumnWidth(1, 100)
        self.lstCat.InsertColumn(2, "Rel. Path")
        self.lstCat.SetColumnWidth(2, 200)

        self.btnCatAdd = wx.BitmapButton(self, bitmap=wx.Bitmap("gui/images/add.png", wx.BITMAP_TYPE_PNG))
        self.btnCatRem = wx.BitmapButton(self, bitmap=wx.Bitmap("gui/images/rem.png", wx.BITMAP_TYPE_PNG))
        self.btnCatEdit = wx.BitmapButton(self, bitmap=wx.Bitmap("gui/images/edit.png", wx.BITMAP_TYPE_PNG))

        self.szrLabel.Add(self.lblLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.szrLabel.Add(self.txtLabel, 1, wx.ALL, 5)

        self.szrPath.Add(self.dirPath, 1, wx.ALL, 5)

        self.szrCatButtons.Add(self.btnCatAdd, 0, wx.ALL, 5)
        self.szrCatButtons.Add(self.btnCatRem, 0, wx.ALL, 5)
        self.szrCatButtons.Add(self.btnCatEdit, 0, wx.ALL, 5)

        self.szrCat.Add(self.lstCat, 1, wx.ALL | wx.EXPAND, 5)
        self.szrCat.Add(self.szrCatButtons, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.szrDialogButtons = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        self.btnOk = self.FindWindowById(wx.ID_OK)
        self.btnCancel = self.FindWindowById(wx.ID_CANCEL)

        # If we are adding a new harddrive, disable the OK button until
        # the data is valid enough
        if not hardDrive:
            self.btnOk.Disable()

        self.szrBaseVert.Add(self.szrLabel, 0, wx.EXPAND | wx.ALL, 5)
        self.szrBaseVert.Add(self.szrPath, 0, wx.EXPAND | wx.ALL, 5)
        self.szrBaseVert.Add(self.lblCat, 0, wx.LEFT | wx.RIGHT | wx.TOP, 5)
        self.szrBaseVert.Add(self.szrCat, 1, wx.EXPAND | wx.ALL, 5)
        self.szrBaseVert.Add(self.szrDialogButtons, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(self.szrBaseVert)

        # -- Event Binding
        self.txtLabel.Bind(wx.EVT_TEXT, self.OnTextLabelChanged)
        self.dirPath.Bind(wx.EVT_DIRPICKER_CHANGED, self.OnDirPathChanged)

        self.PopulateList()

    def PopulateList(self):
        """ Given a list of categories, populates the listview """

        for category in self.categoryList:
            AddCategory(category.name, category.type, category.path)

    def AddCategory(self, category):
        """ Adds a new category to the list """

        index = self.lstCat.InsertItem(self.lstCat.GetItemCount(), category.name)
        self.lstCat.SetStringItem(index, 1, category.type)
        self.lstCat.SetStringItem(index, 2, category.path)
        self.categoryList.append(category)

    def RemCategory(self, index):
        """ Removes a category from the list """

        self.lstCat.DeleteItem(index)
        self.categoryList.remove(index)

    def GetHdd(self):
        """ 
        Returns the original Hdd object if no changes were made
        or a new hdd object with altered data
        ---
        Return: HardDrive object
        """

        if not self.hardDriveDirty:
            return self.originalHardDrive
        else:
            return HardDrive(None, self.txtLabel.GetValue(), self.dirPath.GetPath(), self.categoryList)

    # -- Events --
    def OnTextLabelChanged(self, event):
        """ 
        Checks if the label text is valid and enables the OK
        button if so.
        """

        label = self.txtLabel.GetValue()

        if label.isspace() or not label:
            self.btnOk.Disable()
        else:
            self.btnOk.Enable()

        self.hardDriveDirty = True

    def OnDirPathChanged(self, event):
        """
        When the HDD path is changed we set the hard drive dirty
        flag to True
        """

        self.hardDriveDirty = True





