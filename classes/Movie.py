#! /usr/bin/env python

"""
File: Movie.py
Author: Revolt
--------------------------
Desc:
    This file contains the definition of the Movie class
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

import os, urllib
from datetime import date
from imdb import IMDb

class Movie(object):
    """ The Movie class """

    def __init__(self, cat, name, path):
        """
        Constructor
        ---
        Params:
            @ cat (Category) - The category containing this movie.
            @ name (String) - The name of this movie object.
            @ path (String) - The path of this movie object.
        """

        self.__category = cat
        self.__name = name
        self.__path = path
        self.__dirty = True
        self.__modDate = date.today()
        self.__title = u""
        self.__imdbID = u""
        self.__year = u""
        self.__rating = 0
        self.__genres = []
        self.__plot = u""
        self.__directors = []
        self.__actors = []
        self.__image = None

        self.LoadInfoFromHdd()

    # -- Properties (Get) --
    def GetName(self):
        """
        Return: (String) The title of the movie.
        """

        return self.__name

    def GetRelPath(self):
        """
        Return: (UString) The path to the movie directory relative to the
                         category path
        """
        
        return self.__path

    def GetFullPath(self):
        """
        Return: (UString) The full path to the movie directory
        """
        
        return os.path.join(self.__category.GetFullPath(), self.__path)

    def GetModificationDate(self):
        """
        Return: (datetime) The date of last modification.
        """

        return self.__modDate

    def GetTitle(self):
        """
        Return: (UString) The real title of the movie.
        """

        return self.__title

    def GetIMDBID(self):
        """
        Return: (UString) The id of the imdb entry associated with this movie.
        """

        return self.__imdbID

    def GetYear(self):
        """
        Return: (UString) The year of release of the movie.
        """

        return self.__year

    def GetRating(self):
        """
        Return: (int) The rating of the movie (between 1 and 10)
        """

        return self.__rating

    def GetGenres(self):
        """
        Return: (List of UStrings) The genres of the movie.
        """

        return self.__genres

    def GetPlot(self):
        """
        Return: (UString) The plot of the movie.
        """
        
        return self.__plot

    def GetDirectors(self):
        """
        Return: (List of UStrings) The directors of the movie.
        """

        return self.__directors

    def GetActors(self):
        """
        Return: (List) A list of actors in the movie.
        """

        return self.__actors

    def GetImage(self):
        """
        Return: (Bytes) The image representing this movie.
        """

        return self.__image

    # -- Properties (Set) --
    def SetModificationDate(self, date):
        """
        Sets the modification date of the movie.
        ---
        Params:
            @ date (datetime) - The new date of modification of the movie.
        """

        self.__modDate = date

    def SetTitle(self, title):
        """
        Sets the title of the movie.
        ---
        Params:
            @ title (UString) - The title of the movie.
        """

        self.__dirty = True
        self.__title = title

    def SetIMDBID(self, id):
        """
        Sets the IMDB id of the movie.
        ---
        Params:
            @ url (UString) - The IMDB id of the movie.
        """

        self.__dirty = True
        self.__imdbID = id

    def SetYear(self, year):
        """
        Sets the year of release of the movie.
        ---
        Params:
            @ year (UString) - The year of release of the movie.
        """

        self.__dirty = True
        self.__year = year

    def SetRating(self, rating):
        """
        Sets the rating of the movie.
        ---
        Params:
            @ rating (int) - The rating of the movie (between 1 and 10)
        """

        if rating < 1 or rating > 10:
            return

        self.__dirty = True
        self.__rating = rating

    def SetGenres(self, genres):
        """
        Sets the genres of the movie.
        ---
        Params:
            @ genres (List of UStrings) - The genres of the movie.
        """

        self.__dirty = True
        self.__genres = genres

    def SetPlot(self, plot):
        """
        Sets the plot of the movie.
        ---
        Params:
            @ plot (UString) - The plot of the movie.
        """
        
        self.__dirty = True
        self.__plot = plot

    def SetDirectors(self, directors):
        """
        Sets the director of the movie.
        ---
        Params:
            @ director (List of UStrings) - The directors of the movie.
        """

        self.__dirty = True
        self.__directors = directors

    def SetActors(self, actors):
        """
        Sets the actors of the movie.
        ---
        Params:
            @ actors (List of UStrings) - The actors of the movie.
        """

        self.__dirty = True
        self.__actors = actors

    def SetImage(self, image):
        """
        Sets the image of the movie.
        ---
        Params:
            @ image (Bytes) - Bytes containing image data.
        """

        self.__dirty = True
        self.__image = image

    # -- Methods --
    def LoadInfoFromHdd(self):
        """
        Loads movie info from the Hdd.
        ---
        Return: (Boolean) True if info was loaded successfully,
                           False otherwise.
        """

        if not self.__dirty:
            return True

        if self.__category.GetHdd().LoadMovieInfo(self):
            self.__dirty = False
            return True
        else:
            return False

    def SaveInfoToHdd(self):
        """
        Saves movie info to a config file in the dir.
        ---
        Return: (Boolean) True if info was correctly saved or didn't need
                 to be saved, False if there was an error
        """

        if self.__dirty:
            return self.__category.GetHdd().SaveMovieInfo(self)
        else:
            return True

    def LoadInfoFromIMDB(self):
        """
        Loads the movie info from IMDB.
        """

        if (self.__imdbID == ""):
            return

        ia = IMDb()

        imdbMovieObj = ia.get_movie(self.__imdbID)

        self.__title = imdbMovieObj['title']
        self.__year = unicode(imdbMovieObj['year'])
        self.__rating = int(round(float(imdbMovieObj['rating']), 0))
        self.__genres = imdbMovieObj['genres']
        self.__plot = imdbMovieObj['plot'][0]
        
        self.__directors = []
        for director in imdbMovieObj['director']:
            self.__directors.append(director['name'])

        self.__actors = []
        for actor in imdbMovieObj['cast']:
            self.__actors.append(actor['name'])

        img = None

        try:
            img = urllib.urlopen(imdbMovieObj['cover url'])
            imgData = img.read()
            self.__image = imgData
        except IOError, e:
            pass
        finally:
            if img is not None:
                img.close()

        self.__dirty = True

