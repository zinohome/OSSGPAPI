#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2022 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2022
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: OSSGPAPI
import traceback

import simplejson as json
import os
from datetime import date

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
    keyfieldname = String(required=True, allow_none=False)
    coldef = String(required=True, allow_none=False)
    createdate = Date()

    def check_col_schema(self, colname):
        try:
            govbase = Govbase().db
            if govbase.has(Coldef, colname):
                return True
            else:
                return False
        except Exception as exp:
            log.logger.error('Exception at coldef.check_col_schema() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()


if __name__ == '__main__':
    govbase = Govbase().db
    if not govbase.has_collection(Coldef):
        govbase.create_collection(Coldef)
    userscoldefjson = {"__collection__":"users",
                    "_index":"[{'type':'hash', 'fields':['name'], 'unique':True}]",
                    "_key":"String(required=True)",
                    "name":"String(required=True, allow_none=False)",
                    "password":"String(required=True, allow_none=False)",
                    "role":"String(required=True, allow_none=False)",
                    "active":"Bool(required=True, allow_none=False)"}
    log.logger.debug("userscoldef: %s" % userscoldefjson)
    log.logger.debug("userscoldefjson: %s" % json.dumps(userscoldefjson))
    log.logger.debug("date.today(): %s" % date.today())

    userscoldef = Coldef(_key="users",
                         name='users',
                         coltype="document",
                         coldef=json.dumps(userscoldefjson),
                         createdate=date.today())
    govbase.add(userscoldef)

