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
from appinfo import *
from operator import methodcaller
from gui.panels.MovieDetailsPanel import *
from gui.dialogs.HddSelectorDialog import *
from gui.dialogs.TMDBSearchDialog import *
from classes.filters.FilterName import *
from classes.filters.FilterTMDB import *

# --------------------- Main frame Class -----------------------

class MainFrame(wx.Frame):
    """ The main frame of the application """

    ID_TMDB = 100
    ID_TMDB_SEARCHNEW = 101
    ID_TMDB_REFRESH = 102

    def __init__(self, parent, title):
        """ Constructor """

        # -- Frame Initialization --
        wx.Frame.__init__(self, parent, title=title, size=(700,500))

        # -- Private Variable Declaration --
        self.__currentHdd = None
        self.__categoryList = None
        self.__currentCategory = None
        self.__movieList = None
        self.__selectedMovie = None

        # -- Control Initialization --
        self.mnbMain = wx.MenuBar()
        
        self.mnuMain = wx.Menu()
        self.mnuMain.Append(wx.ID_OPEN, "Select Harddrive")
        self.mnuMain.AppendSeparator()
        self.mnuMain.Append(wx.ID_EXIT, "Exit")

        self.mnuTMDB = wx.Menu()
        self.mnuTMDB.Append(self.ID_TMDB_SEARCHNEW, "Search new movies in TMDB")
        self.mnuTMDB.Append(self.ID_TMDB_REFRESH, "Refresh existing TMDB data")

        self.mnuTools = wx.Menu()
        imdbMenuItem = self.mnuTools.AppendMenu(self.ID_TMDB, "TMDB", self.mnuTMDB)
        #self.mnuTools.AppendSeparator()
        #self.mnuTools.Append(wx.ID_PREFERENCES, "Preferences")

        self.mnuHelp = wx.Menu()
        #self.mnuHelp.Append(wx.ID_HELP, "Help")
        #self.mnuHelp.AppendSeparator()
        self.mnuHelp.Append(wx.ID_ABOUT, "About")

        self.mnbMain.Append(self.mnuMain, "&Main")
        self.mnbMain.Append(self.mnuTools, "&Tools")
        self.mnbMain.Append(self.mnuHelp, "&Help")

        self.SetMenuBar(self.mnbMain)

        self.tlbMain = self.CreateToolBar()
        self.tlbMain.SetMargins((5, 5))

        self.tlbMain.AddLabelTool(wx.ID_OPEN, "Select Harddrive.", 
                                  wx.Bitmap("gui/images/hdd-on.png"),
                                  shortHelp = "Select Harddrive.")
        self.tlbMain.AddLabelTool(wx.ID_REFRESH, "Reload Harddrive.", 
                                  wx.Bitmap("gui/images/hdd-reload.png"),
                                  shortHelp = "Reload Harddrive")

        self.tlbMain.AddSeparator()

        self.lblCat = wx.StaticText(self.tlbMain, wx.ID_ANY, "Category: ")
        self.cmbCat = wx.ComboBox(self.tlbMain, wx.ID_ANY, size = (-1, 23))
        self.tlbMain.AddControl(self.lblCat)
        self.tlbMain.AddControl(self.cmbCat)

        self.tlbMain.AddSeparator()

        self.lblSearch = wx.StaticText(self.tlbMain, wx.ID_ANY, "Search: ")
        self.txtSearch = wx.TextCtrl(self.tlbMain, wx.ID_ANY, size = (150, 23), style = wx.TE_PROCESS_ENTER)
        self.tlbMain.AddControl(self.lblSearch)
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
        self.Bind(wx.EVT_MENU, self.OnMenuSelectExit, id = wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnMenuSelectHardDrive, id = wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.OnMenuSelectTMDBSearch, id = self.ID_TMDB_SEARCHNEW)
        self.Bind(wx.EVT_MENU, self.OnMenuSelectTMDBRefresh, id = self.ID_TMDB_REFRESH)
        self.Bind(wx.EVT_MENU, self.OnMovieListRefresh, id = wx.ID_REFRESH)
        self.Bind(wx.EVT_MENU, self.OnAbout, id = wx.ID_ABOUT)

        self.txtSearch.Bind(wx.EVT_TEXT_ENTER, self.OnMovieSearch)
        self.cmbCat.Bind(wx.EVT_COMBOBOX, self.OnCatChanged)
        self.lstMovie.Bind(wx.EVT_SIZE, self.OnMovieListResize)
        self.lstMovie.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnMovieListItemSelect)

        self.Bind(wx.EVT_CLOSE, self.OnClose)


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

        if self.__categoryList is None:
            return

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
        self.RefreshMovieList()

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

    def RefreshMovieList(self):
        """
        (Re)reads the movie list from the HDD (or cache) and updates the listview.
        """

        dsbWindow = wx.WindowDisabler()
        infBusy = wx.BusyInfo("Please wait...", self)
        self.__movieList = self.__currentCategory.GetMovieList()
        if self.__movieList is not None:
            self.__movieList.sort(key = methodcaller("GetName"))

        self.PopulateMovieList()
        if self.lstMovie.GetItemCount() > 0:
            self.lstMovie.Select(0)
        del infBusy
        del dsbWindow

    def ShowTMDBDialog(self, movieList):
        """
        Shows the TMDB search dialog populated with the provided movie list.
        ---
        Params:
            @ movieList (List of Movies) - The list of movies whose info we wish to get/refresh
                                           from TMDB.
        """

        if movieList is None or len(movieList) == 0:
            return

        dlgTMDBResults = TMDBSearchDialog(self, movieList)

        if dlgTMDBResults.ShowModal() == wx.ID_OK:
            self.RefreshTMDBInfo(movieList)

    def RefreshTMDBInfo(self, movieList):
        """
        Refreshes the TMDB info of each movie in the provided Movie list.
        ---
        Params:
            @ movieList (List of Movies) - The list of movies whose info we wish to refresh
                                           from TMDB.
        """

        dlgProgress = wx.ProgressDialog("Getting TMDB info...", "Preparing TMDB Loading.............................", 
                                        len(movieList), self, wx.PD_AUTO_HIDE | 
                                        wx.PD_CAN_ABORT)

        i = 1

        for movie in movieList:
            shouldContinue, shouldSkip = dlgProgress.Update(i, "Getting info for '" + movie.GetName() + "'")

            if not shouldContinue:
                dlgProgress.Show(False)
                return

            movie.LoadInfoFromTMDB()
            movie.SaveInfoToHdd()

            if movie == self.__selectedMovie:
                self.pnlMovieDetails.SetMovie(movie)

            i += 1

    # -- EVENTS --
    def OnMenuSelectHardDrive(self, event):
        """
        This method is called when the user clicks on the Select Harddrive menu entry.
        """

        self.SelectHDD()

    def OnMenuSelectTMDBSearch(self, event):
        """
        This method is called when the user clicks on the TMDB Search New menu entry.
        """

        tmdbFilter = FilterTMDB()
        noTMDBMovies = tmdbFilter.FilterList(self.__movieList)

        self.ShowTMDBDialog(noTMDBMovies)

    def OnMenuSelectTMDBRefresh(self, event):
        """
        This method is called when the user clicks on the TMDB Refresh menu entry.
        """

        self.RefreshTMDBInfo(self.__movieList)

    def OnMenuSelectExit(self, event):
        """
        This method is called when the user clicks the exit menu entry.
        """

        self.Close()

    def OnCatChanged(self, event):
        """ 
        This method is called when a user selects a new category in the combobox.
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
        self.__selectedMovie = self.__movieList[i]

        self.pnlMovieDetails.SetMovie(self.__selectedMovie)

    def OnMovieSearch(self, event):
        """
        This method is called when the user clicks the search button.
        """

        searchString = self.txtSearch.GetValue()

        nameFilter = None

        if not searchString.isspace():
            nameFilter = FilterName(searchString)

        self.PopulateMovieList(nameFilter)

    def OnMovieListRefresh(self, event):
        """
        This method is called when the user clicks the refresh movie list button.
        """

        self.RefreshMovieList()

    def OnAbout(self, event):
        """
        This method is called when the user clicks the about button.
        """
        
        global appInfo
        aboutInfo = wx.AboutDialogInfo()

        aboutInfo.SetName(appInfo['name'])
        aboutInfo.SetVersion(appInfo['version'])
        aboutInfo.SetDescription(appInfo['description'])
        aboutInfo.SetCopyright(appInfo['copyright'])
        aboutInfo.SetLicense(appInfo['license'])
        aboutInfo.SetDevelopers(appInfo['developers'])

        wx.AboutBox(aboutInfo)

    def OnClose(self, event):
        """
        This method is called when the user wants to close the mainframe.
        """

        del self.__selectedMovie
        del self.__currentCategory
        del self.__categoryList
        del self.__currentHdd
        del self.__movieList

        self.Destroy()

