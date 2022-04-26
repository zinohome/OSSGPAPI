#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2022 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2022
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: OSSGPAPI

import os
from arango import ArangoClient

class Systembase:
    def __init__(self):
        self._client = ArangoClient(hosts = os.getenv('ARANGODB_HOSTS'))
        self._db = self._client.db(name=os.getenv('ARANGODB_SYSDATABASE'), username=os.getenv('ARANGODB_SYSUSER'), password=os.getenv('ARANGODB_SYSPASSWORD'))
        self.initgovbase()
        self.inituserbase()

    @property
    def db(self):
        return self._db

    def initgovbase(self):
        if not self._db.has_database(os.getenv('ARANGODB_GOVDATABASE')):
            self._db.create_database(
                name=os.getenv('ARANGODB_GOVDATABASE'),
                users=[
                    {'username':os.getenv('ARANGODB_GOVUSER'), 'password':os.getenv('ARANGODB_GOVPASSWORD'), 'active':True}
                ],
            )

    def inituserbase(self):
        if not self._db.has_database(os.getenv('ARANGODB_OSSDATABASE')):
            self._db.create_database(
                name=os.getenv('ARANGODB_OSSDATABASE'),
                users=[
                    {'username': os.getenv('ARANGODB_OSSUSER'), 'password': os.getenv('ARANGODB_OSSPASSWORD'),
                     'active': True}
                ],
            )