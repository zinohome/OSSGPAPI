#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2022 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2022
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: OSSGPAPI


'''logging'''
import os
from arango_orm import Collection
from arango_orm.fields import String, Date

from core.govbase import Govbase
from env.environment import Environment
from util import log

'''logging'''
env = Environment()
log = log.Logger(level=os.getenv('OSSGPAPI_APP_LOG_LEVEL'))

class Coldef(Collection):
    __collection__ = 'coldef'
    _index = [{'type':'hash', 'fields':['name'], 'unique':True}]
    _key = String(required=True)
    name = String(required=True, allow_none=False)
    coltype = String(required=True, allow_none=False)
    coldef = String(required=True, allow_none=False)
    createdate = Date()

if __name__ == '__main__':
    govbase = Govbase().db
    if not govbase.has_collection(Coldef):
        govbase.create_collection(Coldef)

