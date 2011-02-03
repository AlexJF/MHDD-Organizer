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

import os, ConfigParser, logging, time, codecs, sys
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
        Reads the category list of the HDD and sets it.
        ---
        Return: (Boolean) True if load was successful, False otherwise
        """

        harddrive = self.GetHdd()
        hddConfigFolderPath = os.path.join(harddrive.GetPath(), ".mhddorganizer")
        hddCategoryConfigPath = os.path.join(hddConfigFolderPath, "categories.ini")

        if not os.path.exists(hddCategoryConfigPath):
            self.__logger.debug("Didn't find categories in the HDD (%s)", self.GetHdd().GetUuid())
            return False

        categoryList = []
        hddCategoryConfigFile = None

        try:
            hddCategoryConfig = ConfigParser.ConfigParser()
            hddCategoryConfigFile = codecs.open(hddCategoryConfigPath, "r", "utf-8")
            hddCategoryConfig.readfp(hddCategoryConfigFile)

            for category in hddCategoryConfig.sections():
                cat = Category(category, hddCategoryConfig.get(category, "Path"), harddrive)
                categoryList.append(cat)

            self.__logger.debug("Loaded %d categories from the HDD (%s)", len(categoryList), self.GetHdd().GetUuid())
        except IOError, e:
            self.__logger.exception("Error reading HDD category config file")
            return False
        finally:
            if hddCategoryConfigFile is not None:
                hddCategoryConfigFile.close()

        harddrive.SetCategoryList(categoryList)

        return True


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
            self.__logger.debug("Creating config folder in HDD (%s)", 
                                self.GetHdd().GetUuid())
            try:
                os.mkdir(hddConfigFolderPath)
            except OSError, e:
                self.__logger.exception("Error while creating config folder")
                return False

        configFile = None

        try:
            configFile = codecs.open(hddCategoryConfigPath, "w", "utf-8")
        except IOError, e:
            self.__logger.exception("Error while opening categories.ini in HDD (%s)", 
                                    self.GetHdd().GetUuid())
            return False

        hddCategoryConfig = ConfigParser.ConfigParser()

        catList = self.GetHdd().GetCategoryList()

        for category in catList:
            if not hddCategoryConfig.has_section(category.GetName()):
                hddCategoryConfig.add_section(category.GetName())

            hddCategoryConfig.set(category.GetName(), "Path", category.GetRelativePath())

        hddCategoryConfig.write(configFile)

        configFile.close()

        self.__logger.debug("Successfully wrote %d categories to the HDD (%s)", 
                            len(catList), self.GetHdd().GetUuid())

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

        for root, dirs, files in os.walk(catFullPath):
            self.__logger.debug("Reading directory: %s", root)

            for f in files:
                name, extension = os.path.splitext(f)
                extension = extension[1:].lower()
                if extension in movieExtensions:
                    self.__logger.debug("Found a movie in the directory: %s", f)
                    movieDirRelPath = os.path.relpath(root, catFullPath)
                    movieName = movieDirRelPath.replace("/", " ")
                    movieName = movieName.replace("\\", " ")
                    movie = Movie(cat, movieName, movieDirRelPath)
                    self.LoadMovieInfo(movie)
                    movieList.append(movie)
                    break

        self.__logger.debug("Loaded %d movies from category '%s'", len(movieList), cat.GetName())

        return movieList

    def GetMovieInfoDict(self, movie):
        """
        Gets the info of the provided movie and returns it in a dict.
        ---
        Params:
            @ movie (Movie) - The movie whose info we wish to load.
        ---
        Return: (Dict) A dict containing movie info.
        """

        self.__logger.debug("Loading movie '%s' info", movie.GetName()) 

        moviePath = movie.GetFullPath()

        infoFolderPath = os.path.join(moviePath, ".mhddorganizer")
        infoFilePath = os.path.join(infoFolderPath, "info.ini")

        if not os.path.exists(infoFilePath):
            self.__logger.debug("Movie doesn't have info in the HDD")
            return dict()

        infoFile = None
        infoDict = dict()

        try:
            infoFile = codecs.open(infoFilePath, "r", "utf-8")
            movieInfoParser = ConfigParser.ConfigParser()
            movieInfoParser.readfp(infoFile)

            infoEntries = movieInfoParser.items("info")
            separator = u"||"

            for entry in infoEntries:
                name, value = entry
                infoDict[name] = value

        except IOError, e:
            self.__logger.exception("Error reading info file")
            return None
        except ConfigParser.NoSectionError, e:
            self.__logger.exception("Didn't find info section in info file")
            return None
        finally:
            if infoFile is not None:
                infoFile.close()

        imageFilePath = os.path.join(infoFolderPath, "cover.jpg")

        if os.path.exists(imageFilePath):
            imageFile = None

            try:
                imageFile = open(imageFilePath, "rb")
                imageData = imageFile.read()
                infoDict['image'] = imageData
            except IOError, e:
                self.__logger.exception("Error reading cover image")

        return infoDict

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

        infoFile = None

        try:
            infoFile = open(infoFilePath, "w")
        except IOError, e:
            self.__logger.exception("Error opening info file for writing")
            return False

        movieInfoParser = ConfigParser.ConfigParser()
        infoSection = "info"

        if not movieInfoParser.has_section(infoSection):
            movieInfoParser.add_section(infoSection)

        separator = u"||"

        movie.SetModificationDate(datetime.now())

        infoDict = movie.GetInfoDict()
        imageData = infoDict['image']
        del infoDict['image']

        for key, value in infoDict.iteritems():
            if isinstance(value, unicode):
                value = value.encode("utf-8")
            elif isinstance(value, list):
                value = separator.join(value).encode("utf-8")
            elif isinstance(value, datetime):
                value = time.mktime(value.timetuple())

            movieInfoParser.set(infoSection, key, value)

        movieInfoParser.write(infoFile)

        infoFile.close()

        imageData = movie.GetImageData()

        if imageData is not None:
            imageFilePath = os.path.join(infoFolderPath, "cover.jpg")
            imageFile = None

            try:
                imageFile = open(imageFilePath, "wb")
                imageFile.write(imageData)
            except IOError, e:
                self.__logger.exception("Error writing cover image")
                return False
            finally:
                if imageFile is not None:
                    imageFile.close()

        return True
