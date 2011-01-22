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


import wx, os

class MovieDetailsPanel(wx.Panel):
    """ The object details panel class """

    def __init__(self, parent):
        """ Constructor """

        # -- Panel Initialization --
        wx.Panel.__init__(self, parent)

        # -- Control Initialization --
        self.szrBase = wx.BoxSizer()
        self.szrGrid = wx.GridBagSizer()

        self.lblName = wx.StaticText(self, label="Movie Name")
        self.lblName.SetFont(wx.Font(16, 70, 90, 92, False, wx.EmptyString))

        self.pnlImgCover = wx.Panel(self, size=(100, 140), style=wx.SUNKEN_BORDER)
        self.imgCover = wx.StaticBitmap(self.pnlImgCover, wx.ID_ANY, wx.Bitmap("gui/images/video-default.png", wx.BITMAP_TYPE_PNG), size=(100, 140), style=wx.SIMPLE_BORDER)
        
        self.lblTitle = wx.StaticText(self, label="Title:")
        self.txtTitle = wx.TextCtrl(self, size=(250, -1))

        self.lblIMDB = wx.StaticText(self, label="IMDB ID:")
        self.txtIMDB = wx.TextCtrl(self, size=(250, -1))
        self.lnkIMDB = wx.HyperlinkCtrl(self, wx.ID_ANY, "Go", "http://www.imdb.com")

        self.lblRelYear = wx.StaticText(self, label="Release Year:")
        self.txtRelYear = wx.TextCtrl(self, size=(40, -1))

        self.lblRating = wx.StaticText(self, label="Rating:")
        self.spnRating = wx.SpinCtrl(self, size=(40, -1), min=0, max=10)

        self.szrDateAndRating = wx.BoxSizer(wx.HORIZONTAL)
        self.szrDateAndRating.Add(self.lblRelYear, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.TOP | wx.BOTTOM, 3)
        self.szrDateAndRating.Add(self.txtRelYear, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
        self.szrDateAndRating.Add(self.lblRating, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
        self.szrDateAndRating.Add(self.spnRating, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.lblGenres = wx.StaticText(self, label="Genre:")
        self.txtGenres = wx.TextCtrl(self, size=(250, -1))

        self.lblPlot = wx.StaticText(self, label="Plot:")
        self.txtPlot = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        self.lblDirectors = wx.StaticText(self, label="Director:")
        self.txtDirectors = wx.TextCtrl(self)

        self.lblActors = wx.StaticText(self, label="Actors:")
        self.txtActors = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        self.szrButtons = wx.BoxSizer(wx.HORIZONTAL)
        self.btnSave = wx.Button(self, wx.ID_ANY, label="Save")
        self.szrButtons.Add(self.btnSave, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.szrGrid.Add(self.lblName, (0, 0), (1, 3), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3)
        self.szrGrid.Add(self.pnlImgCover, (0, 3), (5, 1), wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 20)
        self.szrGrid.Add(self.lblTitle, (1, 0), (1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3) 
        self.szrGrid.Add(self.txtTitle, (1, 1), (1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 3) 
        self.szrGrid.Add(self.lblIMDB, (2, 0), (1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3) 
        self.szrGrid.Add(self.txtIMDB, (2, 1), (1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 3) 
        self.szrGrid.Add(self.lnkIMDB, (2, 2), (1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3) 
        self.szrGrid.Add(self.szrDateAndRating, (3, 0), (1, 3), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3)
        self.szrGrid.Add(self.lblGenres, (4, 0), (1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3) 
        self.szrGrid.Add(self.txtGenres, (4, 1), (1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 3) 
        self.szrGrid.Add(self.lblPlot, (5, 0), (1, 2), wx.LEFT | wx.RIGHT | wx.TOP | wx.ALIGN_CENTER_VERTICAL, 3) 
        self.szrGrid.Add(self.txtPlot, (6, 0), (1, 4), wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 3) 
        self.szrGrid.Add(self.lblDirectors, (7, 0), (1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3) 
        self.szrGrid.Add(self.txtDirectors, (8, 0), (1, 4), wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 3) 
        self.szrGrid.Add(self.lblActors, (9, 0), (1, 1), wx.LEFT | wx.RIGHT | wx.TOP | wx.ALIGN_CENTER_VERTICAL, 3) 
        self.szrGrid.Add(self.txtActors, (10, 0), (1, 4), wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 3) 
        self.szrGrid.Add(self.szrButtons, (11, 0), (1, 4), wx.ALL | wx.ALIGN_CENTER, 3)

        self.szrGrid.AddGrowableCol(1)
        self.szrGrid.AddGrowableRow(6)
        self.szrGrid.AddGrowableRow(10)

        self.szrBase.Add(self.szrGrid, 1, wx.ALL | wx.EXPAND, 0)
        self.SetSizer(self.szrBase)
        self.Layout()

        self.btnSave.Bind(wx.EVT_BUTTON, self.OnSave)

    # -- METHODS --
    def SetMovie(self, movie):
        """
        Given a movie, loads its info into the respective fields on the panel.
        """

        self.__movie = movie
        self.lblName.SetLabel(movie.GetName())
        self.txtTitle.SetValue(movie.GetTitle())
        self.txtIMDB.SetValue(movie.GetIMDBID())
        self.txtRelYear.SetValue(movie.GetYear())
        self.spnRating.SetValue(movie.GetRating())
        separator = ", "
        self.txtGenres.SetValue(separator.join(movie.GetGenres()))
        self.txtPlot.SetValue(movie.GetPlot())
        self.txtDirectors.SetValue(separator.join(movie.GetDirectors()))
        self.txtActors.SetValue(separator.join(movie.GetActors()))

    def UpdateMovie(self):
        """
        Updates the movie object with the information provided in the panel
        fields and writes that data back to disk.
        """

        self.__movie.SetTitle(self.txtTitle.GetValue())
        self.__movie.SetIMDBID(self.txtIMDB.GetValue())
        self.__movie.SetYear(self.txtRelYear.GetValue())
        self.__movie.SetRating(self.spnRating.GetValue())
        self.__movie.SetGenres(self.txtGenres.GetValue().split(", "))
        self.__movie.SetPlot(self.txtPlot.GetValue())
        self.__movie.SetDirectors(self.txtDirectors.GetValue().split(", "))
        self.__movie.SetActors(self.txtActors.GetValue().split(", "))

        self.__movie.SaveInfoToConfig()


    # -- EVENTS --
    def OnSave(self, event):
        """
        Event handler for save button click
        """

        self.UpdateMovie()
