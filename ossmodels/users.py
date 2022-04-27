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
from arango_orm import Collection
from arango_orm.fields import String, Date
from marshmallow.fields import Bool

from core.userbase import Userbase
from env.environment import Environment
from util import log

'''logging'''
env = Environment()
log = log.Logger(level=os.getenv('OSSGPAPI_APP_LOG_LEVEL'))

class  Users(Collection):
    __collection__ = 'coldef'
    _index = [{'type':'hash', 'fields':['name'], 'unique':True}]
    _key = String(required=True)
    name = String(required=True, allow_none=False)
    password = String(required=True, allow_none=False)
    role = String(required=True, allow_none=False)
    active = Bool(required=True, allow_none=False)

if __name__ == '__main__':
    userbase = Userbase().db
    if not govbase.has_collection(Coldef):
        govbase.create_collection(Coldef)