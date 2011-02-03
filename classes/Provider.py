#! /usr/bin/env python

"""
File: Provider.py
Author: Revolt
--------------------------
Desc:
    This file contains the definition and implementation of the 
    generic provider class.
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

class Provider(object):
    """ The Provider class """

    def __init__(self, hdd):
        """
        Initializes a new Provider instance.
        ---
        Params:
            @ hdd (HardDrive) - The harddrive associated with this provider instance.
        """

        self.__hdd = hdd

    # -- Get Properties --
    def GetHdd(self):
        """
        Return: (HardDrive) The Hdd instance associated with this provider
        """

        return self.__hdd

    # -- Methods --
    def LoadCategoryList(self):
        """
        Reads the category list of the HDD and returns it.
        ---
        Return: (List of Categories) The categories pertaining to the
                 hdd associated with this provider.
        """

        raise NotImplementedError()

    def SaveCategoryList(self, catList = None):
        """
        Saves category list of the associated hdd.
        ---
        Params:
            @ catList (List of Categories) - A list of categories to save.
              Should catList be None, the provider gets the list from the HDD.
        ---
        Return: (Boolean) True on success, False otherwise
        """

        raise NotImplementedError()

    def LoadCategoryMovieList(self, cat):
        """
        Loads all movies contained in the provided category.
        ---
        Params:
             @ cat (Category) - The category whose movies we wish to load.
        ---
        Return: (List of Movies) List of movies contained in the category.
        """
        
        raise NotImplementedError()

    def GetMovieInfoDict(self, movie):
        """
        Gets the info of the provided movie and returns it in a dict.
        ---
        Params:
            @ movie (Movie) - The movie whose info we wish to load.
        ---
        Return: (Dict) A dict containing movie info.
        """

        raise NotImplementedError()

    def LoadMovieInfo(self, movie):
        """
        Loads info from a single movie and sets it to the movie object.
        ---
        Params:
            @ movie (Movie) - The movie whose info we wish to load.
        ---
        Return: (Boolean) True on success, False otherwise
        """

        return movie.SetInfoFromDict(self.GetMovieInfoDict(movie))


    def SaveMovieInfo(self, movie):
        """
        Saves a info from a single movie.
        ---
        Params:
            @ movie (Movie) - The movie to save.
        ---
        Return: (Boolean) True on success, False otherwise
        """

        raise NotImplementedError()
