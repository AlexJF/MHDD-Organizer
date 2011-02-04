"""
File: common.py
Author: Revolt
--------------------------
Desc:
    This file contains the definition and implementation of common
    operations to some dialogs.
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


def GetResultTitle(result):
    """
    Return: (UString) A string containing the result title and year.
    """

    title = result['name']
    year = result['released'][0:4]

    if not year == "" and not year.isspace():
        title += " (" + year + ")"

    return title

def GetResultID(result):
    """
    Return: (UString) A string containing the id of the result.
    """

    return result['id']
