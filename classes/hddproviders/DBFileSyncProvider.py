"""
File: DBFileSyncProvider.py
Author: Revolt
--------------------------
Desc:
    This file contains the definition and implementation of the 
    provider that gets info from both a database and a hdd folder 
    directory, merging changes where necessary.
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

import os, logging, time, sqlite3, wx
from datetime import datetime
from classes.Provider import *
from classes.hddproviders.FileProvider import *
from classes.hddproviders.DatabaseProvider import *
from classes.Category import *
from classes.Movie import *

class DBFileSyncProvider(Provider):
    """ The DBFileSyncProvider class """

    def __init__(self, hdd):
        """
        Initializes a new DBFileSyncProvider instance.
        ---
        Params:
            @ hdd (HardDrive) - The harddrive associated with this provider instance.
        """

        super(FileProvider, self).__init__(hdd)
        self.__logger = logging.getLogger("main")
        self.__dbProvider = DatabaseProvider(hdd)
        self.__fileProvider = FileProvider(hdd)
        
    # -- Methods --
    def LoadCategoryList(self):
        """
        Reads the category list of the HDD from the directory tree
        and returns it.
        Note: The category list on the database is ignored since the structure
              is entirely defined by the HDD and not by the cache.
        ---
        Return: (List of Categories) The categories pertaining to the
                 hdd associated with this provider.
        """

        self.__fileProvider.LoadCategoryList()
        self.__dbProvider.SaveCategoryList()

        return categoryList


    def SaveCategoryList(self):
        """
        Saves category list of the associated hdd into the DB.
        ---
        Return: (Boolean) True on success, false otherwise
        """

        self.__fileProvider.SaveCategoryList()
        self.__dbProvider.SaveCategoryList()

        return True

    def LoadCategoryMovieList(self, cat):
        """
        Loads all movies contained in the provided category and returns a list
        with them.
        ---
        Params:
            @ cat (Category) - The category whose movies we want.
        ---
        Return: (List of Movies) The movies contained in the category.
        """

        hddMovieList = self.__fileProvider.LoadCategoryMovieList(cat)
        dbMovieList = self.__dbProvider.LoadCategoryMovieList(cat)
        movieList = []

        for hddMovie in hddMovieList:
            j = 0
            found = False

            for dbMovie in dbMovieList:
                if hddMovie.GetRelativePath() == dbMovie.GetRelativePath():
                    # If we found the same movie in both lists...
                    found = True

                    if dbMovie.GetModificationDate() > hddMovie.GetModificationDate():
                        # If the info in the DB is more recent than the info on the HDD...
                        movieList.append(dbMovie)
                        # Update the info in the HDD right now
                        self.__fileProvider.SaveMovieInfo(dbMovie)
                    else:
                        # Else the HDD info is more recent than the info in the DB
                        movieList.append(hddMovie)
                        # Update the info in the DB right now
                        self.__dbProvider.SaveMovieInfo(hddMovie)

                    dbMovieList.pop(j)
                    break

                j += 1

            if not found:
                # If we haven't found a matching movie in the dbList then this is a new
                # movie so add it to the movieList and update the DB
                movieList.append(hddMovie)
                self.__dbProvider.SaveMovieInfo(hddMovie)

        for movie in dbMovieList:
            # Since we delete matches in dbMovieList as we find them, the movies
            # left in dbMovieList are those that are no longer present in the HDD
            self.__dbProvider.DeleteMovieInfo(movie)

        return movieList

    def GetMovieInfoDict(self, movie):
        """
        Loads all info of the provided movie and returns it as a dict
        to the caller.
        ---
        Params:
            @ movie (Movie) - The movie whose info we wish to load.
        ---
        Return: (Dict) A dict object containing movie info.
        """

        hddInfo = self.__fileProvider.GetMovieInfoDict(movie)
        dbInfo = self.__dbProvider.GetMovieInfoDict(movie)

        if hddInfo is not None and dbInfo is not None:
            if hddInfo['moddate'] >= dbInfo['moddate']:
                return hddInfo
            else:
                return dbInfo
        elif hddInfo is not None:
            return hddInfo
        else
            return dbInfo

    def SaveMovieInfo(self, movie):
        """
        Saves a single movie to the HDD.
        ---
        Params:
            @ movie (Movie) - The movie to save.
        """

        self.__fileProvider.SaveMovieInfo(movie)
        self.__dbProvider.SaveMovieInfo(movie)

        return True
