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
from arango_orm import Database, ConnectionPool

from env.environment import Environment
from util import log

'''logging'''
env = Environment()
log = log.Logger(level=os.getenv('OSSGPAPI_APP_LOG_LEVEL'))

class Systembase:
    def __init__(self):
        log.logger.info("OSSGPAPI - SysBase Connect to: %s" % os.getenv('ARANGODB_HOSTS'))
        self._client = ArangoClient(hosts = os.getenv('ARANGODB_HOSTS'))
        self._client1 = ArangoClient(hosts = os.getenv('ARANGODB_HOSTS'))
        self._client2 = ArangoClient(hosts = os.getenv('ARANGODB_HOSTS'))
        self._client3 = ArangoClient(hosts = os.getenv('ARANGODB_HOSTS'))
        self._noPooldb = self._client.db(name=os.getenv('ARANGODB_SYSDATABASE'), username=os.getenv('ARANGODB_SYSUSER'), password=os.getenv('ARANGODB_SYSPASSWORD'))
        self._cp = ConnectionPool([self._client1, self._client2, self._client3], dbname=os.getenv('ARANGODB_SYSDATABASE'), username=os.getenv('ARANGODB_SYSUSER'), password=os.getenv('ARANGODB_SYSPASSWORD'))
        #self.initgovbase()
        #self.inituserbase()

    @property
    def db(self):
        return self._cp._db

    def initgovbase(self):
        if not self._noPooldb.has_database(os.getenv('ARANGODB_GOVDATABASE')):
            self._noPooldb.create_database(
                name=os.getenv('ARANGODB_GOVDATABASE'),
                users=[
                    {'username':os.getenv('ARANGODB_GOVUSER'), 'password':os.getenv('ARANGODB_GOVPASSWORD'), 'active':True}
                ],
            )

    def inituserbase(self):
        if not self._noPooldb.has_database(os.getenv('ARANGODB_OSSDATABASE')):
            self._noPooldb.create_database(
                name=os.getenv('ARANGODB_OSSDATABASE'),
                users=[
                    {'username': os.getenv('ARANGODB_OSSUSER'), 'password': os.getenv('ARANGODB_OSSPASSWORD'),
                     'active': True}
                ],
            )