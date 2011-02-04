"""
File: TMDBIDSelector.py
Author: Revolt
--------------------------
Desc:
    This file contains the definition and implementation of the dialog
    that allows the user select a new custom TMDB ID based on a search
    by a string.
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

class TMDBIDSelector(wx.Dialog):
    """ The TMDBIDSelector class """

    def __init__(self, parent):
        """
        Constructor 
        """

        # -- Private Variables Initialization --
        self.__logger = logging.getLogger("main")
        self.__resultList = []

        # -- Panel Initialization --
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "Search for an ID")

        # -- Control Initialization --
        self.szrBaseVert = wx.BoxSizer(wx.VERTICAL)
        self.szrSearchHoriz = wx.BoxSizer(wx.HORIZONTAL)
        self.szrListHoriz = wx.BoxSizer(wx.HORIZONTAL)

        self.lblSearch = wx.StaticText(self, wx.ID_ANY, "Search:")
        self.txtSearch = wx.TextCtrl(self, wx.ID_ANY)

        self.szrSearchHoriz.Add(self.lblSearch, 0, wx.ALL, 5)
        self.szrSearchHoriz.Add(self.txtSearch, 1, wx.ALL | wx.EXPAND, 5)

        self.lstTitles = wx.ListView(self, style = wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_SORT_ASCENDING | wx.SUNKEN_BORDER, size=(360, 200))
        self.lstTitles.InsertColumn(0, "Title")
        self.lstTitles.SetColumnWidth(0, 180)
        self.lstTitles.InsertColumn(1, "ID")
        self.lstTitles.SetColumnWidth(1, 180)

        self.szrListHoriz.Add(self.lstTitles, 1, wx.EXPAND | wx.ALL, 5)

        self.szrCustomHoriz = wx.BoxSizer(wx.HORIZONTAL)
        self.szrCustomHoriz.Add(self.radCustom, 0, wx.ALL, 5)
        self.szrCustomHoriz.Add(self.txtCustom, 1, wx.ALL, 5)

        self.szrDialogButtons = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        self.btnOk = self.FindWindowById(wx.ID_OK)
        self.btnCancel = self.FindWindowById(wx.ID_CANCEL)

        self.szrBaseVert.Add(self.radResults, 0, wx.ALL, 5)
        self.szrBaseVert.Add(self.szrListHoriz, 1, wx.EXPAND | wx.ALL, 5)
        self.szrBaseVert.Add(self.szrCustomHoriz, 0, wx.EXPAND | wx.ALL, 5)
        self.szrBaseVert.Add(self.szrDialogButtons, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(self.szrBaseVert)

        # -- Event Binding
        self.lstTitles.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelected)
        self.radResults.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButtonResultsClick)
        self.radCustom.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButtonCustomClick)

        self.btnOk.Bind(wx.EVT_BUTTON, self.OnOk)

        self.PopulateList()


    # -- METHODS --
    def PopulateList(self):
        """ 
        Populates the title list with the titles in the resultList.
        """
        
        self.SetInputResults()

        for result in self.__resultList:
            index = self.lstTitles.InsertStringItem(self.lstTitles.GetItemCount(), GetResultTitle(result))
            self.lstTitles.SetStringItem(index, 1, GetResultID(result))

            if index == self.__selectedIndex:
                self.lstTitles.Select(index)
        else:
            self.SetInputCustom()


    def SetInputResults(self):
        """
        Enables the result listview and selects the results radiobox while
        disabling the custom textbox and radiobutton.
        """

        self.radResults.SetValue(True)
        self.lstTitles.Enable()
        self.txtCustom.Disable()

    def SetInputCustom(self):
        """
        Enables the custom textbox and radiobox while disabling the results
        listview and radiobutton.
        """

        self.radCustom.SetValue(True)
        self.lstTitles.Disable()
        self.txtCustom.Enable()

    def GetSelectedIndex(self):
        """
        Return: (int) The index of the selection.
        """

        return self.__selectedIndex

    # -- EVENTS --
    def OnListItemSelected(self, event):
        """
        Handles a selection in a list view item.
        """

        self.__selectedIndex = event.GetIndex()

    def OnOk(self, event):
        """
        Handles a click on the OK button.
        """

        if self.radCustom.GetValue():
            # If radiobutton 'Custom' is selected, add the title
            # to the result list and set it as selected.

            tmdbId = self.txtCustom.GetValue()

            mdb = tmdb.MovieDb()

            movieInfo = mdb.getMovieInfo(tmdbId)

            if movieInfo is not None:
                self.__resultList.append(movieInfo)
                self.__selectedIndex = len(self.__resultList) - 1

        event.Skip()

    def OnRadioButtonResultsClick(self, event):
        """
        Handles a click on the 'Results' radiobutton.
        """

        self.SetInputResults()

    def OnRadioButtonCustomClick(self, event):
        """
        Handles a click on the 'Custom' radiobutton.
        """

        self.SetInputCustom()
