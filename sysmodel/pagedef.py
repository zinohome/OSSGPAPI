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

class Pagedef(Collection):
    __collection__ = 'pagedef'
    _index = [{'type':'hash', 'fields':['name'], 'unique':True}]
    _key = String(required=True)
    name = String(required=True, allow_none=False)
    level = Integer(required=True, allow_none=False)
    createdate = Date()

    def has_Pagedef_Collection(self, document_name):
        try:
            govbase = Govbase().db
            if govbase.has_collection(Pagedef, document_name):
                return True
            else:
                return False
        except Exception as exp:
            log.logger.error('Exception at Pagedef.has_Pagedef_schema() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()
            return False;

    def existed_Pagedef(self):
        try:
            govbase = Govbase().db
            if govbase.has(Pagedef,self.name):
                return True
            else:
                return False
        except Exception as exp:
            log.logger.error('Exception at Pagedef.existed_Pagedef() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()
            return False

    def create_Pagedef(self, jsonobj):
        try:
            govbase = Govbase().db
            addjson = jsonobj
            if not addjson.__contains__('_key'):
                addjson['_key'] = addjson['name']
            if not govbase.has(Pagedef, addjson['_key']):
                addobj = Pagedef._load(addjson)
                govbase.add(addobj)
                return addobj.json
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at Pagedef.create_Pagedef() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()


    def get_all_Pagedef_names(self):
        try:
            count = self.get_Pagedef_count()
            limit = int(os.getenv('OSSGPADMIN_API_QUERY_LIMIT_UPSET'))
            querycount = count if count <= limit else limit
            govbase = Govbase().db
            records = govbase.query(Pagedef).limit(querycount).all()
            resultlist = []
            for record in records:
                resultlist.append(record.name)
            return resultlist
        except Exception as exp:
            log.logger.error('Exception at Pagedef.get_all_Pagedef_names() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def get_Pagedef_count(self):
        try:
            govbase = Govbase().db
            return govbase.query(Pagedef).count()
        except Exception as exp:
            log.logger.error('Exception at Pagedef.get_Pagedef_count() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def get_all_Pagedef(self):
        try:
            count = self.get_Pagedef_count()
            limit = int(os.getenv('OSSGPADMIN_API_QUERY_LIMIT_UPSET'))
            querycount = count if count <= limit else limit
            govbase = Govbase().db
            records = govbase.query(Pagedef).limit(querycount).all()
            resultlist = []
            for record in records:
                resultlist.append(record.json)
            return resultlist
        except Exception as exp:
            log.logger.error('Exception at Pagedef.get_all_Pagedef() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def get_Pagedef_bykey(self,keystr):
        try:
            returnjson = {}
            returnjson['count'] = 0
            returnjson['data'] = []
            govbase = Govbase().db
            if govbase.has(Pagedef,keystr):
                record = govbase.query(Pagedef).by_key(keystr)
                returnjson['count'] = 1
                returnjson['data'].append(record.json)
            return returnjson
        except Exception as exp:
            log.logger.error('Exception at Pagedef.get_Pagedef_bykey() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def get_Pagedef_byname(self,name):
        try:
            returnjson = {}
            returnjson['count'] = 0
            returnjson['data'] = []
            govbase = Govbase().db
            if govbase.has(Pagedef,name):
                records = govbase.query(Pagedef).filter("name=='"+name+"'").all()
                if len(records) >= 1:
                    returnjson['count'] = 1
                    returnjson['data'].append(records[0].json)
            return returnjson
        except Exception as exp:
            log.logger.error('Exception at Pagedef.get_Pagedef_bykey() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def update_Pagedef(self, jsonobj):
        try:
            govbase = Govbase().db
            updatejson = jsonobj
            if not updatejson.__contains__('_key'):
                updatejson['_key'] = updatejson['name']
            if govbase.has(Pagedef, updatejson['_key']):
                updobj = Pagedef._load(updatejson)
                govbase.update(updobj)
                return updobj.json
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at Pagedef.update_Pagedef() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def delete_Pagedef(self,keystr):
        try:
            govbase = Govbase().db
            if govbase.has(Pagedef, keystr):
                return govbase.delete(govbase.query(Pagedef).by_key(keystr))
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at Pagedef.delete_Pagedef() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def query_Pagedef(self,queryjson):
        try:
            govbase = Govbase().db
            filter = queryjson['filter'] if 'filter' in queryjson else None
            filteror = queryjson['filteror'] if 'filteror' in queryjson else None
            sort = queryjson['sort'] if 'sort' in queryjson else None
            limit = queryjson['limit'] if 'limit' in queryjson else None
            offset = queryjson['offset'] if 'offset' in queryjson else None

            query = govbase.query(Pagedef)
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
            log.logger.error('Exception at Pagedef.query_Pagedef() %s ' % exp)
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
    '''
    topagedef= Pagedef(name = 'home-alt',
                       title = '首页',
                       level = '1',
                       order = '1',
                       segment = 'index',
                       liclass = 'nav-item',
                       hrefclass = 'nav-link',
                       navclass = '',
                       href = 'index.html',
                       icon = 'typcn typcn-chart-area-outline',
                       createdate = str(date.today())
                       )
    #log.logger.debug("topagedef.has_Pagedef_Collection(): %s" % topagedef.has_Pagedef_Collection())
    #log.logger.debug("topagedef.existed_Pagedef(): %s" % topagedef.existed_Pagedef())
    log.logger.debug('topagedef.json: %s' % topagedef.json)
    if not topagedef.has_Pagedef_Collection():
        govbase.create_collection(Pagedef)
    if not topagedef.existed_Pagedef():
        resultstr = topagedef.create_Pagedef(topagedef.json)
        log.logger.debug('resultstr: %s' % resultstr)
    count = topagedef.get_Pagedef_count()
    log.logger.debug('count: %s' % count)
    resultstr = topagedef.get_all_Pagedef()
    log.logger.debug('resultstr: %s' % resultstr)
    resultstr = topagedef.get_Pagedef_bykey('home')
    log.logger.debug('resultstr: %s' % resultstr)
    resultstr = topagedef.get_Pagedef_byname('home-alt')
    log.logger.debug('resultstr: %s' % resultstr)
    topagedef.title = '首页二'
    resultstr = topagedef.delete_Pagedef(topagedef.json)
    log.logger.debug('resultstr: %s' % resultstr)
    #resultstr = topagedef.update_Pagedef('home-alt')
    #log.logger.debug('resultstr: %s' % resultstr)
    '''