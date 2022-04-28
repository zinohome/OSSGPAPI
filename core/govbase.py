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


class Govbase:
    def __init__(self):
        self._client = ArangoClient(hosts = os.getenv('ARANGODB_HOSTS'))
        self._db = self._client.db(name=os.getenv('ARANGODB_GOVDATABASE'), username=os.getenv('ARANGODB_GOVUSER'), password=os.getenv('ARANGODB_GOVPASSWORD'))

    @property
    def db(self):
        return Database(self._db)


