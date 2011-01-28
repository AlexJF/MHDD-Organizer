"""
File: IMDBSearchResultDialog.py
Author: Revolt
--------------------------
Desc:
    This file contains the definition and implementation of the dialog
    that allows the user to choose which IMDB title from the results
    gathered in the IMDB search matches the selected movie object.
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
from imdb import IMDb

class IMDBSearchResultDialog(wx.Dialog):
    """ The IMDBSearchResultDialog class """

    def __init__(self, parent, movieName, resultList, selectedIndex = -1):
        """
        Constructor 
        ---
        Params:
            @ movieName (String) - The name of the movie whose IMDB title
                                   we wish to select.
            @ resultList (List of Strings) - The list of results retrieved
                                   from the IMDB search.
            @ selectedIndex (int) - The index of the result corrently
                                    associated with the movie.
        """

        # -- Private Variables Initialization --
        self.__logger = logging.getLogger("main")
        self.__resultList = resultList
        self.__selectedIndex = selectedIndex

        # -- Panel Initialization --
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "Select title for '" + movieName + "'")

        # -- Control Initialization --
        self.szrBaseVert = wx.BoxSizer(wx.VERTICAL)
        self.szrListHoriz = wx.BoxSizer(wx.HORIZONTAL)

        self.lstTitles = wx.ListView(self, style = wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_SORT_ASCENDING | wx.SUNKEN_BORDER, size=(360, 200))
        self.lstTitles.InsertColumn(0, "Title")
        self.lstTitles.SetColumnWidth(0, 180)
        self.lstTitles.InsertColumn(1, "ID")
        self.lstTitles.SetColumnWidth(1, 180)

        self.szrListHoriz.Add(self.lstTitles, 1, wx.EXPAND | wx.ALL, 5)

        self.szrDialogButtons = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        self.btnOk = self.FindWindowById(wx.ID_OK)
        self.btnCancel = self.FindWindowById(wx.ID_CANCEL)

        self.szrBaseVert.Add(self.szrListHoriz, 1, wx.EXPAND | wx.ALL, 5)
        self.szrBaseVert.Add(self.szrDialogButtons, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(self.szrBaseVert)

        # -- Event Binding
        self.lstTitles.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelected)

        self.PopulateList()

    def PopulateList(self):
        """ 
        Populates the title list with the titles in the resultList.
        """

        for result in self.__resultList:
            index = self.lstTitles.InsertStringItem(self.lstTitles.GetItemCount(), result['title'])
            self.lstTitles.SetStringItem(index, 1, result.movieID)

            if index == self.__selectedIndex:
                self.lstTitles.Select(index)

    # -- EVENTS --
    def OnListItemSelected(self, event):
        """
        Handles a selection in a list view item.
        """

        self.__selectedIndex = event.GetIndex()

    # -- METHODS --
    def GetSelectedIndex(self):
        """
        Return: (int) The index of the selection.
        """

        return self.__selectedIndex
