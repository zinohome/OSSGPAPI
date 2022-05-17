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
from arango_orm import Database
from env.environment import Environment
from arango_orm import ConnectionPool
from util import log

'''logging'''
env = Environment()
log = log.Logger(level=os.getenv('OSSGPAPI_APP_LOG_LEVEL'))


class Govbase:
    def __init__(self):
        log.logger.info("OSSGPAPI - GovBase Connect to: %s" % os.getenv('ARANGODB_HOSTS'))
        #self._client = ArangoClient(hosts = os.getenv('ARANGODB_HOSTS'))
        #self._db = self._client.db(name=os.getenv('ARANGODB_GOVDATABASE'), username=os.getenv('ARANGODB_GOVUSER'), password=os.getenv('ARANGODB_GOVPASSWORD'))
        self._client1 = ArangoClient(hosts = os.getenv('ARANGODB_HOSTS'))
        self._client2 = ArangoClient(hosts = os.getenv('ARANGODB_HOSTS'))
        self._client3 = ArangoClient(hosts = os.getenv('ARANGODB_HOSTS'))
        self._db = ConnectionPool([self._client1, self._client2, self._client3], dbname=os.getenv('ARANGODB_GOVDATABASE'), username=os.getenv('ARANGODB_GOVUSER'), password=os.getenv('ARANGODB_GOVPASSWORD'))

    @property
    def db(self):
        return Database(self._db)



