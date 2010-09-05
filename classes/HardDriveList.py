#! /usr/bin/env python

"""
File: HardDriveList.py
Author: Revolt
--------------------------
Desc:
    This file contains the definition and implementation of the 
    HardDriveList class
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

import wx, os
from classes.HardDrive import *

class HardDriveList:
    """ The HardDriveList class """

    configSync = False

    def __init__(self):
        """ Constructor """

        self.container = []

    def __len__(self):
        """ Returns the number of harddrives in the list """

        return len(self.container)

    def __getitem__(self, key):
        """ Returns the harddrive with the specified key """

        if isinstance(key, int):
            return self.container[key]
        else:
            raise TypeError

    def __iter__(self):
        """ Allows iteration over the container """

        for harddrive in self.container:
            yield harddrive

    def Add(self, hardDrive):
        """ Adds a new harddrive to the list """

        if not isinstance(hardDrive, HardDrive):
            raise TypeError

        if not hardDrive.GetLabel() or not hardDrive.GetPath():
            return False

        self.container.append(hardDrive)

        if self.configSync:
            config = wx.Config.Get()
            config.SetPath("/drives")

            config.SetPath(hardDrive.GetUuid())
            config.Write("Label", hardDrive.GetLabel())
            config.Write("Path", hardDrive.GetPath())

    def Edit(self, index, newHardDrive):
        """
        Edits the harddrive located at the specified index with
        data from the newHardDrive object
        ---
        Params:
            @ index - Index of the harddrive to edit
            @ newHardDrive - HardDrive object with modified data
        """

        if not newHardDrive.GetLabel() or not newHardDrive.GetPath():
            return

        hardDrive = self.container[index]

        hardDrive.SetLabel(newHardDrive.GetLabel())
        hardDrive.SetPath(newHardDrive.GetPath())
        hardDrive.SetCategoryList(newHardDrive.GetCategoryList())
        hardDrive.SaveCategoryList()

    def Remove(self, index):
        """ Removes a harddrive from the list """

        if self.configSync:
            hdd = self.container[index]

            config = wx.Config.Get()
            config.SetPath("/drives")

            if config.HasGroup(hdd.GetUuid()):
                config.DeleteGroup(hdd.GetUuid())

        del self.container[index]

    def SaveToConfig(self, configSync = True):
        """
        Overwrites all stored HDDs in the config with the ones specified
        in this list.
        If configSync == True then every operation performed
        on the list after this command will be reflected on the 
        configuration file of the application.
        """

        self.configSync = configSync

        config = wx.Config.Get()
        config.DeleteGroup("/drives")
        config.SetPath("/drives")

        for hardDrive in self.container:
            config.Write(hardDrive.GetUuid() + "/Label", hardDrive.GetLabel())
            config.Write(hardDrive.GetUuid() + "/Path", hardDrive.GetPath())
        

    def LoadFromConfig(self, configSync = True):
        """ 
        Loads the hard drive list from the app's config
        after clearing the current list.
        If configSync == True then every operation performed
        on the list after this command will be reflected on the 
        configuration file of the application.
        """

        self.container = []
        self.configSync = configSync

        config = wx.Config.Get()
        config.SetPath("/drives")

        (moreDrives, uuid, nextDriveIndex) = config.GetFirstGroup()

        while moreDrives:
            hdd = HardDrive(uuid, config.Read(uuid + "/Label"), config.Read(uuid + "/Path"))

            if hdd.GetLabel() and hdd.GetPath():
                self.container.append(hdd)
        
            (moreDrives, uuid, nextDriveIndex) = config.GetNextGroup(nextDriveIndex)

    def StopConfigSync():
        """
        Allows the user to stop syncing between the config and this list.
        Please note that the only way to activate config syncing is by
        loading (or saving) the list from (to) the config.
        All changes made while syncing are kept.
        """

        configSync = False