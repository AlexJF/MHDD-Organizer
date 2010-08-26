#! /usr/bin/env python

"""
File: ObjectDetailsPanel.py
Author: Revolt
Date: 15-08-2010
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

class ObjectDetailsPanel(wx.Panel):
    """ The object details panel class """

    def __init__(self, parent):
        """ Constructor """

        # -- Panel Initialization --
        wx.Panel.__init__(self, parent)

        # -- Control Initialization --
        self.szrBase = wx.BoxSizer()
        self.szrGrid = wx.GridBagSizer()

        self.lblTitle = wx.StaticText(self, label="Object Title")
        self.lblTitle.SetFont(wx.Font(16, 70, 90, 92, False, wx.EmptyString))

        self.pnlImgCover = wx.Panel(self, size=(100, 140), style=wx.SUNKEN_BORDER)
        self.imgCover = wx.StaticBitmap(self.pnlImgCover, wx.ID_ANY, wx.Bitmap("gui/images/video-default.png", wx.BITMAP_TYPE_PNG), size=(100, 140), style=wx.SIMPLE_BORDER)
        
        self.lblRealTitle = wx.StaticText(self, label="Real Title:")
        self.txtRealTitle = wx.TextCtrl(self, size=(250, -1))

        self.lblIMDB = wx.StaticText(self, label="IMDB:")
        self.txtIMDB = wx.TextCtrl(self, size=(250, -1))
        self.lnkIMDB = wx.HyperlinkCtrl(self, wx.ID_ANY, "Go", "http://www.imdb.com")

        self.lblRelDate = wx.StaticText(self, label="Release Date:")
        self.datRelDate = wx.DatePickerCtrl(self)

        self.lblRating = wx.StaticText(self, label="Rating:")
        self.spnRating = wx.SpinCtrl(self, size=(40, -1), min=0, max=10)

        self.szrDateAndRating = wx.BoxSizer(wx.HORIZONTAL)
        self.szrDateAndRating.Add(self.lblRelDate, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.TOP | wx.BOTTOM, 3)
        self.szrDateAndRating.Add(self.datRelDate, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
        self.szrDateAndRating.Add(self.lblRating, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
        self.szrDateAndRating.Add(self.spnRating, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.lblGenre = wx.StaticText(self, label="Genre:")
        self.txtGenre = wx.TextCtrl(self, size=(250, -1))

        self.lblPlot = wx.StaticText(self, label="Plot:")
        self.txtPlot = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        self.lblDirector = wx.StaticText(self, label="Director:")
        self.txtDirector = wx.TextCtrl(self, size=(250, -1))

        self.lblActors = wx.StaticText(self, label="Actors:")
        self.lstActors = wx.ListView(self, style=wx.LC_REPORT | wx.LC_NO_HEADER | wx.LC_SINGLE_SEL | wx.LC_SORT_ASCENDING)

        self.szrGrid.Add(self.lblTitle, (0, 0), (1, 3), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3)
        self.szrGrid.Add(self.pnlImgCover, (0, 3), (5, 1), wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 20)
        self.szrGrid.Add(self.lblRealTitle, (1, 0), (1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3) 
        self.szrGrid.Add(self.txtRealTitle, (1, 1), (1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 3) 
        self.szrGrid.Add(self.lblIMDB, (2, 0), (1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3) 
        self.szrGrid.Add(self.txtIMDB, (2, 1), (1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 3) 
        self.szrGrid.Add(self.lnkIMDB, (2, 2), (1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3) 
        self.szrGrid.Add(self.szrDateAndRating, (3, 0), (1, 3), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3)
        self.szrGrid.Add(self.lblGenre, (4, 0), (1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3) 
        self.szrGrid.Add(self.txtGenre, (4, 1), (1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 3) 
        self.szrGrid.Add(self.lblPlot, (5, 0), (1, 2), wx.LEFT | wx.RIGHT | wx.TOP | wx.ALIGN_CENTER_VERTICAL, 3) 
        self.szrGrid.Add(self.txtPlot, (6, 0), (1, 4), wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 3) 
        self.szrGrid.Add(self.lblDirector, (7, 0), (1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3) 
        self.szrGrid.Add(self.txtDirector, (7, 1), (1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 3) 
        self.szrGrid.Add(self.lblActors, (8, 0), (1, 1), wx.LEFT | wx.RIGHT | wx.TOP | wx.ALIGN_CENTER_VERTICAL, 3) 
        self.szrGrid.Add(self.lstActors, (9, 0), (1, 4), wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 3) 

        self.szrGrid.AddGrowableCol(3)
        self.szrGrid.AddGrowableRow(6)
        self.szrGrid.AddGrowableRow(9)

        self.szrBase.Add(self.szrGrid, 1, wx.ALL | wx.EXPAND, 0)
        self.SetSizer(self.szrBase)
        self.Layout()
