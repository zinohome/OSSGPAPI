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
from marshmallow.fields import Integer

from core.govbase import Govbase
from env.environment import Environment
from util import log

'''logging'''
env = Environment()
log = log.Logger(level=os.getenv('OSSGPAPI_APP_LOG_LEVEL'))

class Sysdef(Collection):
    __collection__ = 'sysdef'
    _index = [{'type': 'hash', 'fields': ['name'], 'unique': True}]
    _key = String(required=True)
    name = String(required=True, allow_none=False)
    coltype = String(required=True, allow_none=False)
    keyfieldname = String(required=True, allow_none=False)
    coldef = String(required=True, allow_none=False)
    createdate = Date()

    def has_Sysdef_Collection(self):
        try:
            govbase = Govbase().db
            if govbase.has_collection(self.__collection__):
                return True
            else:
                return False
        except Exception as exp:
            log.logger.error('Exception at Sysdef.has_Sysdef_schema() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()
            return False;

    def existed_Sysdef(self, document_name):
        try:
            govbase = Govbase().db
            if govbase._db.has(Sysdef,document_name):
                return True
            else:
                return False
        except Exception as exp:
            log.logger.error('Exception at Sysdef.existed_Sysdef() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()
            return False

    def create_Sysdef(self, jsonobj):
        try:
            govbase = Govbase().db
            addjson = jsonobj
            if not addjson.__contains__('_key'):
                addjson['_key'] = addjson['name']
            if not govbase._db.has(Sysdef, addjson['_key']):
                addobj = Sysdef._load(addjson)
                govbase.add(addobj)
                return addobj.json
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at Sysdef.create_Sysdef() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()


    def get_all_Sysdef_names(self):
        try:
            count = self.get_Sysdef_count()
            limit = int(os.getenv('OSSGPADMIN_API_QUERY_LIMIT_UPSET'))
            querycount = count if count <= limit else limit
            govbase = Govbase().db
            records = govbase.query(Sysdef).limit(querycount).all()
            resultlist = []
            for record in records:
                resultlist.append(record.name)
            return resultlist
        except Exception as exp:
            log.logger.error('Exception at Sysdef.get_all_Sysdef_names() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def get_Sysdef_count(self):
        try:
            govbase = Govbase().db
            return govbase.query(Sysdef).count()
        except Exception as exp:
            log.logger.error('Exception at Sysdef.get_Sysdef_count() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def get_all_Sysdef(self):
        try:
            count = self.get_Sysdef_count()
            limit = int(os.getenv('OSSGPADMIN_API_QUERY_LIMIT_UPSET'))
            querycount = count if count <= limit else limit
            govbase = Govbase().db
            records = govbase.query(Sysdef).limit(querycount).all()
            resultlist = []
            for record in records:
                resultlist.append(record.json)
            return resultlist
        except Exception as exp:
            log.logger.error('Exception at Sysdef.get_all_Sysdef() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def get_Sysdef_bykey(self,keystr):
        try:
            returnjson = {}
            returnjson['count'] = 0
            returnjson['data'] = []
            govbase = Govbase().db
            if govbase._db.has(Sysdef,keystr):
                record = govbase.query(Sysdef).by_key(keystr)
                #returnjson['count'] = 1
                #returnjson['data'].append(record.json)
                returnjson = record.json
            return returnjson
        except Exception as exp:
            log.logger.error('Exception at Sysdef.get_Sysdef_bykey() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def get_Sysdef_byname(self,name):
        try:
            returnjson = {}
            returnjson['count'] = 0
            returnjson['data'] = []
            govbase = Govbase().db
            if govbase._db.has(Sysdef,name):
                records = govbase.query(Sysdef).filter("name=='"+name+"'").all()
                if len(records) >= 1:
                    #returnjson['count'] = 1
                    #returnjson['data'].append(records[0].json)
                    returnjson = records[0].json
            return returnjson
        except Exception as exp:
            log.logger.error('Exception at Sysdef.get_Sysdef_bykey() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def update_Sysdef(self, jsonobj):
        try:
            govbase = Govbase().db
            updatejson = jsonobj
            if not updatejson.__contains__('_key'):
                updatejson['_key'] = updatejson['name']
            if govbase._db.has(Sysdef, updatejson['_key']):
                updobj = Sysdef._load(updatejson)
                govbase.update(updobj)
                return updobj.json
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at Sysdef.update_Sysdef() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def delete_Sysdef(self,keystr):
        try:
            govbase = Govbase().db
            if govbase._db.has(Sysdef, keystr):
                return govbase.delete(govbase.query(Sysdef).by_key(keystr))
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at Sysdef.delete_Sysdef() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def query_Sysdef(self,queryjson):
        try:
            govbase = Govbase().db
            filter = queryjson['filter'] if 'filter' in queryjson else None
            filteror = queryjson['filteror'] if 'filteror' in queryjson else None
            sort = queryjson['sort'] if 'sort' in queryjson else None
            limit = queryjson['limit'] if 'limit' in queryjson else None
            offset = queryjson['offset'] if 'offset' in queryjson else None

            query = govbase.query(Sysdef)
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
            log.logger.error('Exception at Sysdef.query_Sysdef() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    @property
    def json(self):
        jdict = self.__dict__.copy()
        if jdict.__contains__('_dirty'):
            del jdict['_dirty']
        if jdict.__contains__('_refs_vals'):
            del jdict['_refs_vals']
        if jdict.__contains__('_instance_schema'):
            del jdict['_instance_schema']
        if jdict.__contains__('_db'):
            del jdict['_db']
        if jdict.__contains__('_key'):
            del jdict['_key']
        if jdict.__contains__('__collection__'):
            del jdict['__collection__']
        # jdict.update((k, str(v)) for k, v in jdict.items())
        return jdict

if __name__ == '__main__':
    govbase = Govbase().db
    coldefjson = {"__collection__": "coldef",
                       "_index": "[{'type':'hash', 'fields':['name'], 'unique':True}]",
                       "_key": "String(required=True)",
                       "name": "String(required=True, allow_none=False)",
                       "coltype": "String(required=True, allow_none=False)",
                       "keyfieldname": "String(required=True, allow_none=False)",
                       "coldef": "String(required=True, allow_none=False)",
                       "createdate": "String(required=True, allow_none=False)"}
    log.logger.debug("coldefjson: %s" % coldefjson)
    log.logger.debug("coldefjson: %s" % json.dumps(coldefjson))
    log.logger.debug("date.today(): %s" % date.today())
    tosysdef = Sysdef(_key="coldef",
                         name='coldef',
                         coltype="document",
                         keyfieldname="name",
                         coldef=json.dumps(coldefjson),  # 必须是string类型的json，不能是json对象
                         createdate=str(date.today()))
    if not tosysdef.has_Sysdef_Collection():
        govbase.create_collection(Sysdef)

    if not tosysdef.existed_Sysdef():
        resultstr = tosysdef.create_Sysdef(tosysdef.json)
        log.logger.debug('resultstr: %s' % resultstr)
    count = tosysdef.get_Sysdef_count()
    '''
    log.logger.debug('count: %s' % count)
    resultstr = tosysdef.get_all_Sysdef()
    log.logger.debug('resultstr: %s' % resultstr)
    resultstr = tosysdef.get_Sysdef_bykey('home')
    log.logger.debug('resultstr: %s' % resultstr)
    resultstr = tosysdef.get_Sysdef_byname('home-alt')
    log.logger.debug('resultstr: %s' % resultstr)
    tosysdef.title = '首页二'
    resultstr = tosysdef.delete_Sysdef(tosysdef.json)
    log.logger.debug('resultstr: %s' % resultstr)
    #resultstr = tosysdef.update_Sysdef('home-alt')
    #log.logger.debug('resultstr: %s' % resultstr)
    '''