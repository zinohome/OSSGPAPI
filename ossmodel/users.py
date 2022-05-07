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
            addjson = jsonstr
            if not addjson.__contains__('_key'):
                addjson['_key'] = addjson['name']
            if not ossbase.has(Users, addjson['_key']):
                addobj = Users._load(addjson)
                ossbase.add(addobj)
                return addobj.json
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at users.createUsers() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def getUsersbykey(self,keystr):
        try:
            ossbase = Ossbase().db
            if ossbase.has(Users,keystr):
                record = ossbase.query(Users).by_key(keystr)
                return record.json
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at users.getUsersbyname() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def updateUsers(self, jsonstr):
        try:
            ossbase = Ossbase().db
            updatejson = jsonstr
            if not updatejson.__contains__('_key'):
                updatejson['_key'] = updatejson['name']
            if ossbase.has(Users, updatejson['_key']):
                updatejson = Users._load(updatejson)
                ossbase.update(updatejson)
                return updatejson.json
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at users.updateUsers() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def deleteUsers(self,keystr):
        try:
            ossbase = Ossbase().db
            if ossbase.has(Users, keystr):
                #log.logger.debug(ossbase.delete(ossbase.query(Users).by_key(keystr)))
                return ossbase.delete(ossbase.query(Users).by_key(keystr))
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at users.deleteUsers() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def queryUsers(self,queryjson):
        try:
            ossbase = Ossbase().db
            filter = queryjson['filter'] if 'filter' in queryjson else None
            filteror = queryjson['filteror'] if 'filteror' in queryjson else None
            sort = queryjson['sort'] if 'sort' in queryjson else None
            limit = queryjson['limit'] if 'limit' in queryjson else None
            offset = queryjson['offset'] if 'offset' in queryjson else None

            query = ossbase.query(Users)
            if filter is not None:
                for flstr in filter:
                    query.filter(flstr)
            if filteror is not None:
                for flstr in filteror:
                    query.filter(flstr, _or=True)
            if sort is not None:
                query.sort(sort)
            if limit is not None:
                query.limit(limit)
            if ( limit is not None ) & ( offset is not None ):
                query.limit(limit, start_from=offset)
            returnjson = {}
            returnjson['count'] = query.count()
            returnjson['data'] = []
            for obj in query.all():
                returnjson['data'].append(obj.json)
            return returnjson
        except Exception as exp:
            log.logger.error('Exception at users.queryUsers() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

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
            log.logger.error('Exception at users.initsysUsers() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def __str__(self):
        return "<Users({},{},{},{})>".format(self._key, self.name, self.role, self.active)

    @property
    def json(self):
        jdict = self.__dict__.copy()
        del jdict['_dirty']
        del jdict['_refs_vals']
        del jdict['_instance_schema']
        del jdict['_db']
        del jdict['_key']
        #del jdict['__collection__']
        #jdict.update((k, str(v)) for k, v in jdict.items())
        return jdict


if __name__ == '__main__':
    ossbase = Ossbase().db
    tu = Users()
    adminuser = Users(_key="admin", name="admin", password="passw0rd", role="[admin]", active=True)
    if not ossbase.has(Users,'admin'):
        ossbase.add(adminuser)
    newuser = '{"role": "[admin]","active": true,"name": "Tony","password": "passw0rd"}'
    au = tu.createUsers(json.loads(newuser))
    log.logger.debug(tu.userlogin('zhangjun','passw0rd'))
    log.logger.debug(tu.getUsersbyname('zhangjun'))
    log.logger.debug("Users count: %s" % tu.getUserscount())
    upduser = '{"role": "[admin,user]","active": true,"name": "Tony","password": "passw0rd"}'
    uu = tu.updateUsers(json.loads(upduser))
    log.logger.debug("updated user: %s" % uu)
    log.logger.debug("updated user: %s" % dir(uu))
    log.logger.debug("updated user: %s" % uu)
    #log.logger.debug(tu.deleteUsers('Tony'))

    '''
    filterstr = queryjson['filter'] if 'filter' in queryjson else None
    filterorstr = queryjson['filteror'] if 'filteror' in queryjson else None
    sortstr = queryjson['sort'] if 'sort' in queryjson else None
    limit = queryjson['sort'] if 'sort' in queryjson else None
    offset = queryjson['offset'] if 'offset' in queryjson else None
    '''
    qjson = {
        'filter': ['name=="zhangjun"', 'name=="zhangjun"'],
        'filteror': ['name=="admin"'],
        'sort': 'name ASC',
        'limit': 1,
        'offset': 1
    }
    log.logger.debug(qjson)
    log.logger.debug(tu.queryUsers(qjson))
