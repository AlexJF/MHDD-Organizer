#! /usr/bin/env python

"""
File: HardDrive.py
Author: Revolt
--------------------------
Desc:
    This file contains the definition and implementation of the 
    HardDrive class
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

import wx, os, uuid, ConfigParser
from Category import *

class HardDrive:
    """ The Category class """

    def __init__(self, hdduuid = None, label = None, path = None, catList = []):
        """ 
        Constructor
        ---
        Params:
            @ uuid - The UUID associated with this HDD. If none is provided
                     a new one is automatically generated.
            @ label - The label associated with this HDD
            @ path - The path associated with this HDD
        """

        if not hdduuid:
            hdduuid = str(uuid.uuid4())

        self._uuid = hdduuid 
        self._label = label
        self._path = path
        self._categoryListDirty = True
        self._categoryList = catList

    # -- Get Properties --
    def GetUuid(self):
        """
        Return: UUID (as string) of the HDD
        """

        return self._uuid

    def GetLabel(self):
        """
        Return: Label of the HDD
        """
        
        return self._label

    def GetPath(self):
        """
        Return: Path of the HDD
        """

        return self._path

    def GetCategoryList(self):
        """
        Return: Category list associated with this HDD
        """

        return self._categoryList

    # -- Set Properties --
    def SetLabel(self, label):
        """
        Sets a new label for this HDD
        ---
        Params:
            @ label - The new label for this HDD
        """

        self._label = label

    def SetPath(self, path):
        """
        Sets a new path for this HDD
        ---
        Params:
            @ path - The new path for this HDD
        """

        self._path = path

    # -- Methods --
    def Connected(self):
        """
        Checks if this HDD is connected by checking if its path exists
        ---
        Return: True if connected/False otherwise
        """

        return os.path.isdir(self._path)

    def LoadCategoryList(self, force = False):
        """ 
        Loads the category list from the HDD 
        ---
        Params:
            @ force - (Bool) If categories should be loaded even if 
                      list isn't dirty
        Return: True on success/False on failure
        """

        if not self._categoryListDirty and not force:
            return True

        self._categoryList = []
        self._categoryListDirty = False

        hddConfigFolderPath = os.path.join(self._path, ".mhddorganizer")
        hddCategoryConfigPath = os.path.join(hddConfigFolderPath, "categories.ini")

        if not os.path.exists(hddCategoryConfigPath):
            return False

        hddCategoryConfig = ConfigParser.ConfigParser()
        hddCategoryConfig.read(hddCategoryConfigPath)

        for category in hddCategoryConfig.sections():
            cat = Category(category, hddCategoryConfig.get(category, "Type"), hddCategoryConfig.get(category, "Path"), self)
            self._categoryList.append(cat)

        return True

    def SetCategoryList(self, categoryList):
        """
        Sets the category list of this HDD to the supplied list of categories
        ---
        Params:
            @ categoryList - A list of Category objects
        ---
        Note: The list is only altered in memory. To save the changes to the
              HDD call SaveCategoryList()
        """

        self._categoryListDirty = True
        self._categoryList = categoryList

        for category in self._categoryList:
            category.SetHdd(self)

    def SaveCategoryList(self):
        """
        Saves the actual virtual category list of this HDD to the actual HDD
        ---
        Return: True on success/False on failure
        """

        if not self._categoryListDirty:
            return True

        if not os.path.isdir(self._path):
            return False

        hddConfigFolderPath = os.path.join(self._path, ".mhddorganizer")
        hddCategoryConfigPath = os.path.join(hddConfigFolderPath, "categories.ini")

        if not os.path.isdir(hddConfigFolderPath):
            os.mkdir(hddConfigFolderPath)

        configFile = None

        try:
            configFile = open(hddCategoryConfigPath, "w")
        except Exception, e:
            print "Error opening config"
            print e.message
            return False

        hddCategoryConfig = ConfigParser.ConfigParser()

        for category in self._categoryList:
            if not hddCategoryConfig.has_section(category.GetName()):
                hddCategoryConfig.add_section(category.GetName())

            hddCategoryConfig.set(category.GetName(), "Type", category.GetType())
            hddCategoryConfig.set(category.GetName(), "Path", category.GetRelativePath())

        hddCategoryConfig.write(configFile)

        configFile.close()

        self._categoryListDirty = False

        return True
