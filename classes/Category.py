#! /usr/bin/env python

"""
File: Category.pye
Author: Revolt
Date: 28-08-2010
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

class Category:
    """ The Category class """

    def __init__(self, name, catType, relpath, hdd = None):
        """
        Constructor
        ---
        Params:
            @ name (String) - The name of this category
            @ type (String) - The type of this category
            @ relpath (String) - The path to the folder that is the root of the
                        category, in relation to the hdd path
        """

        self._name = name
        self._type = catType
        self._relpath = relpath
        self._hdd = hdd

    # -- Get Properties --
    def GetName(self):
        """
        Return (String): The name of this category
        """

        return self._name

    def GetType(self):
        """
        Return (String): The type of this category
        """
        return self._type

    def GetRelativePath(self):
        """
        Return (String): The path to the folder that is the root
                         of the category, in relation to the hdd
        """
        return self._relpath

    def GetFullPath(self):
        """
        Return (String): The absolute path to the category folder
                         (based on hdd) or the RelativePath if no
                         hdd defined
        """

        if self._hdd == None:
            return self.GetRelativePath()
        else:
            return os.path.join(self._hdd.GetPath(), self.GetRelativePath())

    def GetHdd(self):
        """
        Return (HardDrive): The object representing the harddrive
                            that owns this category or None
        """

        return self._hdd

    # -- Set Properties --
    def SetName(self, name):
        """
        Changes the name of this category
        ---
        Param:
            @ name (String) - The new name of the category
        """

        self._name = name

    def SetType(self, catType):
        """
        Changes the type of this category
        ---
        Param:
            @ type (String) - The new type of the category
        """

        self._type = catType

    def SetRelPath(self, relpath):
        """
        Changes the path of the category relative to the HDD
        ---
        Param:
            @ relpath (String) - The new relpath of the category
        """

        self._relpath = relpath

    def SetHdd(self, hdd):
        """
        Changes the hdd associated with this category
        ---
        Param:
            @ hdd (HardDrive) - The new harddrive that owns this category
        """

        self._hdd = hdd
