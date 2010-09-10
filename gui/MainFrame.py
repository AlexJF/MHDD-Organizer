#! /usr/bin/env python

"""
File: MainFrame.py
Author: Revolt
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
from HddSelector.HddSelectorDialog import *

# --------------------- Main frame Class -----------------------

class MainFrame(wx.Frame):
    """ The main frame of the application """

    currentHDD = None

    def __init__(self, parent, title):
        """ Constructor """

        # -- Frame Initialization --
        wx.Frame.__init__(self, parent, title=title, size=(700,500))

        # -- Private Variable Declaration --
        self._currentHdd = None
        self._currentCat = None

        # -- Control Initialization --
        self.tlbMain = self.CreateToolBar()
        self.tlbMain.AddTool(wx.ID_ADD, wx.Bitmap("gui/images/add.png", wx.BITMAP_TYPE_PNG), shortHelpString = "Add a new object")
        self.tlbMain.AddTool(wx.ID_REMOVE, wx.Bitmap("gui/images/rem.png", wx.BITMAP_TYPE_PNG), shortHelpString = "Remove a object")

        self.cmbCat = wx.ComboBox(self.tlbMain)
        self.tlbMain.AddControl(self.cmbCat)

        self.tlbMain.Realize()

        self.sptMain = wx.SplitterWindow(self)

        self.pnlObjList = wx.Panel(self.sptMain)
        self.pnlObjDetailsBase = wx.Panel(self.sptMain)
        
        self.sptMain.SplitVertically(self.pnlObjList, self.pnlObjDetailsBase, 150)
        self.sptMain.SetSashPosition(150)

        self.lstObj = wx.ListView(self.pnlObjList, style = wx.LC_REPORT | wx.LC_NO_HEADER | wx.LC_SINGLE_SEL | wx.LC_SORT_ASCENDING | wx.SIMPLE_BORDER)
        self.szrBaseObjList = wx.BoxSizer(wx.VERTICAL)
        self.szrBaseObjList.Add(self.lstObj, 1, wx.ALL | wx.EXPAND, 5)

        self.scrObjDetails = wx.ScrolledWindow(self.pnlObjDetailsBase)
        self.szrBaseObjDetails = wx.BoxSizer(wx.VERTICAL)
        self.szrBaseObjDetails.Add(self.scrObjDetails, 1, wx.ALL | wx.EXPAND, 5)
        
        self.pnlObjDetails = ObjectDetailsPanel(self.scrObjDetails)
        self.szrObjDetails = wx.BoxSizer(wx.VERTICAL)
        self.szrObjDetails.Add(self.pnlObjDetails, 1, wx.ALL | wx.EXPAND, 5)

        self.scrObjDetails.SetSizer(self.szrObjDetails)
        self.scrObjDetails.SetScrollRate(5, 5)

        self.pnlObjList.SetSizer(self.szrBaseObjList)
        self.pnlObjDetailsBase.SetSizer(self.szrBaseObjDetails)

        self.Layout()

        # -- Event Binding -- 
        self.Bind(wx.EVT_SHOW, self.OnShow)


    def ChangeHDD(self, hdd):
        """
        Sets the new HDD to be analysed and refreshes the category combobox
        ---
        Params:
            @ hdd (HardDrive) - The new harddrive to be analysed
        """

        if not isinstance(hdd, HardDrive):
            return

        self._currentHdd = hdd
        self._currentCat = None

        if self._currentHdd != None:
            self._currentHdd.LoadCategoryList()

        for category in self._currentHdd.GetCategoryList():
            self.cmbCat.Append(category.GetName(), category)

    # -- EVENTS --

    def OnShow(self, event):
        """ This method is called when the application is shown or hidden """

        if event.GetShow() == True and self.currentHDD == None:
            hddSelectDialog = HddSelectorDialog(self)

            if hddSelectDialog.ShowModal() == wx.ID_OK:
                self.ChangeHDD(hddSelectDialog.GetSelectedHdd()[1])


