#! /usr/bin/env python

"""
File: FilterName.py
Author: Revolt
--------------------------
Desc:
    This file contains the definition of the NameFilter class
    which filters movies according to their name.
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

class FilterName(Filter):
    """ The Filter class """

    def __init__(self, name):
        """
        Initializes a new NameFilter instance.
        ---
        Params:
            @ name (String) - The name to use in the test operation.
        """

        self.__name = name

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

        return movie.GetName().find(self.__name) != -1
        
