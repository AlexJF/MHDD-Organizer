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

import os, uuid, ConfigParser, logging
from Category import *
from hddproviders.DBFileSyncProvider import *
from hddproviders.DatabaseProvider import *

class HardDrive(object):
    """ The HardDrive class """

    def __init__(self, hdduuid = None, label = "", path = ""):
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

        self.__logger = logging.getLogger("main")
        self.__uuid = hdduuid 
        self.__label = label
        self.__path = ""
        self.__loaded = False
        self.__categoryList = []
        self.__provider = None

        self.SetPath(path)

        self.__logger.debug("Initialized new Harddrive: %s - %s - %s - %s", hdduuid, label, path, self.__provider)

    def __del__():
        """
        Destructor
        """

        del self.__provider

    # -- Get Properties --
    def GetUuid(self):
        """
        Return: UUID (as string) of the HDD
        """

        return self.__uuid

    def GetLabel(self):
        """
        Return: Label of the HDD
        """
        
        return self.__label

    def GetPath(self):
        """
        Return: Path of the HDD
        """

        return self.__path

    def GetCategoryList(self):
        """
        Return: Category list associated with this HDD
        """

        if not self.__loaded:
            self.LoadCategoryList()
            self.__loaded = True

        return self.__categoryList

    # -- Set Properties --
    def SetLabel(self, label):
        """
        Sets a new label for this HDD
        ---
        Params:
            @ label - The new label for this HDD
        """

        self.__label = label

    def SetPath(self, path):
        """
        Sets a new path for this HDD
        ---
        Params:
            @ path - The new path for this HDD
        """

        self.__path = path

        if path == "":
            if self.__provider is not None:
                self.SetProvider(None)
        elif self.Connected():
            if not isinstance(self.__provider, DBFileSyncProvider):
                self.SetProvider(DBFileSyncProvider(self))
        else:
            if not isinstance(self.__provider, DatabaseProvider):
                self.SetProvider(DatabaseProvider(self))

    def SetProvider(self, provider):
        """
        Sets a new HDD provider
        ---
            @ provider - The new provider for this HDD
        """
        
        self.__logger.debug("Setting new provider '%s' on HDD '%s'", type(provider), self.__uuid)
        self.__provider = provider

    def SetCategoryList(self, catList):
        """
        Sets a new category list
        ---
        Params:
            @ catList (List of Categories) - The new category list
        """

        if catList is None:
            self.__categoryList = []
            return

        self.__loaded = True
        self.__categoryList = catList

    # -- Methods --
    def Connected(self):
        """
        Checks if this HDD is connected by checking if its path exists
        ---
        Return: (Boolean) True if connected, False otherwise
        """

        return os.path.isdir(self.__path)

    def LoadCategoryList(self):
        """ 
        Loads the category list from the HDD 
        ---
        Return: (Boolean) True on success, False on failure
        """

        if self.__provider is None:
            return False

        return self.__provider.LoadCategoryList()

    def SaveCategoryList(self):
        """
        Saves the actual virtual category list of this HDD to the actual HDD
        ---
        Return: (Boolean) True on success, False on failure
        """

        if self.__provider is None:
            return False

        return self.__provider.SaveCategoryList()

    def LoadCategoryMovieList(self, cat):
        """
        Loads all movies from the provided category and returns a list containing them.
        ---
        Params:
            @ cat (Category) - The category whose movies we wish to get.
        ---
        Return: (List of Movies) The movies contained in the category.
        """

        if self.__provider is None:
            return False

        return self.__provider.LoadCategoryMovieList(cat)

    def LoadMovieInfo(self, movie):
        """
        Loads movie info into the specified movie object.
        ---
        Return: (Boolean) True on success, False on failure.
        """

        if self.__provider is None:
            return False

        return self.__provider.LoadMovieInfo(movie)

    def SaveMovieInfo(self, movie):
        """
        Saves movie info of the specified movie.
        ---
        Return: (Boolean) True on success, False on failure.
        """

        if self.__provider is None:
            return False

        return self.__provider.SaveMovieInfo(movie)
