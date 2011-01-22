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
from CatPropDialog import *
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
        if hardDrive is None:
            self.__hardDrive = HardDrive()
        else:
            self.__hardDrive = hardDrive

        # -- Panel Initialization --
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "HDD Editor")

        # -- Control Initialization --
        self.szrBaseVert = wx.BoxSizer(wx.VERTICAL)

        self.szrLabel = wx.BoxSizer(wx.HORIZONTAL)
        self.szrPath = wx.BoxSizer(wx.HORIZONTAL)
        self.szrCat = wx.BoxSizer(wx.HORIZONTAL)
        self.szrCatButtons = wx.BoxSizer(wx.VERTICAL)

        self.lblLabel = wx.StaticText(self, label="Label:")
        self.txtLabel = wx.TextCtrl(self, value=self.__hardDrive.GetLabel())

        self.dirPath = wx.DirPickerCtrl(self)

        self.dirPath.SetPath(self.__hardDrive.GetPath())

        self.lblCat = wx.StaticText(self, label="Categories")

        self.lstCat = wx.ListView(self, style = wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_SORT_ASCENDING | wx.SUNKEN_BORDER, size=(380, 200))
        self.lstCat.InsertColumn(0, "Name")
        self.lstCat.SetColumnWidth(0, 180)
        self.lstCat.InsertColumn(1, "Rel. Path")
        self.lstCat.SetColumnWidth(1, 200)

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

        self.lstCat.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelected)
        self.lstCat.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnListItemDeSelected)
        self.lstCat.Bind(wx.EVT_LIST_DELETE_ITEM, self.OnListItemRemoved)

        self.btnCatAdd.Bind(wx.EVT_BUTTON, self.OnCatAdd)
        self.btnCatRem.Bind(wx.EVT_BUTTON, self.OnCatRem)
        self.btnCatEdit.Bind(wx.EVT_BUTTON, self.OnCatEdit)

        self.PopulateList()

    def PopulateList(self):
        """ Given a list of categories, populates the listview """

        print self.__hardDrive.GetCategoryList()
        for category in self.__hardDrive.GetCategoryList():
            self.AddCategoryListView(category)

    def AddCategoryListView(self, category):
        """ 
        Adds a new category to the list 
        ---
        Params:
            @ category - The new category to add
        """

        index = self.lstCat.InsertStringItem(self.lstCat.GetItemCount(), category.GetName())
        self.lstCat.SetStringItem(index, 1, category.GetRelativePath())

    def UpdateCategoryListView(self, index, category):
        """
        Update an existing category
        ---
        Params:
            @ index - The index of the category to update
            @ category - New category data
        """

        self.lstCat.SetStringItem(index, 0, category.GetName())
        self.lstCat.SetStringItem(index, 1, category.GetRelativePath())

    def RemCategoryListView(self, index):
        """ 
        Removes a category from the list 
        ---
        Params:
            @ index - The index of the category to remove
        """

        self.lstCat.DeleteItem(index)

    def GetHdd(self):
        """ 
        Returns the original Hdd object if no changes were made
        or a new hdd object with altered data
        ---
        Return: HardDrive object
        """

        return self.__hardDrive

    # -- EVENTS --
    def OnTextLabelChanged(self, event):
        """ 
        Checks if the label text is valid and enables the OK
        button if so.
        """

        label = self.txtLabel.GetValue()
        self.__hardDrive.SetLabel(label)

        if label.isspace() or not label:
            self.btnOk.Disable()
        else:
            self.btnOk.Enable()

    def OnDirPathChanged(self, event):
        """
        When the HDD path is changed we set the hard drive dirty
        flag to True
        """

        self.__hardDrive.SetPath(self.dirPath.GetPath())
        index = 0

        for category in self.__hardDrive.GetCategoryList():
            if not os.path.isdir(category.GetFullPath()):
                category.SetRelPath("")
                self.UpdateCategoryListView(index, category)
            index += 1

    def OnListItemSelected(self, event):
        """ Enables the ok, edit and remove buttons """

        self.btnCatEdit.Enable()
        self.btnCatRem.Enable()
        self.btnOk.Enable()

    def OnListItemDeSelected(self, event):
        """ Disables the ok, edit and remove buttons """

        self.btnCatEdit.Disable()
        self.btnCatRem.Disable()
        self.btnOk.Disable()

    def OnListItemRemoved(self, event):
        """ Disables the ok, edit and remove buttons """

        self.btnCatEdit.Disable()
        self.btnCatRem.Disable()
        self.btnOk.Disable()

    def OnCatAdd(self, event):
        """
        Ask the user for new category details and add it to the list
        """

        dlgCatProp = CatPropDialog(self, self.__hardDrive)

        if dlgCatProp.ShowModal() == wx.ID_OK:
            newCategory = dlgCatProp.GetCategory()
            self.__hardDrive.GetCategoryList().append(newCategory)
            self.AddCategoryListView(newCategory)

    def OnCatRem(self, event):
        """
        Remove the selected category from the lists
        """

        selectedIndex = self.lstCat.GetFirstSelected()

        if selectedIndex == -1:
            return
        
        self.RemCategoryListView(selectedIndex)
        self.__hardDrive.GetCategoryList().pop(selectedIndex)

    def OnCatEdit(self, event):
        """
        Edit the selected category with new user input
        """

        selectedIndex = self.lstCat.GetFirstSelected()

        if selectedIndex == -1:
            return

        dlgCatProp = CatPropDialog(self, self.dirPath.GetPath(), self.__hardDrive.GetCategoryList()[selectedIndex])

        if dlgCatProp.ShowModal() == wx.ID_OK:
            editedCategory = dlgCatProp.GetCategory()
            self.__hardDrive.GetCategoryList()[selectedIndex] = editedCategory
            self.UpdateCategoryListView(selectedIndex, editedCategory) 


