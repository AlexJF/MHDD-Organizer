#! /usr/bin/env python

"""
File: FileProvider.py
Author: Revolt
--------------------------
Desc:
    This file contains the definition and implementation of the 
    provider that gets info from the physical files and directories
    on the HDD.
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

import os, ConfigParser, logging, time, codecs
from datetime import datetime
from classes.Provider import *
from classes.Category import *
from classes.Movie import *

class FileProvider(Provider):
    """ The FileProvider class """

    def __init__(self, hdd):
        """
        Initializes a new FileProvider instance.
        ---
        Params:
            @ hdd (HardDrive) - The harddrive associated with this provider instance.
        """

        super(FileProvider, self).__init__(hdd)
        self.__logger = logging.getLogger("main")


    # -- Methods --
    def LoadCategoryList(self):
        """
        Reads the category list of the HDD and returns it.
        ---
        Return: (List of Categories) The categories pertaining to the
                 hdd associated with this provider.
        """

        harddrive = self.GetHdd()
        hddConfigFolderPath = os.path.join(harddrive.GetPath(), ".mhddorganizer")
        hddCategoryConfigPath = os.path.join(hddConfigFolderPath, "categories.ini")

        if not os.path.exists(hddCategoryConfigPath):
            self.__logger.debug("Didn't find categories in the HDD (%s)", self.GetHdd().GetUuid())
            return None

        categoryList = []

        hddCategoryConfig = ConfigParser.ConfigParser()
        hddCategoryConfig.read(hddCategoryConfigPath)

        for category in hddCategoryConfig.sections():
            cat = Category(category, hddCategoryConfig.get(category, "Path"), harddrive)
            categoryList.append(cat)

        self.__logger.debug("Loaded %d categories from the HDD (%s)", len(categoryList), self.GetHdd().GetUuid())

        return categoryList


    def SaveCategoryList(self):
        """
        Saves category list of the associated hdd.
        ---
        Return: (Boolean) True on success, false otherwise
        """

        harddrive = self.GetHdd()
        harddrivePath = harddrive.GetPath()

        hddConfigFolderPath = os.path.join(harddrivePath, ".mhddorganizer")
        hddCategoryConfigPath = os.path.join(hddConfigFolderPath, "categories.ini")

        if not os.path.isdir(hddConfigFolderPath):
            self.__logger.debug("Created config folder in HDD (%s)", self.GetHdd().GetUuid())
            os.mkdir(hddConfigFolderPath)

        configFile = None

        try:
            configFile = open(hddCategoryConfigPath, "w")
        except Exception, e:
            self.__logger.exception("Error while opening categories.ini in HDD (%s)", self.GetHdd().GetUuid())
            return False

        hddCategoryConfig = ConfigParser.ConfigParser()

        for category in self.__categoryList:
            if not hddCategoryConfig.has_section(category.GetName()):
                hddCategoryConfig.add_section(category.GetName())

            hddCategoryConfig.set(category.GetName(), "Path", category.GetRelativePath())

        hddCategoryConfig.write(configFile)

        configFile.close()

        self.__logger.debug("Successfully wrote %d categories to the HDD (%s)", len(self.__categoryList),
                            self.GetHdd().GetUuid())

        return True

    def LoadCategoryMovieList(self, cat):
        """
        Loads all movies contained in the provided category and returns a list
        with them.
        ---
        Params:
            @ cat (Category) - The category whose movies we want.
        ---
        Return: (List of Movies) The movies contained in the category.
        """

        self.__logger.debug("Loading movie list from category '%s'", cat.GetName())

        if cat.GetHdd() != self.GetHdd():
            self.__logger.error("Category doesn't belong to the HDD associated with this provider")
            return None

        movieList = []
        movieExtensions = ["avi", "mpeg", "mpg", "mkv"]

        catFullPath = cat.GetFullPath()
        items = os.listdir(catFullPath)

        for item in items:
            itemFullPath = os.path.join(catFullPath, item)
            if os.path.isdir(itemFullPath):
                movie = None
                self.__logger.debug("Reading directory: %s", itemFullPath)

                for f in os.listdir(itemFullPath):
                    name, extension = os.path.splitext(f)
                    extension = extension[1:].lower()
                    if extension in movieExtensions:
                        self.__logger.debug("Found a movie in the directory: %s", f)
                        movie = Movie(cat, item, item)
                        break

                if movie is not None:
                    movieList.append(movie)

        self.__logger.debug("Loaded %d movies from category '%s'", len(movieList), cat.GetName())

        return movieList

    def LoadMovieInfo(self, movie):
        """
        Loads all info of the provided movie into its object.
        ---
        Params:
            @ movie (Movie) - The movie whose info we wish to load.
        ---
        Return: (Boolean) True if successful, False otherwise.
        """

        self.__logger.debug("Loading movie '%s' info", movie.GetName()) 

        moviePath = movie.GetFullPath()

        infoFolderPath = os.path.join(moviePath, ".mhddorganizer")
        infoFilePath = os.path.join(infoFolderPath, "info.ini")

        if not os.path.exists(infoFilePath):
            self.__logger.debug("Movie doesn't have info in the HDD")
            return False

        try:
            movieInfoParser = ConfigParser.ConfigParser()
            movieInfoParser.read(infoFilePath)

            infoEntries = movieInfoParser.items("info")
            separator = "||"

            for entry in infoEntries:
                name, value = entry

                if name == "moddate":
                    movie.SetModificationDate(datetime.fromtimestamp(float(value)))
                elif name == "title":
                    movie.SetTitle(value)
                elif name == "imdb":
                    movie.SetIMDBID(value)
                elif name == "year":
                    movie.SetYear(value)
                elif name == "rating":
                    value = int(value)
                    movie.SetRating(value)
                elif name == "genres":
                    movie.SetGenres(value.split(separator))
                elif name == "plot":
                    movie.SetPlot(value)
                elif name == "directors":
                    movie.SetDirectors(value.split(separator))
                elif name == "actors":
                    movie.SetActors(value.split(separator))
        except Exception, e:
            self.__logger.exception("Error reading info file")
            return False

        return True

    def SaveMovieInfo(self, movie):
        """
        Saves a single movie to the HDD.
        ---
        Params:
            @ movie (Movie) - The movie to save.
        """

        self.__logger.debug("Saving movie '%s' info", movie.GetName()) 

        moviePath = movie.GetFullPath()

        infoFolderPath = os.path.join(moviePath, ".mhddorganizer")
        infoFilePath = os.path.join(infoFolderPath, "info.ini")

        if not os.path.isdir(infoFolderPath):
            try:
                os.mkdir(infoFolderPath)
            except OSError, e:
                self.__logger.exception("Error creating movie data folder")
                return False

        configFile = None

        try:
            configFile = codecs.open(infoFilePath, encoding='utf-8', mode="w")
        except Exception, e:
            self.__logger.exception("Error opening info file for writing")
            return False

        movieInfoParser = ConfigParser.ConfigParser()
        infoSection = "info"

        if not movieInfoParser.has_section(infoSection):
            movieInfoParser.add_section(infoSection)

        separator = "||"

        movie.SetModificationDate(datetime.now())
        movieInfoParser.set(infoSection, "moddate", time.mktime(movie.GetModificationDate().timetuple()))
        movieInfoParser.set(infoSection, "title", movie.GetTitle())
        movieInfoParser.set(infoSection, "imdb", movie.GetIMDBID())
        movieInfoParser.set(infoSection, "year", movie.GetYear())
        movieInfoParser.set(infoSection, "rating", movie.GetRating())
        movieInfoParser.set(infoSection, "genres", separator.join(movie.GetGenres()))
        movieInfoParser.set(infoSection, "plot", movie.GetPlot())
        movieInfoParser.set(infoSection, "directors", separator.join(movie.GetDirectors()))
        movieInfoParser.set(infoSection, "actors", separator.join(movie.GetActors()))

        movieInfoParser.write(configFile)

        configFile.close()

        return True
