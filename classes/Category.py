#! /usr/bin/env python

"""
File: Category.py
Author: Revolt
Date: 28-08-2010
--------------------------
Desc:
    This file contains the definition of the Category class
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

class Category:
    """ The Category class """

    name = None
    type = None
    path = None

    def __init__(self, name, type, path):
        self.name = name
        self.type = type
        self.path = path
