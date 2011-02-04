#! /usr/bin/env python

"""
File: ImageViewer.py
Author: Revolt
--------------------------
Desc:
    This file contains the definition and implementation of an image
    viewer control.
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

class ImageViewer(wx.Control):
    """ The ImageViewer class """

    def __init__(self, parent, id = -1, image = wx.NullImage, pos = wx.DefaultPosition,
                 size = wx.DefaultSize, style = 0, label = ""):
        """ 
        Constructor of an ImageViewer control.
        ---
        Params:
            @ parent (wx.Window) - The parent window of this control.
            @ image (wx.Image) - An image to be shown in the control.
            @ label (String) - A label for the image to be shown.
        """

        wx.Control.__init__(self, parent, id, pos, size, style)

        self.__startX = self.__startY = 0
        self.__image = image
        self.__cachedBitmap = wx.NullBitmap

        self.SetLabel(label)
        self.SetMinSize(size)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnResize)

        self.CreateBitmap()

    # -- PROPERTIES (SET) --
    def GetImage(self):
        """
        Return: (wx.Image) - The image shown in the control.
        """

        return self.__image

    # -- PROPERTIES (SET) --
    def SetImage(self, image):
        """
        Sets a new image to show in the control.
        ---
        Params:
            @ image (wx.Image) - The image to show in the control.
        """

        self.__image = image
        self.CreateBitmap()
        self.Refresh()

    # -- METHODS --
    def CreateBitmap(self):
        """
        This method (re)creates the cached bitmap to reflect size
        changes and also (re) calculates the startX and startY
        attributes so that the image is centered on the control.
        """

        self.__cachedBitmap = wx.NullBitmap
        self.__startX = self.__startY = 0

        image = self.__image.Copy()
        (imageW, imageH) = image.GetSize()

        if imageW == 0 or imageH == 0:
            return

        (controlW, controlH) = self.GetSize()

        if imageW > controlW or imageH > controlH:
            ratio = float(imageW) / imageH

            if imageW > imageH:
                imageW = controlW
                imageH = imageW / ratio
            else:
                imageH = controlH
                imageW = imageH * ratio

            image = image.Rescale(imageW, imageH)

        self.__startX = (controlW - imageW) / 2
        self.__startY = (controlH - imageH) / 2
        self.__cachedBitmap = image.ConvertToBitmap()

    def Render(self, dc):
        """
        The method responsible for actually drawing the control.
        ---
        Params:
            @ dc (wx.DC) - The device context to which to draw.
        """

        bgColour = self.GetDefaultAttributes().colBg
        brush = wx.Brush(bgColour)
        dc.SetBrush(brush)
        dc.SetPen(wx.TRANSPARENT_PEN)

        (w, h) = dc.GetSizeTuple()
        dc.DrawRectangle(0, 0, w, h)
        dc.DrawBitmap(self.__cachedBitmap, self.__startX, self.__startY, True)

    # -- EVENTS --
    def OnPaint(self, event):
        """
        The method called when a paint event occurs.
        """

        paintDC = wx.PaintDC(self)
        self.Render(paintDC)

    def OnResize(self, event):
        """
        The method called when the control is resized.
        """

        self.CreateBitmap()
        self.Refresh()

