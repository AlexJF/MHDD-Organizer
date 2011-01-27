#! /usr/bin/env python

"""
File: IMDBSearchDialog.py
Author: Revolt
--------------------------
Desc:
    This file contains the definition and implementation of the dialog
    that allows the user to choose the correct title from a collection
    of titles retrieved from IMDB.
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

class IMDBSearchDialog(wx.Dialog):
    """ The IMDBSearchDialog class """

    def __init__(self, parent, movieList):
        """
        Constructor 
        ---
        Params:
            @ movieList (List of Movies) - The list of movies that we
                        wish to choose IMDB titles for.
        """

        # -- Private Variables Initialization --
        self.__logger = logging.getLogger("main")
        self.__movieList = movieList
        self.__resultCache = []

        # -- Panel Initialization --
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "IMDB Search Results")

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

        self.szrDialogButtons = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        self.btnOk = self.FindWindowById(wx.ID_OK)
        self.btnCancel = self.FindWindowById(wx.ID_CANCEL)

        self.szrBaseVert.Add(self.szrListHoriz, 1, wx.EXPAND | wx.ALL, 5)
        self.szrBaseVert.Add(self.szrDialogButtons, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(self.szrBaseVert)

        # -- Event Binding
        self.lstResults.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnListItemActivated)
        self.btnOk.Bind(wx.EVT_BUTTON, self.OnButtonOkClick)

        self.PopulateList()

    def PopulateList(self):
        """ 
        Searches IMDB for all movies in the movie list.
        """

        self.__logger.debug("Started searching IMDB")

        ia = IMDb()

        dlgProgress = wx.ProgressDialog("Searching IMDB...", "Preparing Search...", 
                                        len(self.__movieList), self, wx.PD_AUTO_HIDE | 
                                        wx.PD_CAN_ABORT)
        i = 1

        for movie in self.__movieList:
            shouldContinue, shouldSkip = dlgProgress.Update(i, "Searching for '" + movie.GetName() + "'...")

            if not shouldContinue:
                dlgProgress.Show(False)
                return

            results = ia.search_movie(movie.GetName())
            self.__resultCache.append(results)

            self.__logger.debug("Found %d results for '%s'", len(results), movie.GetName())

            index = self.lstResults.InsertStringItem(self.lstResults.GetItemCount(), movie.GetName())

            imdbID = movie.GetIMDBID()
            resultIndex = 0
            resultTitle = ""
            resultID = ""

            # If the movie doesn't have an IMDB ID set then just use the results
            if imdbID == "" or imdbID.isspace():
                if len(results) == 0:
                    resultIndex = -1
                    resultTitle = "No title found"
                else:
                    resultTitle = results[0]['title']
                    resultID = results[0].movieID
            else:
                found = False
                j = 0

                for result in results:
                    if result.movieID == imdbID:
                        resultIndex = j
                        resultTitle = result['title']
                        resultID = result.movieID
                        found = True
                        break
                    j += 1

                # If the movie's IMDB ID isn't contained in the results, add it to it
                if not found:
                    newResult = ia.get_movie(imdbID)
                    results.append(newResult)
                    resultIndex = len(results) - 1
                    resultTitle = newResult['title']
                    resultID = newResult.movieID

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


    def OnButtonOkClick(self, event):
        """
        Handles a click in the Ok button of the dialog.
        """

        index = 0

        for results in self.__resultCache:
            movie = self.__movieList[index]
            selectedResultIndex = self.lstResults.GetItemData(index)

            if selectedResultIndex == -1:
                continue
            
            selectedResult = results[selectedResultIndex]

            movie.SetIMDBID(selectedResult['id'])

            index += 1
