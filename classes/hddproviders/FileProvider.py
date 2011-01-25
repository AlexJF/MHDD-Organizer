#! /usr/bin/env python

"""
File: FileProvider.py
Author: Revolt
--------------------------
Desc:
    This file contains the definition and implementation of the 
    FileProvider class. This class is responsible for retrieving
    HDD info from a directory structure representing a movie
    tree.
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

import os, ConfigParser
from classes.Provider import *

class FileProvider(Provider):
    """ The FileProvider class """

    def __init__(self, hdd):
        """
        Initializes a new FileProvider instance.
        ---
        Params:
            @ hdd (HardDrive) - The harddrive associated with this provider instance.
        """

        super(Provider, self).__init__(hdd)
