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

import wx, os, uuid
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

        self.uuid = hdduuid 
        self.label = label
        self.path = path
        self.categoryListDirty = True
        self.categoryList = catList

    # -- Get Properties --
    def GetUuid(self):
        """
        Return: UUID (as string) of the HDD
        """

        return self.uuid

    def GetLabel(self):
        """
        Return: Label of the HDD
        """
        
        return self.label

    def GetPath(self):
        """
        Return: Path of the HDD
        """

        return self.path

    def GetCategoryList(self):
        """
        Return: Category list associated with this HDD
        """

        return self.categoryList

    # -- Set Properties --
    def SetLabel(self, label):
        """
        Sets a new label for this HDD
        ---
        Params:
            @ label - The new label for this HDD
        """

        self.label = label

    def SetPath(self, path):
        """
        Sets a new path for this HDD
        ---
        Params:
            @ path - The new path for this HDD
        """

        self.path = path

    # -- Methods --
    def Connected(self):
        """
        Checks if this HDD is connected by checking if its path exists
        ---
        Return: True if connected/False otherwise
        """

        return os.path.isdir(self.path)

    def LoadCategoryList(self, force = False):
        """ 
        Loads the category list from the HDD 
        ---
        Params:
            @ force - (Bool) If categories should be loaded even if 
                      list isn't dirty
        Return: True on success/False on failure
        """

        if not self.categoryListDirty and not force:
            return True

        self.categoryList = []
        self.categoryListDirty = False

        hddConfigFolderPath = os.path.join(self.path, ".mhddorganizer")
        hddCategoryConfigPath = os.path.join(hddConfigFolderPath, "categories.ini")

        if not os.path.exists(hddCategoryConfigPath):
            return False

        hddCategoryConfig = ConfigParser.ConfigParser()
        hddCategoryConfig.read(hddCategoryConfigPath)

        for category in hddCategoryConfig.sections:
            cat = Category(category, hddCategoryConfig.get(category, "Type"), hddCategoryConfig.get(category, "Path"))
            categoryList.append(cat)

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

        self.categoryListDirty = True
        self.categoryList = categoryList

    def SaveCategoryList(self):
        """
        Saves the actual virtual category list of this HDD to the actual HDD
        ---
        Return: True on success/False on failure
        """

        if not self.categoryListDirty:
            return True

        if not os.path.isdir(path):
            return False

        hddConfigFolderPath = os.path.join(self.path, ".mhddorganizer")
        hddCategoryConfigPath = os.path.join(hddConfigFolderPath, "categories.ini")

        if not os.path.isdir(hddConfigFolderPath):
            os.mkdir(hddConfigFolderPath)

        hddCategoryConfig = ConfigParser.ConfigParser()

        for category in self.categoryList:
            if not hddCategoryConfig.has_section(category.Name):
                hddCategoryConfig.add_section(category.name)

            hddCategoryConfig.set(category.name, "Type", category.type)
            hddCategoryConfig.set(category.name, "Path", category.path)

        hddCategoryConfig.write(hddCategoryConfigPath)

        return True
