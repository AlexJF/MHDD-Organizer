#! /usr/bin/env python

"""
File: Category.py
Author: Revolt
--------------------------
Desc:
    This file contains the definition of the Category class
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

import os
from gui.IMDBSearchDialog import *

class Category:
    """ The Category class """

    def __init__(self, name, relpath, hdd = None):
        """
        Constructor
        ---
        Params:
            @ name (String) - The name of this category
            @ relpath (String) - The path to the folder that is the root of the
                        category, in relation to the hdd path
            @ hdd (HardDrive) - The harddrive that owns this category
        """

        self.__name = name
        self.__relpath = relpath
        self.__hdd = hdd

    # -- Get Properties --
    def GetName(self):
        """
        Return (String): The name of this category
        """

        return self.__name

    def GetRelativePath(self):
        """
        Return (String): The path to the folder that is the root
                         of the category, in relation to the hdd
        """
        return self.__relpath

    def GetFullPath(self):
        """
        Return (String): The absolute path to the category folder
                         (based on hdd) or the RelativePath if no
                         hdd defined
        """

        if self.__hdd == None:
            return self.GetRelativePath()
        else:
            return os.path.join(self.__hdd.GetPath(), self.GetRelativePath())

    def GetHdd(self):
        """
        Return (HardDrive): The object representing the harddrive
                            that owns this category or None
        """

        return self.__hdd

    # -- Set Properties --
    def SetName(self, name):
        """
        Changes the name of this category
        ---
        Param:
            @ name (String) - The new name of the category
        """

        self.__name = name

    def SetRelPath(self, relpath):
        """
        Changes the path of the category relative to the HDD
        ---
        Param:
            @ relpath (String) - The new relpath of the category
        """

        self.__relpath = relpath

    def SetHdd(self, hdd):
        """
        Changes the hdd associated with this category
        ---
        Param:
            @ hdd (HardDrive) - The new harddrive that owns this category
        """

        self.__hdd = hdd

    # -- Methods --
    def GetMovieList(self):
        """
        Retrieves the list of movies managed by this category
        ---
        Returns (List of Movies): The list of movies under this
                                  category.
        ---
        NOTE: This only works if the category is managed by a HDD
        """

        if not self.GetHdd():
            return None

        objList = []
        imdbSearchList = []
        catFullPath = self.GetFullPath()

        items = os.listdir(catFullPath)
        i = 0

        dlgProgress = wx.ProgressDialog("Parsing category entries", "Preparing \
                                        entry list.", len(items), style = wx.PD_APP_MODAL | wx.PD_AUTO_HIDE)

        dlgProgress.Show()

        for item in items:
            i += 1
            itemFullPath = os.path.join(catFullPath, item)
            dlgProgress.Update(i, "Parsing '" + item + "'")
            if os.path.isdir(itemFullPath):
                try:
                    obj = Movie(itemFullPath)

                    if obj:
                        objList.append(obj)
                        if not obj.GetLoadedLocalInfo():
                            imdbSearchList.append(obj)

                except ValueError as e:
                    print str(e)

        if len(imdbSearchList) > 0:
            dlgIMDBSearch = IMDBSearchDialog(None, self.__name, imdbSearchList)

            if dlgIMDBSearch.ShowModal() == wx.ID_OK:
                for movie in imdbSearchList:
                    movie.LoadInfoFromIMDB()

        return objList
