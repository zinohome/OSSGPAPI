#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus

from typing import Optional
from sqlalchemy import Column, VARCHAR
from sqlmodel import Field, SQLModel
from datetime import date, timedelta, time, datetime
import decimal

from config import config
from core.dbmeta import DBMeta
from util import log, toolkit

'''config'''
cfg = config.app_config

'''logging'''
log = log.Logger(level=cfg['Application_Config'].app_log_level)

'''meta'''
meta = DBMeta()

class ogdbuser(SQLModel, table=True):
    ogdbuser_id: Optional[str] = Field(default=None, primary_key=True)
    ogdbuser_name: str = Field(sa_column=Column("ogdbuser_name", default=None, primary_key=False))
    ogdbuser_password: str = Field(sa_column=Column("ogdbuser_password", default=None, primary_key=False))
    ogdbuser_active: str = Field(sa_column=Column("ogdbuser_active", default=None, primary_key=False))
    ogdb_id: str = Field(sa_column=Column("ogdb_id", default=None, primary_key=False))

    def sortJson(self):
        return self.json(sort_keys=True)

    def getTableSchema(self):
        return meta.gettable('ogdbuser')

    def getPrimaryKeys(self):
        return meta.gettable('ogdbuser').primarykeys

    def getPKType(self,pkname):
        return meta.get_table_pk_type('ogdbuser',pkname)

    def getpkqmneed(self,pkname):
        return meta.get_table_pk_qmneed('ogdbuser',pkname)