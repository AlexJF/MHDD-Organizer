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
        Reads the category list of the HDD from the DB and returns it.
        ---
        Return: (List of Categories) The categories pertaining to the
                 hdd associated with this provider.
        """

        categoryList = []

        dbCursor = self.__dbConn.cursor()

        dbCursor.execute("SELECT * FROM categories")

        for row in dbCursor:
            cat = Category(row[1], row[2], self.GetHdd())
            categoryList.append(cat)

        self.__logger.debug("Read %d categories from the DB (%s)", 
                            len(categoryList), self.GetHdd.GetUuid())

        return categoryList


    def SaveCategoryList(self):
        """
        Saves category list of the associated hdd into the DB.
        ---
        Return: (Boolean) True on success, false otherwise
        """

        dbCursor = self.__dbConn.cursor()

        dbCatList = self.LoadCategoryList()
        hddCatList = self.GetHdd().GetCategoryList()

        updateList = []
        deleteList = []

        i = 0
        for dbCat in dbCatList:
            j = 0
            for hddCat in hddCatList:
                # Category is present in both places so UPDATE
                if dbCat.GetPath() == hddCat.GetPath():
                    updateList.append(hddCat)
                    hddCatList.pop(j)
                    break
                j += 1
            else:
                # Category is only present in  the DB so DELETE

        # What was left in hddCatList are the categories
        # not present in the DB so INSERT
        insertList = hddCatList

        for cat in updateList:
            dbCursor.execute("UPDATE categories SET name = ? WHERE path = ?",
                             cat.GetName(),
                             cat.GetPath())

        for cat in deleteList:
            dbCursor.execute("DELETE FROM categories WHERE path = ?", cat.GetPath())

        for cat in insertList:
            dbCursor.execute("INSERT INTO categories (id, name, path)
                              VALUES (, ?, ?)", cat.GetName(), cat.GetPath())

        self.__dbConn.commit()

        self.__logger.debug("Successfully wrote %d categories to the DB (%s)", 
                            len(categoryList),
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
        separator = u"||"

        dbCursor = self.__dbConn.cursor()

        dbCursor.execute("SELECT movies.* FROM movies INNER JOIN categories " + 
                         "ON categories.id = movies.cat WHERE categories.path = ?"
                         cat.GetPath())

        for movieData in dbCursor:
            movie = Movie(cat, movieData['name'], movieData['path'])
            movie.SetImageData(movieData['image'])
            movie.SetTitle(movieData['title'])
            movie.SetIMDBID(movieData['imdb'])
            movie.SetYear(movieData['year'])
            movie.SetRating(movieData['rating'])
            movie.SetGenres(movieData['genres'].split(separator))
            movie.SetPlot(movieData['plot'])
            movie.SetDirectors(movieData['directors'].split(separator))
            movie.SetActors(movieData['actors'].split(separator))
            movie.SetModificationDate(time.fromtimestamp(movieData['moddate']))

            movieList.append(movie)

        self.__logger.debug("Loaded %d movies from category '%s'", len(movieList), cat.GetName())

        return movieList

    def SaveCategoryMovieList(self, cat):
        """
        Saves all movies contained in the provided category.
        ---
        Params:
            @ cat (Category) - The category whose movies we wish to save.
        """

        self.__logger.debug("Saving all movies inside the provided category '%s'",
                            cat.GetName())

        existingMovieList = self.LoadCategoryMovieList()
        newMovieList = cat.GetMovieList()
        deleteList = []

        found = False

        for existingmovie in existingMovieList:
            found = False

            for movie in newMovieList:
                if movie.GetRelativePath() == existingMovie.GetRelativePath():
                    found = True
                    break

            if not found:
                deleteList.append(existingMovie)

        for movie in newMovieList:
            self.SaveMovieInfo(movie)

        if len(deleteList) > 0:
            dbCursor = self.__dbConn.cursor()

            dbCursor.execute("SELECT id FROM categories WHERE path = ?", cat.GetRelativePath())
            result = dbCursor.fetchone()

            catid = result['id']

            for movie in deleteList:
                dbCursor.execute("DELETE FROM movies WHERE path = ? AND cat = ?", 
                                 movie.GetRelativePath(), catid)

        return True

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

        dbCursor = self.__dbConn.cursor()

        dbCursor.execute("SELECT * FROM movies WHERE movies.path = ?", movie.GetRelPath())

        movieData = dbCursor.fetchone()

        movie.SetImageData(movieData['image'])
        movie.SetTitle(movieData['title'])
        movie.SetIMDBID(movieData['imdb'])
        movie.SetYear(movieData['year'])
        movie.SetRating(movieData['rating'])
        movie.SetGenres(movieData['genres'].split(separator))
        movie.SetPlot(movieData['plot'])
        movie.SetDirectors(movieData['directors'].split(separator))
        movie.SetActors(movieData['actors'].split(separator))
        movie.SetModificationDate(datetime.fromtimestamp(movieData['moddate']))

        return True

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

        if len(result) == 0:
            # If the movie we are saving isn't present in the DB, INSERT
            dbCursor.execute("INSERT INTO movies (id, cat, name, path, image, title, " +
                             "imdb, year, rating, genres, plot, directors, actors, " +
                             "modddate) VALUES (, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                             catid, movie.GetName(), movie.GetRelativePath(),
                             movie.GetImageData(), movie.GetTitle(), movie.GetIMDBID(),
                             movie.GetYear(), movie.GetRating(), 
                             separator.join(movie.GetGenres()), movie.GetPlot(),
                             separator.join(movie.GetDirectors()),
                             separator.join(movie.GetActors()),
                             movie.GetModificationDate())
        else:
            # Else, if the movie is present in the DB, UPDATE
            dbCursor.execute("UPDATE movies SET image = ?, title = ?, imdb = ?, " +
                             "year = ?, rating = ?, genres = ?, plot = ?, directors = ?, " +
                             "actors = ?, moddate = ? WHERE cat = ? AND path = ?",
                             movie.GetImageDate(), movie.GetTitle(),
                             movie.GetIMDBID(), movie.GetYear(), movie.GetRating(),
                             separator.join(movie.GetGenres()), movie.GetPlot(),
                             separator.join(movie.GetDirectors()),
                             separator.join(movie.GetActors()),
                             movie.GetModificationDate(), catid, movie.GetRelativePath())

        return True
