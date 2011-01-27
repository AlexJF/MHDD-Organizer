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

    __category = None

    def __init__(self, parent, hdd, category = None):
        """
        Constructor 
        ---
        Params:
            @parent - Owner of the dialog.
            @ hdd (HardDrive) - The hdd in which to add the category
            @ category (Category) - Category to edit or None
        """

        # -- Private Variables Initialization --
        if category:
            self.__category = category
        else:
            self.__category = Category("", "", hdd)

        # -- Panel Initialization --
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "Category Editor")

        # -- Control Initialization --
        self.szrBaseVert = wx.BoxSizer(wx.VERTICAL)

        self.szrName = wx.BoxSizer(wx.HORIZONTAL)
        self.szrPath = wx.BoxSizer(wx.HORIZONTAL)

        self.lblName = wx.StaticText(self, label = "Name:")
        self.txtName = wx.TextCtrl(self, value=self.__category.GetName())

        self.dirPath = wx.DirPickerCtrl(self)
        self.dirPath.SetPath(self.__category.GetFullPath())

        self.szrName.Add(self.lblName, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.szrName.Add(self.txtName, 1, wx.ALL, 5)

        self.szrPath.Add(self.dirPath, 1, wx.ALL, 5)

        self.szrDialogButtons = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        self.btnOk = self.FindWindowById(wx.ID_OK)
        self.btnCancel = self.FindWindowById(wx.ID_CANCEL)

        # If we are adding a new category, disable the OK button until
        # the data is valid enough
        if not category:
            self.btnOk.Disable()

        self.szrBaseVert.Add(self.szrName, 0, wx.EXPAND | wx.ALL, 5)
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

        return self.__category

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
            self.__category.SetName(name)
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
        if newPath.find(self.__category.GetHdd().GetPath()) == -1:
            self.btnOk.Disable()
            return

        self.__category.SetRelPath(os.path.relpath(newPath, self.__category.GetHdd().GetPath()))
