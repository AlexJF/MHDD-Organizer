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
from classes.filters.FilterName import *

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
        self.__currentCategory = None
        self.__movieList = None

        # -- Control Initialization --
        self.mnbMain = wx.MenuBar()
        
        self.mnuMain = wx.Menu()
        self.mnuMain.Append(wx.ID_OPEN, "Select Harddrive")
        self.mnuMain.AppendSeparator()
        self.mnuMain.Append(wx.ID_EXIT, "Exit")

        self.mnuView = wx.Menu()
        self.mnuView.AppendCheckItem(wx.ID_VIEW_LIST, "View as List")
        self.mnuView.AppendCheckItem(wx.ID_VIEW_SMALLICONS, "View as Icons")
        self.mnuView.AppendCheckItem(wx.ID_VIEW_SORTNAME, "Sort by Name")
        self.mnuView.AppendCheckItem(wx.ID_VIEW_SORTDATE, "Sort by Date")
        self.mnuView.AppendCheckItem(wx.ID_VIEW_SORTSIZE, "Sort by Size")

        self.mnuTools = wx.Menu()
        self.mnuTools.Append(wx.ID_PREFERENCES, "Preferences")

        self.mnuHelp = wx.Menu()
        self.mnuHelp.Append(wx.ID_HELP, "Help")
        self.mnuHelp.AppendSeparator()
        self.mnuHelp.Append(wx.ID_ABOUT, "About")

        self.mnbMain.Append(self.mnuMain, "&Main")
        self.mnbMain.Append(self.mnuView, "&View")
        self.mnbMain.Append(self.mnuTools, "&Tools")
        self.mnbMain.Append(self.mnuHelp, "&Help")

        self.SetMenuBar(self.mnbMain)

        self.tlbMain = self.CreateToolBar()
        self.tlbMain.AddTool(wx.ID_ADD, wx.Bitmap("gui/images/add.png", wx.BITMAP_TYPE_PNG), shortHelpString = "Add a new object")
        self.tlbMain.AddTool(wx.ID_REMOVE, wx.Bitmap("gui/images/rem.png", wx.BITMAP_TYPE_PNG), shortHelpString = "Remove a object")
        self.tlbMain.AddSeparator()

        self.cmbCat = wx.ComboBox(self.tlbMain, wx.ID_ANY, size = (-1, 23))
        self.tlbMain.AddControl(self.cmbCat)
        self.tlbMain.AddSeparator()

        self.txtSearch = wx.TextCtrl(self.tlbMain, wx.ID_ANY, size = (150, 23), style = wx.TE_PROCESS_ENTER)
        self.tlbMain.AddControl(self.txtSearch)

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
        self.Bind(wx.EVT_MENU, self.OnMenuSelectHardDrive, id = wx.ID_OPEN)

        self.txtSearch.Bind(wx.EVT_TEXT_ENTER, self.OnMovieSearch)
        self.cmbCat.Bind(wx.EVT_COMBOBOX, self.OnCatChanged)
        self.lstMovie.Bind(wx.EVT_SIZE, self.OnMovieListResize)
        self.lstMovie.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnMovieListItemSelect)


    def SelectHDD(self):
        """
        Shows the hdd selection dialog and changes the current hdd
        according to that selection
        """

        hddSelectDialog = HddSelectorDialog(self)

        if hddSelectDialog.ShowModal() == wx.ID_OK:
            self.ChangeHDD(hddSelectDialog.GetSelectedHdd()[1])

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
            self.cmbCat.Append(category.GetName())

        if len(self.__categoryList) > 0:
            self.cmbCat.SetSelection(0)
            self.ChangeCat(self.__categoryList[0])

    def ChangeCat(self, cat):
        """
        Sets the new active Category
        ---
        Params:
            @ cat (Category) - The new active category
        """

        self.__currentCategory = cat
        self.__movieList = cat.GetMovieList()
        self.PopulateMovieList()

    def PopulateMovieList(self, condition = None):
        """
        Populates the movie list with movies from the selected category
        ---
        Params:
            @  condition (Filter) - The condition with which to filter the movie list
        """

        self.lstMovie.DeleteAllItems()

        if self.__movieList is None:
            return

        i = 0

        for movie in self.__movieList:
            if condition is None or condition.Test(movie):
                index = self.lstMovie.InsertStringItem(self.lstMovie.GetItemCount(), movie.GetName())
                self.lstMovie.SetItemData(index, i)

            i += 1

    # -- EVENTS --
    def OnMenuSelectHardDrive(self, event):
        """
        This method is called when the user clicks on the Select Harddrive menu entry.
        """

        self.SelectHDD()

    def OnCatChanged(self, event):
        """ 
        This method is called when a user selects a new category in the combobox 
        """

        self.lstMovie.DeleteAllItems()

        selectedCategoryIndex = event.GetSelection()

        category = self.__categoryList[selectedCategoryIndex]
        
        self.ChangeCat(category)

    def OnMovieListResize(self, event):
        """
        This method is called when the user resizes the splitter window and thus the list.
        """

        self.lstMovie.SetColumnWidth(0, event.GetSize().width)
        event.Skip()

    def OnMovieListItemSelect(self, event):
        """
        This method is called when the user selects a movie from the list.
        """

        selectedIndex = event.GetIndex()
        i = self.lstMovie.GetItemData(selectedIndex)
        selectedMovie = self.__movieList[i]

        self.pnlMovieDetails.SetMovie(selectedMovie)

    def OnMovieSearch(self, event):
        """
        This method is called when the user clicks the search button.
        """

        searchString = self.txtSearch.GetValue()

        nameFilter = None

        if not searchString.isspace():
            nameFilter = FilterName(searchString)

        self.PopulateMovieList(nameFilter)
