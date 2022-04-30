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
from core.ossbase import Ossbase
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

    def has_Coldef_schema(self, name):
        try:
            govbase = Govbase().db
            if govbase.has(Coldef, name):
                return True
            else:
                return False
        except Exception as exp:
            log.logger.error('Exception at coldef.has_col_schema() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def col_existed(self, name):
        try:
            ossbase = Ossbase().db
            if ossbase.has_collection(self.name):
                return True
            else:
                return False
        except Exception as exp:
            log.logger.error('Exception at coldef.col_existed() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def get_Coldef_count(self):
        try:
            govbase = Govbase().db
            return govbase.query(Coldef).count()
        except Exception as exp:
            log.logger.error('Exception at Coldef.get_Coldef_count() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def create_Coldef(self, jsonstr):
        try:
            govbase = Govbase().db
            addjson = jsonstr
            if not addjson.__contains__('_key'):
                addjson['_key'] = addjson['name']
            if not govbase.has(Coldef, addjson['_key']):
                addobj = Coldef._load(addjson)
                govbase.add(addobj)
                return addobj.json
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at Coldef.create_Coldef() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def get_Coldef_bykey(self,keystr):
        try:
            govbase = Govbase().db
            if govbase.has(Coldef,keystr):
                record = govbase.query(Coldef).by_key(keystr)
                return record.json
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at Coldef.get_Coldef_bykey() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def get_Coldef_byname(self,name):
        try:
            govbase = Govbase().db
            if govbase.has(Coldef,name):
                log.logger.error(name)
                records = govbase.query(Coldef).filter("name=='"+name+"'").all()
                if len(records) >= 1:
                    getreturn = records[0].json
                    return getreturn
                else:
                    return None
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at Coldef.get_Coldef_byname() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def update_Coldef(self, jsonstr):
        try:
            govbase = Govbase().db
            updatejson = jsonstr
            if not updatejson.__contains__('_key'):
                updatejson['_key'] = updatejson['name']
            if govbase.has(Coldef, updatejson['_key']):
                govbase = Coldef._load(updatejson)
                govbase.update(updatejson)
                return updatejson.json
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at Coldef.update_Coldef() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def delete_Coldef(self,keystr):
        try:
            govbase = Govbase().db
            if govbase.has(Coldef, keystr):
                #log.logger.debug(govbase.delete(govbase.query(Coldef).by_key(keystr)))
                return govbase.delete(govbase.query(Coldef).by_key(keystr))
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at Coldef.delete_Coldef() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def query_Coldef(self,queryjson):
        try:
            govbase = Govbase().db
            filter = queryjson['filter'] if 'filter' in queryjson else None
            filteror = queryjson['filteror'] if 'filteror' in queryjson else None
            sort = queryjson['sort'] if 'sort' in queryjson else None
            limit = queryjson['limit'] if 'limit' in queryjson else None
            offset = queryjson['offset'] if 'offset' in queryjson else None

            query = govbase.query(Coldef)
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
            log.logger.error('Exception at Coldef.query_Coldef() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    @property
    def json(self):
        jdict = self.__dict__.copy()
        del jdict['_dirty']
        del jdict['_refs_vals']
        del jdict['_instance_schema']
        del jdict['_db']
        del jdict['_key']
        #del jdict['__collection__']
        # jdict.update((k, str(v)) for k, v in jdict.items())
        return jdict

if __name__ == '__main__':
    govbase = Govbase().db
    coldef = Coldef()
    log.logger.debug("Coldef.get_Coldef_bykey('users'): %s" % coldef.get_Coldef_bykey('users'))
    log.logger.debug("Coldef.get_Coldef_byname('users'): %s" % coldef.get_Coldef_byname('users'))

    '''
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
                         keyfieldname="name",
                         coldef=userscoldefjson,
                         createdate=date.today())
    if userscoldef.has_Coldef_schema(userscoldef.name):
        if not userscoldef.col_existed():
            govbase.add(userscoldef)
    '''

