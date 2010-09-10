#! /usr/bin/env python

"""
File: CatPropDialog.py
Author: Revolt
--------------------------
Desc:
    This file contains the definition and implementation of the dialog
    that allows you to add a new category to the harddrive or edit the 
    props of an already added category.
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
from classes.Category import *

class CatPropDialog(wx.Dialog):
    """ The Cat Prop Dialog class """

    def __init__(self, parent, hddPath, category = None):
        """
        Constructor 
        ---
        Params:
            @ hddPath (String) - Path to the hdd that will own this category
            @ category (Category) - Category to edit or None
        """

        # -- Private Variables Initialization --
        self._hddPath = hddPath
        name = ""
        type = ""
        relpath = ""

        if category:
            name = category.GetName()
            type = category.GetType()
            relpath = category.GetRelativePath()

        # -- Panel Initialization --
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "Category Editor")

        # -- Control Initialization --
        self.szrBaseVert = wx.BoxSizer(wx.VERTICAL)

        self.szrName = wx.BoxSizer(wx.HORIZONTAL)
        self.szrType = wx.BoxSizer(wx.HORIZONTAL)
        self.szrPath = wx.BoxSizer(wx.HORIZONTAL)

        self.lblName = wx.StaticText(self, label = "Name:")
        self.txtName = wx.TextCtrl(self, value=name)

        self.lblType = wx.StaticText(self, label = "Type:")
        self.cmbType = wx.ComboBox(self, choices = ("Movies",), style = wx.CB_READONLY | wx.CB_SORT)

        self.cmbType.SetSelection(0)
        if type:
            self.cmbType.SetStringSelection(type)

        self.dirPath = wx.DirPickerCtrl(self)
        self.dirPath.SetPath(os.path.join(self._hddPath, relpath))

        self.szrName.Add(self.lblName, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.szrName.Add(self.txtName, 1, wx.ALL, 5)

        self.szrType.Add(self.lblType, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.szrType.Add(self.cmbType, 1, wx.ALL, 5)

        self.szrPath.Add(self.dirPath, 1, wx.ALL, 5)

        self.szrDialogButtons = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        self.btnOk = self.FindWindowById(wx.ID_OK)
        self.btnCancel = self.FindWindowById(wx.ID_CANCEL)

        # If we are adding a new category, disable the OK button until
        # the data is valid enough
        if not category:
            self.btnOk.Disable()

        self.szrBaseVert.Add(self.szrName, 0, wx.EXPAND | wx.ALL, 5)
        self.szrBaseVert.Add(self.szrType, 0, wx.EXPAND | wx.ALL, 5)
        self.szrBaseVert.Add(self.szrPath, 0, wx.EXPAND | wx.ALL, 5)
        self.szrBaseVert.Add(self.szrDialogButtons, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(self.szrBaseVert)

        # -- Event Binding
        self.txtName.Bind(wx.EVT_TEXT, self.OnTextNameChanged)
        self.dirPath.Bind(wx.EVT_DIRPICKER_CHANGED, self.OnDirPathChanged)


    def GetCategory(self):
        """ 
        Return (Category): Category object with input data
        """

        return Category(self.txtName.GetValue(), self.cmbType.GetStringSelection(), os.path.relpath(self.dirPath.GetPath(), self._hddPath))

    # -- EVENTS --
    def OnTextNameChanged(self, event):
        """ 
        Checks if the label text is valid and enables the OK
        button if so.
        """

        name = self.txtName.GetValue()

        if name.isspace() or not name:
            self.btnOk.Disable()
        else:
            self.btnOk.Enable()

    def OnDirPathChanged(self, event):
        """
        When the HDD path is changed we set the hard drive dirty
        flag to True
        """

        newPath = self.dirPath.GetPath()

        # If the hddPath isn't present in the newPath then it is
        # invalid because the category path must be contained in
        # the respective hdd
        if newPath.find(self._hddPath) == -1:
            seld.dirPath.SetPath(self._hddPath)
