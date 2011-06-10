#! /usr/bin/env python

"""
File: HddSelectorDialog.py
Author: Revolt
--------------------------
Desc:
    This file contains the definition and implementation of the dialog
    that allows you to select what disk to analyze.
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
from HddPropDialog import *
from classes.Category import *
from classes.HardDriveList import *

class HddSelectorDialog(wx.Dialog):
    """ The Hdd Selector Dialog class """

    def __init__(self, parent):
        """ Constructor """

        # -- Private Variables Initialization --
        self.__hddList = HardDriveList()

        # -- Panel Initialization --
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "Please Select a HDD")

        # -- Control Initialization --
        self.szrBaseVert = wx.BoxSizer(wx.VERTICAL)
        self.szrBaseHori = wx.BoxSizer(wx.HORIZONTAL)

        self.lstHdd = wx.ListView(self, style = wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.SUNKEN_BORDER)
        self.lstHdd.SetMinSize((380, 200))
        self.lstHdd.InsertColumn(0, "Label")
        self.lstHdd.SetColumnWidth(0, 180)
        self.lstHdd.InsertColumn(1, "Path")
        self.lstHdd.SetColumnWidth(1, 200)

        self.lstHddImageList = wx.ImageList(22, 22)
        self.lstHddImageList.Add(wx.Bitmap("gui/images/hdd-off.png", wx.BITMAP_TYPE_PNG))
        self.lstHddImageList.Add(wx.Bitmap("gui/images/hdd-on.png", wx.BITMAP_TYPE_PNG))

        self.lstHdd.SetImageList(self.lstHddImageList, wx.IMAGE_LIST_SMALL)

        self.szrButtonsVert = wx.BoxSizer(wx.VERTICAL)

        self.btnAdd = wx.BitmapButton(self, bitmap=wx.Bitmap("gui/images/add.png", wx.BITMAP_TYPE_PNG))
        self.btnRem = wx.BitmapButton(self, bitmap=wx.Bitmap("gui/images/rem.png", wx.BITMAP_TYPE_PNG))
        self.btnRem.Disable()
        self.btnEdit = wx.BitmapButton(self, bitmap=wx.Bitmap("gui/images/edit.png", wx.BITMAP_TYPE_PNG))
        self.btnEdit.Disable()
        self.btnRefresh = wx.BitmapButton(self, bitmap=wx.Bitmap("gui/images/refresh.png", wx.BITMAP_TYPE_PNG))

        self.szrButtonsVert.Add(self.btnAdd, 1, wx.ALL, 5)
        self.szrButtonsVert.Add(self.btnRem, 1, wx.ALL, 5)
        self.szrButtonsVert.Add(self.btnEdit, 1, wx.ALL, 5)
        self.szrButtonsVert.Add(self.btnRefresh, 1, wx.ALL, 5)

        self.szrBaseHori.Add(self.lstHdd, 1, wx.ALL | wx.EXPAND, 5)
        self.szrBaseHori.Add(self.szrButtonsVert, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.szrDialogButtons = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        self.btnOk = self.FindWindowById(wx.ID_OK)
        self.btnOk.Disable()
        self.btnCancel = self.FindWindowById(wx.ID_CANCEL)

        self.szrBaseVert.Add(self.szrBaseHori, 1, wx.EXPAND | wx.ALL, 5)
        self.szrBaseVert.Add(self.szrDialogButtons, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(self.szrBaseVert)

        # -- Event Binding --
        self.lstHdd.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelected)
        self.lstHdd.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnListItemDeSelected)
        self.lstHdd.Bind(wx.EVT_LIST_DELETE_ITEM, self.OnListItemRemoved)

        self.btnAdd.Bind(wx.EVT_BUTTON, self.OnHddAdd)
        self.btnRem.Bind(wx.EVT_BUTTON, self.OnHddRem)
        self.btnEdit.Bind(wx.EVT_BUTTON, self.OnHddEdit)
        self.btnRefresh.Bind(wx.EVT_BUTTON, self.OnHddRefresh)

        self.btnOk.Bind(wx.EVT_BUTTON, self.OnHddSelectorOk)

        self.ReloadHddList()

    def AddHardDriveListView(self, hardDrive):
        """ 
        Adds a new harddrive to the listview 
        ---
        Params:
            @ hardDrive - A HardDrive object containing data about
                          the harddrive we're gonna add to the list
        """

        index = self.lstHdd.InsertImageStringItem(self.lstHdd.GetItemCount(), hardDrive.GetLabel(), hardDrive.Connected())
        self.lstHdd.SetStringItem(index, 1, hardDrive.GetPath())

    def UpdateHardDriveListView(self, index):
        """
        Updates the harddrive info in the listview of the harddrive
        at the specified index
        ---
        Params:
            @ index - Index of the harddrive to update
        """

        hdd = self.__hddList[index]

        self.lstHdd.SetStringItem(index, 0, hdd.GetLabel(), hdd.Connected())
        self.lstHdd.SetStringItem(index, 1, hdd.GetPath())

    def RemoveHardDriveListView(self, index):
        """
        Removes the hard drive at the specified index from the list view
        ---
        Params:
            @ index - Index of the hard drive in the list view
        """
        
        self.lstHdd.DeleteItem(index)

    def ReloadHddList(self):
        """ Reloads Hdd info from the config and refreshes the listview """

        self.__hddList.LoadFromConfig()
        self.RefreshHddList()


    def RefreshHddList(self):
        """ Refreshes the listview according to the Hdd info in memory """

        self.lstHdd.DeleteAllItems()
        for hardDrive in self.__hddList:
            self.AddHardDriveListView(hardDrive)

    def GetHddList(self):
        """
        Returns this selector's hdd list.
        ---
        Return: (HardDriveList) This selector's hdd list.
        """

        return self.__hddList

    def GetSelectedHdd(self):
        """ 
        Returns the Hdd selected by the user in the list 
        ---
        Return: 
            # indexSelectedItem - Index of the selected Hdd on the listview
            # hardDrive - The HardDrive object associated with the selected Hdd
        """

        indexSelectedItem = self.lstHdd.GetFirstSelected()

        if indexSelectedItem == -1:
            return -1, None

        return indexSelectedItem, self.__hddList[indexSelectedItem]

    # -- EVENTS --
    def OnListItemSelected(self, event):
        """ Enables the ok, edit and remove buttons """

        self.btnEdit.Enable()
        self.btnRem.Enable()

        selectedHdd = self.GetSelectedHdd()[1]
        self.btnOk.Enable()

    def OnListItemDeSelected(self, event):
        """ Disables the ok, edit and remove buttons """

        self.btnEdit.Disable()
        self.btnRem.Disable()
        self.btnOk.Disable()

    def OnListItemRemoved(self, event):
        """ Disables the ok, edit and remove buttons """

        self.btnEdit.Disable()
        self.btnRem.Disable()
        self.btnOk.Disable()

    def OnHddAdd(self, event):
        """ Shows the Hdd Add dialog and handles insertion of Hdd to the config and list """

        dlgHddProp = HddPropDialog(self)

        if dlgHddProp.ShowModal() == wx.ID_OK:
            newHdd = dlgHddProp.GetHdd()

            self.__hddList.Add(newHdd)
            self.AddHardDriveListView(newHdd)

        dlgHddProp.Destroy()

    def OnHddRem(self, event):
        """ Removes the selected Hdd from the list and config """

        selectedIndex, selectedHdd = self.GetSelectedHdd()

        if not selectedHdd:
            return

        if wx.MessageBox("Do you want to remove all MHDD Organizer info from the HDD aswell?", 
                         "MHDD Info Removal",
                         wx.YES_NO,
                         self) == wx.YES:
            selectedHdd.CleanAllInfo()

        self.RemoveHardDriveListView(selectedIndex)
        self.__hddList.Remove(selectedIndex)
        self.RefreshHddList()

    def OnHddEdit(self, event):
        """ Allows the user to edit Hdd's info """

        selectedIndex, selectedHdd = self.GetSelectedHdd()

        if not selectedHdd:
            return

        dlgHddProp = HddPropDialog(self, selectedHdd)

        if dlgHddProp.ShowModal() == wx.ID_OK:
            editedHdd = dlgHddProp.GetHdd()
            
            self.__hddList.Edit(selectedIndex, editedHdd)
            self.UpdateHardDriveListView(selectedIndex)

        dlgHddProp.Destroy()


    def OnHddRefresh(self, event):
        """ Refreshes the Hdd list """

        self.RefreshHddList()

    def OnHddSelectorOk(self, event):
        """ Saves changes made """

        self.__hddList.SaveToConfig()
        event.Skip()
