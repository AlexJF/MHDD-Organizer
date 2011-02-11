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

        Provider.__init__(self, hdd)
        self.__logger = logging.getLogger("mhdd.provider.db")
        
        stdPaths = wx.StandardPaths.Get()
        appDataFolder = stdPaths.GetUserLocalDataDir()
        dbFolder = os.path.join(appDataFolder, "databases")

        if not os.path.isdir(dbFolder):
            try:
                os.mkdir(dbFolder)
            except OSError, e:
                self.__logger.exception("Error creating database directory")
                raise e

        dbPath = os.path.join(dbFolder, hdd.GetUuid())

        self.__dbConn = sqlite3.connect(dbPath)
        self.__dbConn.row_factory = sqlite3.Row

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

        self.__logger.debug("Initializing database tables")

        dbCursor = self.__dbConn.cursor()

        sql = "CREATE TABLE IF NOT EXISTS categories " + \
              "(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, " + \
              "path TEXT UNIQUE);"

        dbCursor.execute(sql)

        sql = "CREATE TABLE IF NOT EXISTS movies " + \
              "(id INTEGER PRIMARY KEY AUTOINCREMENT, cat INT, name TEXT, path TEXT," + \
              "image BLOB, title TEXT, tmdb TEXT, year TEXT, rating INT, " + \
              "genres TEXT, overview TEXT, directors TEXT, actors TEXT, moddate INT);"

        dbCursor.execute(sql)

        self.__dbConn.commit()

        dbCursor.close()

    def GetCategoryList(self):
        """
        Gets the category list of the HDD and returns it.
        ---
        Return: (List of Categories) The categories in the HDD.
        """

        categoryList = []

        dbCursor = self.__dbConn.cursor()

        dbCursor.execute("SELECT * FROM categories")

        for row in dbCursor:
            cat = Category(row[1], row[2], self.GetHdd())
            categoryList.append(cat)

        self.__logger.debug("Read %d categories from the DB (%s)", 
                            len(categoryList), self.GetHdd().GetLabel())

        dbCursor.close()

        return categoryList

    def SaveCategoryList(self):
        """
        Saves category list of the associated hdd into the DB.
        ---
        Return: (Boolean) True on success, false otherwise
        """

        dbCursor = self.__dbConn.cursor()

        dbCatList = self.GetCategoryList()

        catList = list(self.GetHdd().GetCategoryList())

        updateList = []
        deleteList = []

        i = 0
        for dbCat in dbCatList:
            j = 0
            for cat in catList:
                # Category is present in both places so UPDATE
                if dbCat.GetRelativePath() == cat.GetRelativePath():
                    updateList.append(cat)
                    catList.pop(j)
                    break
                j += 1
            else:
                # Category is only present in  the DB so DELETE
                deleteList.append(dbCat)

        # What was left in catList are the categories
        # not present in the DB so INSERT
        insertList = catList

        for cat in updateList:
            dbCursor.execute("UPDATE categories SET name = ? WHERE path = ?",
                             [cat.GetName(), cat.GetRelativePath()])

        for cat in deleteList:
            dbCursor.execute("SELECT id FROM categories WHERE path = ?", [cat.GetRelativePath()])
            result = dbCursor.fetchone()
            catid = result['id']
            dbCursor.execute("DELETE FROM categories WHERE id = ?", [catid])
            dbCursor.execute("DELETE FROM movies WHERE cat = ?", [catid])

        for cat in insertList:
            dbCursor.execute("INSERT INTO categories (name, path) " + \
                             "VALUES (?, ?)", [cat.GetName(), cat.GetRelativePath()])

        self.__dbConn.commit()

        self.__logger.debug("Successfully wrote %d categories to the DB (%s)", 
                            len(updateList) + len(insertList),
                            self.GetHdd().GetLabel())

        return True

    def GetCategoryMovieList(self, cat):
        """
        Loads all movies contained in the provided category and returns them
        in a list.
        ---
        Params:
            @ cat (Category) - The category whose movies we want to load.
        ---
        Return: (List of Movies) - Movies contained in the category.
        """

        self.__logger.debug("Loading movie list from category '%s'", cat.GetName())

        if cat.GetHdd() != self.GetHdd():
            self.__logger.error("Category doesn't belong to the HDD associated with this provider")
            return None

        movieList = []

        dbCursor = self.__dbConn.cursor()

        dbCursor.execute("SELECT movies.name, movies.path FROM movies INNER JOIN categories " + \
                         "ON categories.id = movies.cat WHERE categories.path = ?",
                         [cat.GetRelativePath()])

        for movieData in dbCursor:
            movie = Movie(cat, movieData['name'], movieData['path'])
            self.LoadMovieInfo(movie)
            movieList.append(movie)

        self.__logger.debug("Loaded %d movies from category '%s'", len(movieList), cat.GetName())

        dbCursor.close()

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

        self.__logger.debug("Getting movie '%s' info", movie.GetName()) 

        dbCursor = self.__dbConn.cursor()

        dbCursor.execute("SELECT * FROM movies WHERE movies.path = ?", [movie.GetRelativePath()])

        movieDict = dict()
        row = dbCursor.fetchone()
        
        for key in row.keys():
            movieDict[key] = row[key]

        dbCursor.close()

        return movieDict

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
                         [movie.GetCategory().GetRelativePath()])

        result = dbCursor.fetchone()
        catid = result['id']
        
        dbCursor.execute("SELECT id FROM movies WHERE cat = ? " + \
                         " AND path = ?", [catid, movie.GetRelativePath()])

        result = dbCursor.fetchone()

        separator = u"||"

        movieDict = {'cat':catid, 'name':movie.GetName(), 'path':movie.GetRelativePath()}

        infoDict = movie.GetInfoDict()
        for key, value in infoDict.iteritems():
            if isinstance(value, list):
                infoDict[key] = separator.join(value)
            elif isinstance(value, datetime):
                infoDict[key] = time.mktime(value.timetuple())

        parameterDict = dict(infoDict)
        parameterDict.update(movieDict)

        if result is None:
            # If the movie we are saving isn't present in the DB, INSERT
            dbCursor.execute("INSERT INTO movies (cat, name, path, image, title, " + \
                             "tmdb, year, rating, genres, overview, directors, actors, " + \
                             "moddate) VALUES (:cat, :name, :path, :image, :title, " + \
                             ":tmdb, :year, :rating, :genres, :overview, :directors, " + \
                             ":actors, :moddate)", parameterDict)
        else:
            # Else, if the movie is present in the DB, UPDATE
            dbCursor.execute("UPDATE movies SET image = :image, title = :title, " + \
                             "tmdb = :tmdb, year = :year, rating = :rating, " +  \
                             "genres = :genres, overview = :overview, directors = :directors, " + \
                             "actors = :actors, moddate = :moddate WHERE cat = :cat " +  \
                             "AND path = :path", parameterDict)

        self.__dbConn.commit()
        dbCursor.close()

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
                         [cat.GetRelativePath()])
        result = dbCursor.fetchone()
        catid = result['id']

        dbCursor.execute("DELETE FROM movies WHERE path = ? AND cat = ?", 
                         [movie.GetRelativePath(), catid])

        self.__dbConn.commit()
        dbCursor.close()

        return True

