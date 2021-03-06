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
from Movie import *

class Category(object):
    """ The Category class """

    def __init__(self, name, relpath, hdd):
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
        self.__movieList = []
        self.__loaded = False

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

    def SetRelativePath(self, relpath):
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
            @ hdd (HardDrive) - The new harddrive that owns this category.
        """

        self.__hdd = hdd

    # -- Methods --
    def GetMovieList(self, refresh = False):
        """
        Retrieves the list of movies managed by this category.
        ---
        Params:
            @ refresh (Boolean) - Whether or not to force a refresh of the list.
        ---
        Return (List of Movies): The list of movies under this category.
        """

        if self.__loaded and not refresh:
            return self.__movieList

        self.__hdd.LoadCategoryMovieList(self)

        return self.__movieList

    def SetMovieList(self, movieList):
        """
        Sets the list of movies managed by this category.
        ---
        Params:
            @ movieList (List of Movies) - Movies managed by this category.
        """

        if movieList is None:
            self.__movieList = []
        else:
            self.__movieList = movieList
        self.__loaded = True
