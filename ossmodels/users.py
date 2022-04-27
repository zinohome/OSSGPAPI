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

from core.ossbase import Ossbase
from env.environment import Environment
from util import log

'''logging'''
env = Environment()
log = log.Logger(level=os.getenv('OSSGPAPI_APP_LOG_LEVEL'))

class  Users(Collection):
    __collection__ = 'users'
    _index = [{'type':'hash', 'fields':['name'], 'unique':True}]
    _key = String(required=True)
    name = String(required=True, allow_none=False)
    password = String(required=True, allow_none=False)
    role = String(required=True, allow_none=False)
    active = Bool(required=True, allow_none=False)

    def initsyscount(self):
        try:
            ossbase = Ossbase().db
            if not ossbase.has_collection(Users):
                ossbase.create_collection(Users)
            adminuser = Users(_key="admin", name="admin", password="passw0rd", role="[admin]", active=True)
            if not ossbase.has(Users, 'admin'):
                ossbase.add(adminuser)
        except Exception as exp:
            log.logger.error('Exception at gen_schema() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()


    def __str__(self):
        return "<Users({},{},{},{})>".format(self._key, self.name, self.role, self.active)


if __name__ == '__main__':
    ossbase = Ossbase().db
    if not ossbase.has_collection(Users):
        ossbase.create_collection(Users)
    adminuser = Users(_key="admin", name="admin", password="passw0rd", role="[admin]", active=True)
    if not ossbase.has(Users,'admin'):
        ossbase.add(adminuser)
    log.logger.debug("Users count: %s" % ossbase.query(Users).count())