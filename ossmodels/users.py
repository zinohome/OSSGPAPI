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
import traceback
import simplejson as json
from arango_orm import Collection
from arango_orm.fields import String, Date
from marshmallow.fields import Bool

from core.ossbase import Ossbase
from env.environment import Environment
from util import log

'''logging'''
env = Environment()
log = log.Logger(level=os.getenv('OSSGPAPI_APP_LOG_LEVEL'))

class Users(Collection):
    __collection__ = 'users'
    _index = [{'type':'hash', 'fields':['name'], 'unique':True}]
    _key = String(required=True)
    name = String(required=True, allow_none=False)
    password = String(required=True, allow_none=False)
    role = String(required=True, allow_none=False)
    active = Bool(required=True, allow_none=False)

    def getUserscount(self):
        try:
            ossbase = Ossbase().db
            return ossbase.query(Users).count()
        except Exception as exp:
            log.logger.error('Exception at users.getuserscount() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def createUsers(self, jsonstr):
        try:
            ossbase = Ossbase().db
            addjson = json.loads(jsonstr)
            if not ossbase.has(Users, addjson['name']):
                if not addjson.__contains__('_key'):
                    addjson['_key'] = addjson['name']
                addobj = Users._load(addjson)
                ossbase.add(addobj)
                return addobj
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at users.createUsers() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def getUsersbyname(self,username):
        try:
            ossbase = Ossbase().db
            if ossbase.has(Users,username):
                records = ossbase.query(Users).filter("name=='"+username+"'").all()
                if len(records) >= 1:
                    authreturn = {}
                    authreturn['name'] = records[0].name
                    authreturn['role'] = records[0].role
                    #authreturn['password'] = records[0].password
                    authreturn['active'] = records[0].active
                    return authreturn
                else:
                    return None
            else:
                return {"Authentication":False}
        except Exception as exp:
            log.logger.error('Exception at users.getUsersbyname() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def updateUsers(self, jsonstr):
        pass

    def deleteUsers(self,keystr):
        pass

    def queryUsers(self,queryjson):
        pass

    def userlogin(self,username,password):
        try:
            ossbase = Ossbase().db
            if ossbase.has(Users,username):
                records = ossbase.query(Users).filter("name=='"+username+"'").filter("password=='"+password+"'").filter("active==True").all()
                if len(records) >= 1:
                    authreturn = {"Authentication":True}
                    authreturn['name'] = records[0].name
                    authreturn['role'] = records[0].role
                    authreturn['active'] = records[0].active
                    return authreturn
                else:
                    return {"Authentication": False}
            else:
                return {"Authentication":False}
        except Exception as exp:
            log.logger.error('Exception at users.userlogin() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def initsysUsers(self):
        # Only called at application start
        try:
            ossbase = Ossbase().db
            if not ossbase.has_collection(Users):
                ossbase.create_collection(Users)
            adminuser = Users(_key="admin", name="admin", password="passw0rd", role="[admin]", active=True)
            if not ossbase.has(Users, 'admin'):
                ossbase.add(adminuser)
        except Exception as exp:
            log.logger.error('Exception at users.initsyscount() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def __str__(self):
        return "<Users({},{},{},{})>".format(self._key, self.name, self.role, self.active)

    def __str__(self):
        return "<Users({},{},{},{})>".format(self._key, self.name, self.role, self.active)


if __name__ == '__main__':
    ossbase = Ossbase().db
    tu = Users()
    adminuser = Users(_key="admin", name="admin", password="passw0rd", role="[admin]", active=True)
    if not ossbase.has(Users,'admin'):
        ossbase.add(adminuser)
    newuser = '{"role": "[admin]","active": true,"name": "Tony","password": "passw0rd"}'
    au = tu.createUsers(newuser)
    log.logger.debug(tu.userlogin('zhangjun','passw0rd'))
    log.logger.debug(tu.getUsersbyname('zhangjun'))
    log.logger.debug("Users count: %s" % tu.getUserscount())