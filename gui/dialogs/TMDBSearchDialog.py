"""
File: TMDBSearchDialog.py
Author: Revolt
--------------------------
Desc:
    This file contains the definition and implementation of the dialog
    that allows the user to choose the correct title from a collection
    of titles retrieved from TMDB.
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
from classes.infoproviders import tmdb
from common import GetResultTitle, GetResultID
from TMDBSearchResultDialog import *

class TMDBSearchDialog(wx.Dialog):
    """ The TMDBSearchDialog class """

    def __init__(self, parent, movieList):
        """
        Constructor 
        ---
        Params:
            @ movieList (List of Movies) - The list of movies that we
                        wish to choose TMDB titles for.
        """

        # -- Private Variables Initialization --
        self.__logger = logging.getLogger("mhdd.dialog.tmdbsearch")
        self.__movieList = movieList
        self.__resultCache = []

        # -- Panel Initialization --
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "TMDB Search Results")

        # -- Control Initialization --
        self.szrBaseVert = wx.BoxSizer(wx.VERTICAL)
        self.szrListHoriz = wx.BoxSizer(wx.HORIZONTAL)

        self.lstResults = wx.ListView(self, style = wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_SORT_ASCENDING | wx.SUNKEN_BORDER, size=(540, 200))
        self.lstResults.InsertColumn(0, "Name")
        self.lstResults.SetColumnWidth(0, 180)
        self.lstResults.InsertColumn(1, "Title")
        self.lstResults.SetColumnWidth(1, 180)
        self.lstResults.InsertColumn(2, "ID")
        self.lstResults.SetColumnWidth(2, 180)

        self.szrListHoriz.Add(self.lstResults, 1, wx.EXPAND | wx.ALL, 5)

        self.lblTMDBAttribution = wx.StaticText(self, wx.ID_ANY, "This product uses the TMDb API but is not endorsed or certified by TMDb.")

        self.szrDialogButtons = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        self.btnOk = self.FindWindowById(wx.ID_OK)
        self.btnCancel = self.FindWindowById(wx.ID_CANCEL)

        self.szrBaseVert.Add(self.szrListHoriz, 1, wx.EXPAND | wx.ALL, 5)
        self.szrBaseVert.Add(self.lblTMDBAttribution, 0, wx.EXPAND | wx.ALL, 5)
        self.szrBaseVert.Add(self.szrDialogButtons, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.SetSizerAndFit(self.szrBaseVert)

        # -- Event Binding
        self.lstResults.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnListItemActivated)
        self.btnOk.Bind(wx.EVT_BUTTON, self.OnButtonOkClick)

        self.PopulateList()

    def PopulateList(self):
        """ 
        Searches TMDB for all movies in the movie list.
        """

        self.__logger.debug("Started searching TMDB")

        mdb = tmdb.MovieDb()

        dlgProgress = wx.ProgressDialog("Searching TMDB...", 
                                        "Preparing Search.......................................", 
                                        len(self.__movieList), self, 
                                        wx.PD_AUTO_HIDE | wx.PD_CAN_ABORT \
                                                        | wx.PD_APP_MODAL)

        i = 1

        for movie in self.__movieList:
            shouldContinue, shouldSkip = dlgProgress.Update(i, "Searching for '" + movie.GetName() + "'...")

            if not shouldContinue:
                dlgProgress.Show(False)
                return

            results = []

            try:
                results = mdb.search(movie.GetName())
                self.__resultCache.append(results)
            except tmdb.TmdBaseError, e:
                self.__logger.exception("Failed to perform TMDB search.")
                wx.MessageBox("Failed to perform TMDB search for " + movie.GetName(),
                              "Error", wx.ID_OK | wx.ICON_ERROR, self)
                break

            self.__logger.debug("Found %d results for '%s'", len(results), movie.GetName())

            index = self.lstResults.InsertStringItem(self.lstResults.GetItemCount(), movie.GetName())

            tmdbID = movie.GetTMDBID()
            resultIndex = 0
            resultTitle = ""
            resultID = ""

            # If the movie doesn't have a TMDB ID set then just use the results
            if tmdbID == "" or tmdbID.isspace():
                if len(results) == 0:
                    resultIndex = -1
                    resultTitle = "No title found"
                else:
                    resultTitle = GetResultTitle(results[0])
                    resultID = GetResultID(results[0])
            else:
                found = False
                j = 0

                for result in results:
                    if result['id'] == tmdbID:
                        resultIndex = j
                        resultTitle = GetResultTitle(result)
                        resultID = GetResultID(result)
                        found = True
                        break
                    j += 1

                # If the movie's TMDB ID isn't contained in the results, add it to it
                if not found:
                    newResult = mdb.getMovieInfo(tmdbID)
                    results.append(newResult)
                    resultIndex = len(results) - 1
                    resultTitle = GetResultTitle(newResult)
                    resultID = GetResultID(newResult)

            self.__logger.debug(movie.GetName() + " - " + str(resultIndex) + ", " + resultTitle + ", " + resultID)

            self.lstResults.SetItemData(index, resultIndex)
            self.lstResults.SetStringItem(index, 1, resultTitle)
            self.lstResults.SetStringItem(index, 2, resultID)

            i += 1


    # -- EVENTS --
    def OnListItemActivated(self, event):
        """
        Handles a double click in a list view item.
        """

        selectedIndex = event.GetIndex()
        movie = self.__movieList[selectedIndex]
        results = self.__resultCache[selectedIndex]
        currentResultIndex = self.lstResults.GetItemData(selectedIndex)

        dlgSearchResultSelect = TMDBSearchResultDialog(self, movie.GetName(), results, currentResultIndex)

        if dlgSearchResultSelect.ShowModal() == wx.ID_OK:
            currentResultIndex = dlgSearchResultSelect.GetSelectedIndex()
            currentResultList = dlgSearchResultSelect.GetResultList()

            self.__resultCache[selectedIndex] = currentResultList
            self.lstResults.SetItemData(selectedIndex, currentResultIndex)

            if currentResultIndex != -1:
                selectedResult = currentResultList[currentResultIndex]
                self.lstResults.SetStringItem(selectedIndex, 1, GetResultTitle(selectedResult))
                self.lstResults.SetStringItem(selectedIndex, 2, GetResultID(selectedResult))
            else:
                self.lstResults.SetStringItem(selectedIndex, 1, "None")
                self.lstResults.SetStringItem(selectedIndex, 2, "")

    def OnButtonOkClick(self, event):
        """
        Handles a click in the Ok button of the dialog.
        """

        index = 0

        for results in self.__resultCache:
            movie = self.__movieList[index]
            selectedResultIndex = self.lstResults.GetItemData(index)
            index += 1

            if selectedResultIndex == -1:
                continue
            
            selectedResult = results[selectedResultIndex]

            movie.SetTMDBID(GetResultID(selectedResult))

        event.Skip()
