#! /usr/bin/env python

"""
File: DatabaseProvider.py
Author: Revolt
--------------------------
Desc:
    This file contains the definition and implementation of the 
    provider that gets info from a database that caches all movie
    info of a specific HDD.
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

import os, logging, time, sqlite3, wx
from datetime import datetime
from classes.Provider import *
from classes.Category import *
from classes.Movie import *

class DatabaseProvider(Provider):
    """ The DatabaseProvider class """

    def __init__(self, hdd):
        """
        Initializes a new DatabaseProvider instance.
        ---
        Params:
            @ hdd (HardDrive) - The harddrive associated with this provider instance.
        """

        super(FileProvider, self).__init__(hdd)
        self.__logger = logging.getLogger("main")
        
        appDataFolder = wx.StandardPaths.GetUserDataDir()
        dbFolder = os.path.join(appDataFolder, "databases")

        if not os.path.isdir(dbFolder):
            try:
                os.mkdir(dbFolder)
            except OSError, e:
                self.__logger.exception("Error creating database directory")
                raise e

        dbPath = os.path.join(dbFolder, hdd.GetUuid())

        self.__dbConn = sqlite3.connect(dbPath)

        self.InitializeDatabase()

    def __del__(self):
        """
        Handles the destruction of a DatabaseProvider instance.
        """

        self.__logger.debug("Destroying DatabaseProvider...")
        self.__dbConn.close()

    # -- Methods --
    def InitializeDatabase(self):
        """
        Initializes a new database creating all necessary tables.
        """

        dbCursor = self.__dbConn.cursor()

        sql = "CREATE TABLE IF NOT EXISTS categories " + 
              "(id INT PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, 
                path TEXT UNIQUE);"

        dbCursor.execute(sql)

        sql = "CREATE TABLE IF NOT EXISTS movies " +
              "(id INT PRIMARY KEY AUTOINCREMENT, cat INT, name TEXT, path TEXT UNIQUE" +
              "image BLOB, title TEXT, imdb TEXT, year TEXT, rating INT, " +
              "genres TEXT, plot TEXT, directors TEXT, actors TEXT, moddate INT);"

        dbCursor.execute(sql)

        self.__dbConn.commit()

    def LoadCategoryList(self):
        """
        Reads the category list of the HDD from the DB and sets it.
        ---
        Return: (Boolean) True if successful, false otherwise.
        """

        categoryList = []

        dbCursor = self.__dbConn.cursor()

        dbCursor.execute("SELECT * FROM categories")

        for row in dbCursor:
            cat = Category(row[1], row[2], self.GetHdd())
            categoryList.append(cat)

        self.__logger.debug("Read %d categories from the DB (%s)", 
                            len(categoryList), self.GetHdd.GetUuid())

        self.GetHdd().SetCategoryList(categoryList)

        return True


    def SaveCategoryList(self):
        """
        Saves category list of the associated hdd into the DB.
        ---
        Return: (Boolean) True on success, false otherwise
        """

        dbCursor = self.__dbConn.cursor()

        dbCatList = self.LoadCategoryList()

        catList = self.GetHdd().GetCategoryList()

        updateList = []
        deleteList = []

        i = 0
        for dbCat in dbCatList:
            j = 0
            for cat in catList:
                # Category is present in both places so UPDATE
                if dbCat.GetPath() == cat.GetPath():
                    updateList.append(cat)
                    catList.pop(j)
                    break
                j += 1
            else:
                # Category is only present in  the DB so DELETE

        # What was left in catList are the categories
        # not present in the DB so INSERT
        insertList = catList

        for cat in updateList:
            dbCursor.execute("UPDATE categories SET name = ? WHERE path = ?",
                             cat.GetName(),
                             cat.GetPath())

        for cat in deleteList:
            dbCursor.execute("SELECT id FROM categories WHERE path = ?", cat.GetPath())
            result = dbCursor.fetchone()
            catid = result['id']
            dbCursor.execute("DELETE FROM categories, movies WHERE id = ?", catid)
            dbCursor.execute("DELETE FROM movies WHERE cat = ?", catid)

        for cat in insertList:
            dbCursor.execute("INSERT INTO categories (id, name, path)
                              VALUES (, ?, ?)", cat.GetName(), cat.GetPath())

        self.__dbConn.commit()

        self.__logger.debug("Successfully wrote %d categories to the DB (%s)", 
                            len(updateList) + len(insertList),
                            self.GetHdd().GetUuid())

        return True

    def LoadCategoryMovieList(self, cat):
        """
        Loads all movies contained in the provided category and sets them to
        the provided category.
        ---
        Params:
            @ cat (Category) - The category whose movies we want to load.
        ---
        Return: (Boolean) True if successful, False otherwise
        """

        self.__logger.debug("Loading movie list from category '%s'", cat.GetName())

        if cat.GetHdd() != self.GetHdd():
            self.__logger.error("Category doesn't belong to the HDD associated with this provider")
            return False

        movieList = []
        separator = u"||"

        dbCursor = self.__dbConn.cursor()

        dbCursor.execute("SELECT name, path FROM movies INNER JOIN categories " + 
                         "ON categories.id = movies.cat WHERE categories.path = ?"
                         cat.GetPath())

        for movieData in dbCursor:
            movie = Movie(cat, movieData['name'], movieData['path'])
            self.LoadMovieInfo(movie)
            movieList.append(movie)

        self.__logger.debug("Loaded %d movies from category '%s'", len(movieList), cat.GetName())

        cat.SetMovieList(movieList)

        return True

    def GetMovieInfoDict(self, movie):
        """
        Gets the info of the provided movie and returns it in a dict.
        ---
        Params:
            @ movie (Movie) - The movie whose info we wish to load.
        ---
        Return: (Dict) A dict containing movie info.
        """

        self.__logger.debug("Getting movie '%s' info", movie.GetName()) 

        dbCursor = self.__dbConn.cursor()

        dbCursor.execute("SELECT * FROM movies WHERE movies.path = ?", movie.GetRelPath())

        movieData = dbCursor.fetchone()

        return movieData

    def SaveMovieInfo(self, movie):
        """
        Saves a single movie to the HDD.
        ---
        Params:
            @ movie (Movie) - The movie to save.
        """

        self.__logger.debug("Saving movie '%s' info", movie.GetName()) 

        dbCursor = self.__dbConn.cursor()

        dbCursor.execute("SELECT id FROM categories WHERE path = ?",
                         movie.GetCategory().GetRelativePath())

        result = dbCursor.fetchone()
        catid = result['id']

        dbCursor.execute("SELECT id FROM movies WHERE cat = ? " +
                         " AND path = ?", catid, movie.GetRelativePath())

        result = dbCursor.fetchone()

        separator = u"||"

        movie.SetModificationDate(datetime.now())

        movieDict = {'cat':catid, 'path':movie.GetRelativePath()}

        for key, value in movieDict.iteritems():
            if isinstance(value, list):
                value = separator.join(value)
            elif isinstance(value, datetime):
                value = time.mktime(value.timetuple())

        infoDict = movie.GetInfoDict()
        parameterDict = dict(infoDict)
        parameterDict.update(movieDict)

        if len(result) == 0:
            # If the movie we are saving isn't present in the DB, INSERT
            dbCursor.execute("INSERT INTO movies (id, cat, name, path, image, title, " +
                             "imdb, year, rating, genres, plot, directors, actors, " +
                             "modddate) VALUES (, :cat, :name, :path, :image, :title, " +
                             ":imdb, :year, :rating, :genres, :plot, :directors, " +
                             ":actors, :moddate)", parameterDict)
        else:
            # Else, if the movie is present in the DB, UPDATE
            dbCursor.execute("UPDATE movies SET image = :image, title = :title, " +
                             "imdb = :imdb, year = :year, rating = :rating, " + 
                             "genres = :genres, plot = :plot, directors = :directors, " +
                             "actors = :actors, moddate = :moddate WHERE cat = :cat " + 
                             "AND path = :path",
                             parameterDict)

        return True

    def DeleteMovieInfo(self, movie):
        """
        Deletes the provided movie from the database.
        Note: Only the DatabaseProvider should have this method since
        its structure is defined by the physical file structure on disk.
        Therefore on sync, the app might detect that one movie that was
        previously on the HDD is no more and, therefore, should be removed
        from the DB cache.
        ---
        Params:
            @ movie (Movie) - The movie whose info we wish to remove.
        """

        self.__logger.debug("Deleting movie '%s' from database",
                            movie.GetName())

        cat = movie.GetCategory()

        dbCursor = self.__dbConn.cursor()

        dbCursor.execute("SELECT id FROM categories WHERE path = ?", 
                         cat.GetRelativePath())
        result = dbCursor.fetchone()
        catid = result['id']

        dbCursor.execute("DELETE FROM movies WHERE path = ? AND cat = ?", 
                         movie.GetRelativePath(), catid)

        return True

