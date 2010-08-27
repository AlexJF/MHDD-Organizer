#! /usr/bin/env python

"""
File: HDDSelectorDialog.py
Author: Revolt
Date: 26-08-2010
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


import wx, os, uuid
from HDDAddDialog import *

class HDDSelectorDialog(wx.Dialog):
    """ The HDD Selector Dialog class """

    hddUuidList = []

    def __init__(self, parent):
        """ Constructor """

        # -- Panel Initialization --
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "Please Select a MHDD")

        # -- Control Initialization --
        self.szrBaseVert = wx.BoxSizer(wx.VERTICAL)
        self.szrBaseHori = wx.BoxSizer(wx.HORIZONTAL)

        self.lstHDD = wx.ListView(self, style = wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_SORT_ASCENDING | wx.SIMPLE_BORDER)
        self.lstHDD.InsertColumn(0, "Label")
        self.lstHDD.SetColumnWidth(0, 180)
        self.lstHDD.InsertColumn(1, "Path")
        self.lstHDD.SetColumnWidth(1, 200)

        self.lstHDDImageList = wx.ImageList(22, 22)
        self.lstHDDImageList.Add(wx.Bitmap("gui/images/hdd-off.png", wx.BITMAP_TYPE_PNG))
        self.lstHDDImageList.Add(wx.Bitmap("gui/images/hdd-on.png", wx.BITMAP_TYPE_PNG))

        self.lstHDD.SetImageList(self.lstHDDImageList, wx.IMAGE_LIST_SMALL)

        self.szrButtonsVert = wx.BoxSizer(wx.VERTICAL)

        self.btnAdd = wx.BitmapButton(self, bitmap=wx.Bitmap("gui/images/add.png", wx.BITMAP_TYPE_PNG))
        self.btnRem = wx.BitmapButton(self, bitmap=wx.Bitmap("gui/images/rem.png", wx.BITMAP_TYPE_PNG))
        self.btnEdit = wx.BitmapButton(self, bitmap=wx.Bitmap("gui/images/edit.png", wx.BITMAP_TYPE_PNG))
        self.btnRefresh = wx.BitmapButton(self, bitmap=wx.Bitmap("gui/images/refresh.png", wx.BITMAP_TYPE_PNG))

        self.szrButtonsVert.Add(self.btnAdd, 1, wx.ALL, 5)
        self.szrButtonsVert.Add(self.btnRem, 1, wx.ALL, 5)
        self.szrButtonsVert.Add(self.btnEdit, 1, wx.ALL, 5)
        self.szrButtonsVert.Add(self.btnRefresh, 1, wx.ALL, 5)

        self.szrBaseHori.Add(self.lstHDD, 1, wx.ALL | wx.EXPAND, 5)
        self.szrBaseHori.Add(self.szrButtonsVert, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.szrDialogButtons = self.CreateButtonSizer(wx.OK | wx.CANCEL)

        self.szrBaseVert.Add(self.szrBaseHori, 1, wx.EXPAND | wx.ALL, 5)
        self.szrBaseVert.Add(self.szrDialogButtons, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(self.szrBaseVert)

        self.btnAdd.Bind(wx.EVT_BUTTON, self.OnHDDAdd)
        self.btnRem.Bind(wx.EVT_BUTTON, self.OnHDDRem)
        self.btnRefresh.Bind(wx.EVT_BUTTON, self.OnHDDRefresh)

        self.RefreshHDDList()

    def RefreshHDDList(self):
        """ Refreshes the list of HDDs """

        self.lstHDD.DeleteAllItems()
        self.hddUuidList = []

        config = wx.Config.Get()
        config.SetPath("/drives")

        (groupmore, groupvalue, groupnextindex) = config.GetFirstGroup()

        uuidIndex = 0

        while groupmore:
            hddLabel = config.Read(groupvalue + "/Label")
            hddPath = config.Read(groupvalue + "/Path")

            if hddLabel and hddPath:
                hddConnected = os.path.isdir(hddPath)

                self.hddUuidList.append(groupvalue)

                index = self.lstHDD.InsertImageStringItem(self.lstHDD.GetItemCount(), hddLabel, int(hddConnected))
                self.lstHDD.SetItemData(index, uuidIndex)
                self.lstHDD.SetStringItem(index, 1, hddPath)
                uuidIndex += 1
        
            (groupmore, groupvalue, groupnextindex) = config.GetNextGroup(groupnextindex)


    def GetSelectedHDD(self):
        """ Returns the HDD selected by the user in the list """

        return "Test"

    #-------- EVENTS ---------

    def OnHDDAdd(self, event):
        """ Shows the HDD Add dialog and handles insertion of HDD to the config and list """

        dlgHddAdd = HDDAddDialog(self)

        if dlgHddAdd.ShowModal() == wx.ID_OK:
            newHddLabel = dlgHddAdd.GetHDDLabel()
            newHddPath = dlgHddAdd.GetHDDPath()

            print newHddLabel
            print newHddPath

            config = wx.Config.Get()
            config.SetPath("/drives")

            newHddUuidStr = str(uuid.uuid4())

            while config.HasGroup(newHddUuidStr):
                newHddUuidStr = str(uuid.uuid4())

            config.SetPath(newHddUuidStr)
            print config.GetPath()
            config.Write("Label", newHddLabel)
            config.Write("Path", newHddPath)
            #config.Flush()
            
            self.RefreshHDDList()

    def OnHDDRem(self, event):
        """ Removes the selected HDD from the list and config """

        indexSelectedItem = self.lstHDD.GetFirstSelected()

        if indexSelectedItem == -1:
            return

        hddUuid = self.hddUuidList[self.lstHDD.GetItemData(indexSelectedItem)]

        if not hddUuid:
            return

        config = wx.Config.Get()
        config.SetPath("/drives")

        if config.HasGroup(hddUuid):
            config.DeleteGroup(hddUuid)

        self.RefreshHDDList()

    def OnHDDRefresh(self, event):
        """ Refreshes the HDD list """

        self.RefreshHDDList()
