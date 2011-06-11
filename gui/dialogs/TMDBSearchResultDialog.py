"""
File: TMDBSearchResultDialog.py
Author: Revolt
--------------------------
Desc:
    This file contains the definition and implementation of the dialog
    that allows the user to choose which TMDB title from the results
    gathered in the TMDB search matches the selected movie object.
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


import wx, logging
from common import GetResultTitle, GetResultID
from classes.infoproviders import tmdb

class TMDBSearchResultDialog(wx.Dialog):
    """ The TMDBSearchResultDialog class """

    def __init__(self, parent, movieName, resultList, selectedIndex = -1):
        """
        Constructor 
        ---
        Params:
            @ movieName (String) - The name of the movie whose TMDB title
                                   we wish to select.
            @ resultList (List of Strings) - The list of results retrieved
                                   from the TMDB search.
            @ selectedIndex (int) - The index of the result corrently
                                    associated with the movie.
        """

        # -- Private Variables Initialization --
        self.__logger = logging.getLogger("mhdd.dialog.tmdbsearchresult")
        self.__resultList = resultList
        self.__selectedIndex = selectedIndex

        # -- Panel Initialization --
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "Select title for '" + movieName + "'")

        # -- Control Initialization --
        self.szrBaseVert = wx.BoxSizer(wx.VERTICAL)
        self.szrSearchHoriz = wx.BoxSizer(wx.HORIZONTAL)
        self.szrListHoriz = wx.BoxSizer(wx.HORIZONTAL)

        self.lblSearch = wx.StaticText(self, wx.ID_ANY, "New Search:")
        self.txtSearch = wx.TextCtrl(self, wx.ID_ANY, value = movieName, style = wx.TE_PROCESS_ENTER)

        self.szrSearchHoriz.Add(self.lblSearch, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.szrSearchHoriz.Add(self.txtSearch, 1, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.lstTitles = wx.ListView(self, style = wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_SORT_ASCENDING | wx.SUNKEN_BORDER, size=(360, 200))
        self.lstTitles.InsertColumn(0, "Title")
        self.lstTitles.SetColumnWidth(0, 180)
        self.lstTitles.InsertColumn(1, "ID")
        self.lstTitles.SetColumnWidth(1, 180)

        self.szrListHoriz.Add(self.lstTitles, 1, wx.EXPAND | wx.ALL, 5)

        self.szrDialogButtons = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        self.btnOk = self.FindWindowById(wx.ID_OK)
        self.btnCancel = self.FindWindowById(wx.ID_CANCEL)

        self.szrBaseVert.Add(self.szrSearchHoriz, 0, wx.ALL | wx.EXPAND, 5)
        self.szrBaseVert.Add(self.szrListHoriz, 1, wx.EXPAND | wx.ALL, 5)
        self.szrBaseVert.Add(self.szrDialogButtons, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(self.szrBaseVert)

        # -- Event Binding
        self.lstTitles.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelected)
        self.txtSearch.Bind(wx.EVT_TEXT_ENTER, self.OnSearchEnter)

        self.PopulateList()


    # -- METHODS --
    def PopulateList(self):
        """ 
        Populates the title list with the titles in the resultList.
        """

        self.lstTitles.DeleteAllItems()

        found = False
        
        for result in self.__resultList:
            index = self.lstTitles.InsertStringItem(self.lstTitles.GetItemCount(), GetResultTitle(result))
            self.lstTitles.SetStringItem(index, 1, GetResultID(result))

            if index == self.__selectedIndex:
                found = True
                self.lstTitles.Select(index)

        index = self.lstTitles.InsertStringItem(self.lstTitles.GetItemCount(), "None")

        if not found:
            self.lstTitles.Select(index)

    def GetSelectedIndex(self):
        """
        Return: (int) The index of the selection.
        """

        if self.__selectedIndex >= len(self.__resultList):
            return -1
        else:
            return self.__selectedIndex

    def GetResultList(self):
        """
        Return: (List of Results) The current list of results.
        """

        return self.__resultList

    # -- EVENTS --
    def OnListItemSelected(self, event):
        """
        Handles a selection in a list view item.
        """

        self.__selectedIndex = event.GetIndex()

    def OnSearchEnter(self, event):
        """
        Handles a return in the search textbox.
        """

        searchStr = self.txtSearch.GetValue()

        mdb = tmdb.MovieDb()
        self.__resultList = []
        try:
            self.__resultList = mdb.search(searchStr)
            self.__logger.debug("Got %d results from TMDB search for '%s'",
                                len(self.__resultList), searchStr)
        except tmdb.TmdBaseError, e:
            wx.MessageBox("Error while performing your query to TMDB:" + str(e),
                          "Error", wx.ID_OK | wx.ICON_ERROR, self)
            self.__logger.exception("Failed to perform TMDB search.")

        self.PopulateList()
