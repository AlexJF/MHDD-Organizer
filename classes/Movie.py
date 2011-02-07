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

import os, urllib, logging
from datetime import datetime
from infoproviders import tmdb

class Movie(object):
    """ The Movie class """

    def __init__(self, cat, name, path):
        """
        Constructor
        ---
        Params:
            @ cat (Category) - The category containing this movie.
            @ name (String) - The name of this movie object.
            @ path (String) - The path of this movie object relative to the
                              category path.
        """

        self.__category = cat
        self.__name = name
        self.__path = path
        self.__dirty = True
        self.__modDate = datetime.fromtimestamp(0)
        self.__title = u""
        self.__imdbID = u""
        self.__tmdbID = u""
        self.__year = u""
        self.__rating = 0
        self.__genres = []
        self.__overview = u""
        self.__directors = []
        self.__actors = []
        self.__imageData = None

    # -- Properties (Get) --
    def GetCategory(self):
        """
        Return: (Category) The category of the movie.
        """
        
        return self.__category

    def GetName(self):
        """
        Return: (UString) The title of the movie.
        """

        return self.__name

    def GetRelativePath(self):
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

    def GetTMDBID(self):
        """
        Return: (UString) The id of the tmdb entry associated with this movie.
        """

        return self.__tmdbID

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

    def GetOverview(self):
        """
        Return: (UString) The overview of the movie.
        """
        
        return self.__overview

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

    def GetImageData(self):
        """
        Return: (Buffer) The image representing this movie.
        """

        return self.__imageData

    # -- Properties (Set) --
    def SetModificationDate(self, date):
        """
        Sets the modification date of the movie.
        ---
        Params:
            @ date (datetime) - The new date of modification of the movie.
        """

        if isinstance(date, datetime):
            self.__modDate = date
        else:
            try:
                timestamp = float(date)
                self.__modDate = datetime.fromtimestamp(timestamp)
            except ValueError, e:
                self.__modDate = datetime.fromtimestamp(0)

    def SetTitle(self, title):
        """
        Sets the title of the movie.
        ---
        Params:
            @ title (UString) - The title of the movie.
        """

        self.__dirty = True
        self.__title = title

    def SetTMDBID(self, id):
        """
        Sets the TMDB id of the movie.
        ---
        Params:
            @ url (UString) - The TMDB id of the movie.
        """

        self.__dirty = True
        self.__tmdbID = id

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

        if not isinstance(rating, int):
            try:
                rating = int(rating)
            except ValueError, e:
                rating = 0

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

        if isinstance(genres, basestring):
            self.__dirty = True
            separator = u"||"
            self.__genres = genres.split(separator)
        elif isinstance(genres, list):
            self.__dirty = True
            self.__genres = genres

    def SetOverview(self, overview):
        """
        Sets the overview of the movie.
        ---
        Params:
            @ overview (UString) - The overview of the movie.
        """
        
        self.__dirty = True
        self.__overview = overview

    def SetDirectors(self, directors):
        """
        Sets the director of the movie.
        ---
        Params:
            @ director (List of UStrings) - The directors of the movie.
        """

        if isinstance(directors, basestring):
            self.__dirty = True
            separator = u"||"
            self.__directors = directors.split(separator)
        elif isinstance(directors, list):
            self.__dirty = True
            self.__directors = directors

    def SetActors(self, actors):
        """
        Sets the actors of the movie.
        ---
        Params:
            @ actors (List of UStrings) - The actors of the movie.
        """

        if isinstance(actors, basestring):
            self.__dirty = True
            separator = u"||"
            self.__actors = actors.split(separator)
        elif isinstance(actors, list):
            self.__dirty = True
            self.__actors = actors

    def SetImageData(self, image):
        """
        Sets the image of the movie.
        ---
        Params:
            @ image (Bytes) - Bytes containing image data.
        """

        self.__dirty = True
        self.__imageData = buffer(image)

    # -- Methods --
    def GetInfoDict(self):
        """
        Return: (Dict) An info dict containing all info of this movie
                object.
        """

        global getMethodsDict
        infoDict = dict()

        for key, value in getMethodsDict.iteritems():
            infoDict[key] = value(self)

        return infoDict

    def SetInfoFromDict(self, infoDict, dirty = False):
        """
        Sets movie info from an info dict.
        ---
        Params:
            @ infodict (Dict) - A dict object containing movie info.
            @ dirty (Boolean) - Is the dict coming directly from the
                                provider (thus not dirty) or from another
                                source (thus dirty).
        ---
        Return: (Boolean) True if info was loaded successfully,
                          False otherwise.
        """

        global setMethodsDict

        if infoDict is not None:
            for key, value in infoDict.iteritems():
                if value is None:
                    continue
                try:
                    function = setMethodsDict[key]
                    function(self, value)
                except KeyError, e:
                    pass

            self.__dirty = dirty
            return True
        else:
            return False

    def LoadInfoFromHdd(self):
        """
        Loads movie info from the Hdd.
        ---
        Return: (Boolean) True if info was loaded successfully,
                           False otherwise.
        """

        if not self.__dirty:
            return True

        infoDict = self.__category.GetHdd().LoadMovieInfo(self)

        return self.LoadInfoFromDict(infoDict)

    def SaveInfoToHdd(self):
        """
        Saves movie info to the HDD.
        ---
        Return: (Boolean) True if info was correctly saved or didn't need
                 to be saved, False if there was an error
        """

        if self.__dirty:
            movie.SetModificationDate(datetime.now())
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
        self.__overview = imdbMovieObj['overview'][0]
        
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
            self.SetImageData(imgData)
        except IOError, e:
            pass
        finally:
            if img is not None:
                img.close()

        self.__dirty = True

    def LoadInfoFromTMDB(self):
        """
        Loads the movie info from TMDB.
        """

        if (self.__tmdbID == ""):
            return

        mdb = tmdb.MovieDb()

        movieInfo = None

        try:
            movieInfo = mdb.getMovieInfo(self.__tmdbID)
        except tmdb.TmdNoResults, e:
            return

        self.SetTitle(movieInfo['name'])
        self.SetRating(movieInfo['rating'])
        self.SetOverview(movieInfo['overview'])
        self.SetYear(movieInfo['released'][0:4])
        genres = []
        try:
            for genre in movieInfo['categories']['genre'].keys():
                genres.append(genre)
        except KeyError, e:
            pass
        self.SetGenres(genres)
        directors = []
        try:
            for director in movieInfo['cast']['director']:
                directors.append(director['name'])
        except KeyError, e:
            pass
        self.SetDirectors(directors)
        actors = []
        try:
            for actor in movieInfo['cast']['actor']:
                actors.append(actor['name'])
        except KeyError, e:
            pass
        self.SetActors(actors)

        img = None

        try:
            img = urllib.urlopen(movieInfo['images'][0]['cover'])
            imgData = img.read()
            self.SetImageData(imgData)
        except KeyError, e:
            pass
        except IOError, e:
            pass
        finally:
            if img is not None:
                img.close()

        self.__dirty = True

setMethodsDict = dict()
setMethodsDict['title'] = Movie.SetTitle
setMethodsDict['tmdb'] = Movie.SetTMDBID
setMethodsDict['year'] = Movie.SetYear
setMethodsDict['rating'] = Movie.SetRating
setMethodsDict['overview'] = Movie.SetOverview
setMethodsDict['genres'] = Movie.SetGenres
setMethodsDict['directors'] = Movie.SetDirectors
setMethodsDict['actors'] = Movie.SetActors
setMethodsDict['image'] = Movie.SetImageData
setMethodsDict['moddate'] = Movie.SetModificationDate

getMethodsDict = dict()
getMethodsDict['title'] = Movie.GetTitle
getMethodsDict['tmdb'] = Movie.GetTMDBID
getMethodsDict['year'] = Movie.GetYear
getMethodsDict['rating'] = Movie.GetRating
getMethodsDict['overview'] = Movie.GetOverview
getMethodsDict['genres'] = Movie.GetGenres
getMethodsDict['directors'] = Movie.GetDirectors
getMethodsDict['actors'] = Movie.GetActors
getMethodsDict['image'] = Movie.GetImageData
getMethodsDict['moddate'] = Movie.GetModificationDate
