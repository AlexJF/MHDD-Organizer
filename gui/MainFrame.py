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
from MovieDetailsPanel import *
from HddSelector.HddSelectorDialog import *

# --------------------- Main frame Class -----------------------

class MainFrame(wx.Frame):
    """ The main frame of the application """

    def __init__(self, parent, title):
        """ Constructor """

        # -- Frame Initialization --
        wx.Frame.__init__(self, parent, title=title, size=(700,500))

        # -- Private Variable Declaration --
        self.__currentHdd = None
        self.__categoryList = None
        self.__movieList = None

        # -- Control Initialization --
        self.tlbMain = self.CreateToolBar()
        self.tlbMain.AddTool(wx.ID_ADD, wx.Bitmap("gui/images/add.png", wx.BITMAP_TYPE_PNG), shortHelpString = "Add a new object")
        self.tlbMain.AddTool(wx.ID_REMOVE, wx.Bitmap("gui/images/rem.png", wx.BITMAP_TYPE_PNG), shortHelpString = "Remove a object")

        self.cmbCat = wx.ComboBox(self.tlbMain)
        self.tlbMain.AddControl(self.cmbCat)

        self.tlbMain.Realize()

        self.sptMain = wx.SplitterWindow(self)

        self.pnlMovieList = wx.Panel(self.sptMain)
        self.pnlMovieDetailsBase = wx.Panel(self.sptMain)
        
        self.sptMain.SplitVertically(self.pnlMovieList, self.pnlMovieDetailsBase, 150)
        self.sptMain.SetSashPosition(150)

        self.lstMovie = wx.ListView(self.pnlMovieList, style = wx.LC_REPORT | wx.LC_NO_HEADER | wx.LC_SINGLE_SEL | wx.LC_SORT_ASCENDING | wx.SUNKEN_BORDER)
        self.lstMovie.InsertColumn(0, "Name")
        self.szrBaseMovieList = wx.BoxSizer(wx.VERTICAL)
        self.szrBaseMovieList.Add(self.lstMovie, 1, wx.ALL | wx.EXPAND, 5)

        self.scrMovieDetails = wx.ScrolledWindow(self.pnlMovieDetailsBase)
        self.szrBaseMovieDetails = wx.BoxSizer(wx.VERTICAL)
        self.szrBaseMovieDetails.Add(self.scrMovieDetails, 1, wx.ALL | wx.EXPAND, 5)
        
        self.pnlMovieDetails = MovieDetailsPanel(self.scrMovieDetails)
        self.szrMovieDetails = wx.BoxSizer(wx.VERTICAL)
        self.szrMovieDetails.Add(self.pnlMovieDetails, 1, wx.ALL | wx.EXPAND, 5)

        self.scrMovieDetails.SetSizer(self.szrMovieDetails)
        self.scrMovieDetails.SetScrollRate(5, 5)

        self.pnlMovieList.SetSizer(self.szrBaseMovieList)
        self.pnlMovieDetailsBase.SetSizer(self.szrBaseMovieDetails)

        self.Layout()

        # -- Event Binding -- 
        self.Bind(wx.EVT_SHOW, self.OnShow)
        self.cmbCat.Bind(wx.EVT_COMBOBOX, self.OnCatChanged)
        self.lstMovie.Bind(wx.EVT_SIZE, self.OnMovieListResize)
        self.lstMovie.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnMovieListItemSelect)


    def ChangeHDD(self, hdd):
        """
        Sets the new HDD to be analysed and refreshes the category combobox
        ---
        Params:
            @ hdd (HardDrive) - The new harddrive to be analysed
        """

        if not isinstance(hdd, HardDrive):
            return

        self.__currentHdd = hdd
        self.__categoryList = self.__currentHdd.GetCategoryList()

        for category in self.__categoryList:
            self.cmbCat.Append(category.GetName(), category)

        if len(self.__categoryList) > 0:
            self.cmbCat.SetSelection(0)
            self.PopulateMovieList(self.__categoryList[0])

    def PopulateMovieList(self, category):
        """
        Populates the movie list with movies from the provided category
        ---
        Params:
            @ category (Category) - The category whose movies we want to insert in the list
        """

        self.__movieList = category.GetMovieList()

        for movie in self.__movieList:
            self.lstMovie.InsertStringItem(self.lstMovie.GetItemCount(), movie.GetName())

    # -- EVENTS --

    def OnShow(self, event):
        """ This method is called when the application is shown or hidden """

        if event.GetShow() == True and self.__currentHdd == None:
            hddSelectDialog = HddSelectorDialog(self)

            if hddSelectDialog.ShowModal() == wx.ID_OK:
                self.ChangeHDD(hddSelectDialog.GetSelectedHdd()[1])

    def OnCatChanged(self, event):
        """ This method is called when a user selects a new category in the combobox """

        self.lstMovie.DeleteAllItems()

        selectedCategoryIndex = event.GetSelection()

        category = self.cmbCat.GetClientData(selectedCategoryIndex)
        
        if not category:
            return

        self.PopulateMovieList(category)

    def OnMovieListResize(self, event):
        self.lstMovie.SetColumnWidth(0, event.GetSize().width)
        event.Skip()

    def OnMovieListItemSelect(self, event):
        selectedIndex = event.GetIndex()
        selectedMovie = self.__movieList[selectedIndex]

        self.pnlMovieDetails.SetMovie(selectedMovie)

