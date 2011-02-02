#! /usr/bin/env python

"""
File: FilterIMDB.py
Author: Revolt
--------------------------
Desc:
    This file contains the definition of the FilterIMDB class
    which filters movies according to their IMDB id
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

from classes.Filter import *

class FilterIMDB(Filter):
    """ The Filter IMDB class """

    def __init__(self, id = None):
        """
        Initializes a new FilterIMDB instance.
        ---
        Params:
            @ id (UString) - Part of the imdb id to search for.
                             If None, match only empty imdb id
        """

        self.__id = id

    def Test(self, movie):
        """
        Tests the provided movie in regard to its name.
        ---
        Params:
            @ movie (Movie) - The movie to test.
        ---
        Returns: True if the movie contains the specified name, False
                 otherwise.
        """

        imdbID = movie.GetIMDBID()

        if self.__id is None:
            return imdbID is None or imdbID.isspace()
        else:
            return imdbID.find(self.__id) != -1
        
