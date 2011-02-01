#! /usr/bin/env python

"""
File: Filter.py
Author: Revolt
--------------------------
Desc:
    This file contains the definition of the Filter interface
    which encapsulates a predicate to use in list filtering.
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

class Filter(object):
    """ The Filter class """

    def Test(self, obj):
        """
        Tests the provided object according to a certain condition.
        ---
        Params:
            @ obj - The object to test.
        ---
        Return: (Boolean) True if the object passed the test, False otherwise.
        """

        raise NotImplementedError()

    def FilterList(self, list, positive = True):
        """
        Filters the provided list returning the result.
        Note: Original list isn't modified.
        ---
        Params:
            @ list (List) - The list to filter.
            @ positive (Boolean) - If condition is positive or negative.
        ---
        Return: (List) Filtered list.
        """

        resultList = []

        if list is not None:
            for item in list:
                if self.Test(item) == positive:
                    resultList.append(item)

        return resultList
