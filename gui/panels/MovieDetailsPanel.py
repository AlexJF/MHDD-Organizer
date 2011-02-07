#! /usr/bin/env python

"""
File: MovieDetailsPanel.py
Author: Revolt
--------------------------
Desc:
    This file contains the definition and implementation of the panel 
    containing details about a multimedia object
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


import wx, os, io
from gui.controls.ImageViewer import *
from gui.dialogs.ImageSelectorDialog import *

class MovieDetailsPanel(wx.Panel):
    """ The object details panel class """

    def __init__(self, parent):
        """ Constructor """

        # -- Private Variables --
        self.__defImage = wx.Image("gui/images/video-default.png", wx.BITMAP_TYPE_PNG)
        self.__currentMovie = None

        # -- Panel Initialization --
        wx.Panel.__init__(self, parent)

        # -- Control Initialization --
        self.szrBase = wx.BoxSizer()
        self.szrGrid = wx.GridBagSizer()

        self.lblName = wx.StaticText(self, label="Movie Name")
        self.lblName.SetFont(wx.Font(16, 70, 90, 92, False, wx.EmptyString))

        self.imgCover = ImageViewer(self, wx.ID_ANY, self.__defImage)
        self.imgCover.SetMinSize((100, 140))
        
        self.lblTitle = wx.StaticText(self, label="Title:")
        self.txtTitle = wx.TextCtrl(self, size=(250, -1))

        self.lblTMDB = wx.StaticText(self, label="TMDB ID:")
        self.txtTMDB = wx.TextCtrl(self, size=(250, -1))
        self.lnkTMDB = wx.HyperlinkCtrl(self, wx.ID_ANY, "Go", "http://www.imdb.com")

        self.lblRelYear = wx.StaticText(self, label="Release Year:")
        self.txtRelYear = wx.TextCtrl(self, size=(40, -1))

        self.lblRating = wx.StaticText(self, label="Rating:")
        self.spnRating = wx.SpinCtrl(self, size=(40, -1), min=0, max=10)

        self.szrDateAndRating = wx.BoxSizer(wx.HORIZONTAL)
        self.szrDateAndRating.Add(self.lblRelYear, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.TOP | wx.BOTTOM, 3)
        self.szrDateAndRating.Add(self.txtRelYear, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
        self.szrDateAndRating.Add(self.lblRating, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
        self.szrDateAndRating.Add(self.spnRating, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.lblGenres = wx.StaticText(self, label="Genres:")
        self.txtGenres = wx.TextCtrl(self, size=(250, -1))

        self.lblDirectors = wx.StaticText(self, label="Director:")
        self.txtDirectors = wx.TextCtrl(self)

        self.lblOverview = wx.StaticText(self, label="Overview:")
        self.txtOverview = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        self.lblActors = wx.StaticText(self, label="Actors:")
        self.txtActors = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        self.szrButtons = wx.BoxSizer(wx.HORIZONTAL)
        self.btnSave = wx.Button(self, wx.ID_ANY, label="Save")
        self.szrButtons.Add(self.btnSave, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.szrGrid.Add(self.lblName, (0, 0), (1, 3), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3)
        self.szrGrid.Add(self.imgCover, (0, 3), (6, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 20)
        self.szrGrid.Add(self.lblTitle, (1, 0), (1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3) 
        self.szrGrid.Add(self.txtTitle, (1, 1), (1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 3) 
        self.szrGrid.Add(self.lblTMDB, (2, 0), (1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3) 
        self.szrGrid.Add(self.txtTMDB, (2, 1), (1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 3) 
        self.szrGrid.Add(self.lnkTMDB, (2, 2), (1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3) 
        self.szrGrid.Add(self.szrDateAndRating, (3, 0), (1, 3), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3)
        self.szrGrid.Add(self.lblGenres, (4, 0), (1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3) 
        self.szrGrid.Add(self.txtGenres, (4, 1), (1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 3) 
        self.szrGrid.Add(self.lblDirectors, (5, 0), (1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3) 
        self.szrGrid.Add(self.txtDirectors, (5, 1), (1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 3) 
        self.szrGrid.Add(self.lblOverview, (6, 0), (1, 2), wx.LEFT | wx.RIGHT | wx.TOP | wx.ALIGN_CENTER_VERTICAL, 3) 
        self.szrGrid.Add(self.txtOverview, (7, 0), (1, 4), wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 3) 
        self.szrGrid.Add(self.lblActors, (8, 0), (1, 1), wx.LEFT | wx.RIGHT | wx.TOP | wx.ALIGN_CENTER_VERTICAL, 3) 
        self.szrGrid.Add(self.txtActors, (9, 0), (1, 4), wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 3) 
        self.szrGrid.Add(self.szrButtons, (10, 0), (1, 4), wx.ALL | wx.ALIGN_CENTER, 3)

        self.szrGrid.AddGrowableCol(1)
        self.szrGrid.AddGrowableRow(7)
        self.szrGrid.AddGrowableRow(9)

        self.szrBase.Add(self.szrGrid, 1, wx.ALL | wx.EXPAND, 0)
        self.SetSizer(self.szrBase)
        self.Layout()

        # -- Event Binding --
        self.btnSave.Bind(wx.EVT_BUTTON, self.OnSave)
        self.imgCover.Bind(wx.EVT_LEFT_UP, self.OnImageClick)
        self.lnkTMDB.Bind(wx.EVT_HYPERLINK, self.OnLinkClick)

    # -- METHODS --
    def SetMovie(self, movie):
        """
        Given a movie, loads its info into the respective fields on the panel.
        """

        self.__currentMovie = movie
        self.lblName.SetLabel(movie.GetName())
        self.txtTitle.SetValue(movie.GetTitle())
        self.txtTMDB.SetValue(movie.GetTMDBID())
        self.txtRelYear.SetValue(movie.GetYear())
        self.spnRating.SetValue(movie.GetRating())
        separator = u", "
        self.txtGenres.SetValue(separator.join(movie.GetGenres()))
        self.txtOverview.SetValue(movie.GetOverview())
        self.txtDirectors.SetValue(separator.join(movie.GetDirectors()))
        self.txtActors.SetValue(separator.join(movie.GetActors()))

        imageData = movie.GetImageData()

        if imageData is not None:
            imageStream = io.BytesIO(bytearray(imageData))
            image = wx.ImageFromStream(imageStream)
            self.imgCover.SetImage(image)
        else:
            self.imgCover.SetImage(self.__defImage)

    def UpdateMovie(self):
        """
        Updates the movie object with the information provided in the panel
        fields and writes that data back to disk.
        """

        self.__currentMovie.SetTitle(self.txtTitle.GetValue())
        self.__currentMovie.SetTMDBID(self.txtTMDB.GetValue())
        self.__currentMovie.SetYear(self.txtRelYear.GetValue())
        self.__currentMovie.SetRating(self.spnRating.GetValue())
        self.__currentMovie.SetGenres(self.txtGenres.GetValue().split(", "))
        self.__currentMovie.SetOverview(self.txtOverview.GetValue())
        self.__currentMovie.SetDirectors(self.txtDirectors.GetValue().split(", "))
        self.__currentMovie.SetActors(self.txtActors.GetValue().split(", "))
        image = self.imgCover.GetImage()
        imageStream = io.BytesIO()
        if image is not None and image != self.__defImage:
            if image.SaveStream(imageStream, wx.BITMAP_TYPE_JPEG):
                self.__currentMovie.SetImageData(imageStream.getvalue())
        self.__currentMovie.SaveInfoToHdd()


    # -- EVENTS --
    def OnSave(self, event):
        """
        Event handler for save button click.
        """

        self.UpdateMovie()

    def OnImageClick(self, event):
        """
        Handles a click on the image.
        """

        if self.__currentMovie is None:
            return

        dlgImageSelect = ImageSelectorDialog(self, self.imgCover.GetImage())

        if dlgImageSelect.ShowModal() == wx.ID_OK:
            selectedImage = dlgImageSelect.GetImage()
            self.imgCover.SetImage(selectedImage)

    def OnLinkClick(self, event):
        """
        Handles a click on the 'Go' link.
        """

        tmdbID = self.txtTMDB.GetValue()
        
        if not tmdbID.isspace():
            tmdbURL = "http://www.tmdb.org/movie/" + tmdbID
            wx.LaunchDefaultBrowser(tmdbURL)
