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

class Provider(Provider):
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
    def GetHDD(self):
        """
        Returns the HDD instance associated with this provider
        """

        return self.__hdd
