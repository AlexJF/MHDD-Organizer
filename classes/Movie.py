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

import wx, os, ConfigParser
from datetime import date
from imdb import IMDb

class Movie:
    """ The Movie class """

    __loadedLocalInfo = False
    __name = ""
    __realTitle = ""
    __imdbLink = ""
    __year = ""
    __modDate = None
    __rating = ""
    __genres = []
    __plot = ""
    __director = ""
    __actors = []

    def __init__(self, dirPath):
        """
        Constructor
        ---
        dirPath (String) - The path to the directory which this Movie object represents
        """

        if not os.path.isdir(dirPath):
            raise ValueError("Movie path doesn't exist: " + dirPath)

        self.__dirPath = dirPath
        self.__name = os.path.split(self.__dirPath)[1]

        foundMovie = False
        movieExtensions = ["avi", "mpeg", "mpg", "mkv"]

        for f in os.listdir(dirPath):
            extension = os.path.splitext(f)[1][1:].lower()
            print extension
            if extension in movieExtensions:
                foundMovie = True

        if not foundMovie:
            raise ValueError("Path doesn't contain a movie: " + dirPath)

        self.LoadInfoFromConfig()

    # -- Properties (Get) --
    def GetLoadedLocalInfo(self):
        """
        Return (Boolean): If local info was already loaded.
        """

        return self.__loadedLocalInfo

    def GetName(self):
        """
        Return (String): The title of the movie.
        """

        return self.__name

    def GetRealTitle(self):
        """
        Return (String): The real title of the movie.
        """

        return self.__realTitle

    def GetIMDBLink(self):
        """
        Return (String): The link to the imdb page correspondent to this movie.
        """

        return self.__imdbLink

    def GetYear(self):
        """
        Return (String): The year of release of the movie.
        """

        return self.__relDate

    def GetModDate(self):
        """
        Return (Date): The date since the last modification.
        """

        return self.__modDate

    def GetRating(self):
        """
        Return (Float): The rating of the movie.
        """

        return self.__rating

    def GetGenres(self):
        """
        Return (List of Strings): The genres of the movie.
        """

        return self.__genres

    def GetPlot(self):
        """
        Return (String): The plot of the movie.
        """
        
        return self.__plot

    def GetDirectors(self):
        """
        Return (List of Strings): The directors of the movie.
        """

        return self.__director

    def GetActors(self):
        """
        Return (List): A list of actors in the movie.
        """

        return self.__actors

    # -- Properties (Set) --
    def SetName(self, name):
        """
        Sets the name of the movie.
        ---
        name (String) - The name of the movie.
        """

        self.__name = name

    def SetRealTitle(self, title):
        """
        Sets the title of the movie.
        ---
        title (String) - The title of the movie.
        """

        self.__realTitle = title

    def SetIMDBLink(self, url):
        """
        Sets the IMDB url of the movie.
        ---
        url (String) - The IMDB url of the movie.
        """

        self.__imdbLink = url

    def SetYear(self, year):
        """
        Sets the year of release of the movie.
        ---
        year (String) - The year of release of the movie.
        """

        self.__relDate = relDate

    def SetRating(self, rating):
        """
        Sets the rating of the movie.
        ---
        rating (Float) - The rating of the movie.
        """

        self.__rating = rating

    def SetGenres(self, genre):
        """
        Sets the genres of the movie.
        ---
        genre (List of Strings) - The genres of the movie.
        """

        self.__genre = genre

    def SetPlot(self, plot):
        """
        Sets the plot of the movie.
        ---
        plot (String) - The plot of the movie.
        """
        
        self.__plot = plot

    def SetDirectors(self, directors):
        """
        Sets the director of the movie.
        ---
        director (List of Strings) - The directors of the movie.
        """

        self.__director = director

    def SetActors(self, actors):
        """
        Sets the actors of the movie.
        ---
        actors (List of Strings) - The actors of the movie.
        """

        return self.__actors

    # -- Methods --
    def LoadInfoFromConfig(self):
        """
        Loads movie info from a config file in the dir.
        """
        config = wx.Config.Get()
        #infoFolderPath = os.path.join(self.__dirPath, config.Read("/MovieInfoFolderName"))
        infoFolderPath = os.path.join(self.__dirPath, ".mhddorganizer")
        infoFilePath = os.path.join(infoFolderPath, "info.ini")

        if not os.path.exists(infoFilePath):
            return False

        movieInfoParser = ConfigParser.ConfigParser()
        movieInfoParser.read(infoFilePath)

        infoEntries = movieInfoParser.items("info")

        for entry in infoEntries:
            name, value = entry

            if name == "moddate":
                self.__modDate = date.fromtimestamp(value)
            elif name == "title":
                self.__realTitle = value
            elif name == "imdb":
                self.__imdbLink = value
            elif name == "year":
                self.__year = value
            elif name == "rating":
                value = float(value)
                self.__rating = value if (value >= 0 and value <= 10) else 0
            elif name == "genre":
                self.__genre = value
            elif name == "plot":
                self.__plot = value
            elif name == "director":
                self.__director = value
            elif name == "actors":
                self.__actors = value.split("||")

        self.__loadedLocalInfo = True

        return True

    def LoadInfoFromIMDB(self):
        """
        Loads the movie info from IMDB.
        """

        if (self.__imdbLink == ""):
            return

        ia = IMDb()

        imdbMovieObj = ia.get_movie(self.__imdbLink)

        self.__realTitle = imdbMovieObj['title']
        self.__year = imdbMovieObj['year']
        self.__rating = float(imdbMovieObj['rating'])
        self.__genres = imdbMovieObj['genres']
        self.__plot = imdbMovieObj['plot'][0]
        self.__directors = imdbMovieObj['director']
        for actor in imdbMovieObj['cast']:
            self.__actors.append(actor['name'])

        return self.SaveInfoToConfig()

    def SaveInfoToConfig(self):
        """
        Saves movie info to a config file in the dir.
        """
        config = wx.Config.Get()
        infoFolderPath = os.path.join(self.__dirPath, config.Read("/MovieInfoFolderName"))
        infoFilePath = os.path.join(dataFolderPath, "info.ini")

        if not os.path.isdir(infoFolderPath):
            try:
                os.mkdir(infoFolderPath)
            except OSError, e:
                print "Error creating movie data folder."
                print e.message
                return False

        configFile = None

        try:
            configFile = open(infoFilePath, "w")
        except Exception, e:
            print "Error opening config"
            print e.message
            return False

        movieInfoParser = ConfigParser.ConfigParser()
        infoSection = "info"

        if not movieInfoParser.has_section(infoSection):
            movieInfoParser.add_section(infoSection)

        movieInfoParser.set(infoSection, "modddate", time.mktime(self.__modDate.timetuple()))
        movieInfoParser.set(infoSection, "title", self.__realTitle)
        movieInfoParser.set(infoSection, "imdb", self.__imdbLink)
        movieInfoParser.set(infoSection, "year", self.__year)
        movieInfoParser.set(infoSection, "rating", self.__rating)
        movieInfoParser.set(infoSection, "genre", self.__genre)
        movieInfoParser.set(infoSection, "plot", self.__plot)
        movieInfoParser.set(infoSection, "director", self.__director)
        movieInfoParser.set(infoSection, "actors", string.join(self.__actors, "||"))

        movieInfoParser.write(configFile)

        configFile.close()

        return True


