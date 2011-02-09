#! /usr/bin/env python

"""
File: ImageSelectorDialog.py
Author: Revolt
--------------------------
Desc:
    This file contains the definition and implementation of the dialog
    that allows you to see an image in greater size and to select a
    new one.
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
from gui.controls.ImageViewer import *

class ImageSelectorDialog(wx.Dialog):
    """ The Image Selector Dialog class """

    def __init__(self, parent, image, defImage = wx.NullImage):
        """
        Constructor 
        ---
        Params:
            @ image (wx.Image) - Currently set image.
        """

        # -- Private Variables Initialization --
        self.__image = image
        self.__imagePath = ""
        self.__defImage = defImage

        # -- Panel Initialization --
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "Image Selector", style = wx.RESIZE_BORDER)
        self.SetMaxSize((600, 800))
        
        # -- Control Initialization --
        self.szrBaseVert = wx.BoxSizer(wx.VERTICAL)

        self.lblInstructions = wx.StaticText(self, wx.ID_ANY, "Left-click to " +
                               "select a new image and right-click to use the " +
                               "default")

        self.szrImageHoriz = wx.BoxSizer(wx.HORIZONTAL)

        self.imgView = ImageViewer(self, wx.ID_ANY, image, size=(280, 200))
        self.szrImageHoriz.Add(self.imgView, 1, wx.EXPAND | wx.ALL, 5)

        self.szrDialogButtons = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        self.btnOk = self.FindWindowById(wx.ID_OK)
        self.btnCancel = self.FindWindowById(wx.ID_CANCEL)

        self.szrBaseVert.Add(self.lblInstructions, 0, wx.ALL, 5)
        self.szrBaseVert.Add(self.szrImageHoriz, 1, wx.EXPAND | wx.ALL, 5)
        self.szrBaseVert.Add(self.szrDialogButtons, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(self.szrBaseVert)

        # -- Event Binding
        self.imgView.Bind(wx.EVT_LEFT_UP, self.OnImageLeftClick)
        self.imgView.Bind(wx.EVT_RIGHT_UP, self.OnImageRightClick)

        self.imgView.Refresh()

    # -- PROPERTIES (GET) --
    def GetImage(self):
        """
        Return: (wx.Image) The currently selected image.
        """

        return self.__image

    # -- PROPERTIES (SET) --
    def SetImage(self, image):
        """
        Sets a new image.
        ---
        Params:
            @ image (wx.Image) - The new image to set.
        """

        self.__image = image
        self.RefreshImage()

    # -- METHODS --
    def RefreshImage(self):
        """
        Refreshes the ImageViewer with the internal image object
        """

        if self.__image is not None:
            self.imgView.SetImage(self.__image)
        else:
            self.imgView.SetImage(wx.NullImage)

    # -- EVENTS --
    def OnImageLeftClick(self, event):
        """
        Handle left click on the image viewer.
        """

        imageWildcard = "All image files|*.bmp;*.jpg;*.jpeg;*.png|" + \
                        "BMP files|*.bmp|JPG files|*.jpg;*.jpeg|" + \
                        "PNG files|*.png"

        fileChooser = wx.FileDialog(self, "Choose an image", 
                                    defaultFile = self.__imagePath,
                                    wildcard = imageWildcard, 
                                    style = wx.FD_FILE_MUST_EXIST |
                                            wx.FD_PREVIEW |
                                            wx.FD_OPEN)

        if fileChooser.ShowModal() == wx.ID_OK:
            self.__imagePath = fileChooser.GetPath()
            newImage = wx.Image(self.__imagePath)
            self.SetImage(newImage)
            
    def OnImageRightClick(self, event):
        """
        Handle right click on the image viewer.
        """

        self.SetImage(self.__defImage)
