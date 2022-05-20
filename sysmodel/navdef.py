#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2022 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2022
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: OSSGPAPI
import distutils
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

class Navdef(Collection):
    __collection__ = 'navdef'
    _index = [{'type':'hash', 'fields':['name'], 'unique':True}]
    _key = String(required=True)
    name = String(required=True, allow_none=False)
    title = String(required=True, allow_none=False)
    level = Integer(required=True, allow_none=False)
    order = String(required=True, allow_none=False)
    segment = String(required=False, allow_none=True)
    navclass = String(required=True, allow_none=False)
    href = String(required=False, allow_none=True)
    icon = String(required=False, allow_none=True)
    createdate = Date()

    def has_Navdef_Collection(self):
        try:
            govbase = Govbase().db
            if govbase.has_collection(Navdef):
                return True
            else:
                return False
        except Exception as exp:
            log.logger.error('Exception at Navdef.has_Navdef_schema() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()
            return False;

    def existed_Navdef(self, document_name):
        try:
            govbase = Govbase().db
            if govbase.has(Navdef, document_name):
                return True
            else:
                return False
        except Exception as exp:
            log.logger.error('Exception at Navdef.existed_Navdef() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()
            return False

    def create_Navdef(self, jsonobj):
        try:
            govbase = Govbase().db
            addjson = jsonobj
            if not addjson.__contains__('_key'):
                addjson['_key'] = addjson['name']
            if not govbase.has(Navdef, addjson['_key']):
                addobj = Navdef._load(addjson)
                govbase.add(addobj)
                return addobj.json
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at Navdef.create_Navdef() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()


    def get_all_Navdef_names(self):
        try:
            count = self.get_Navdef_count()
            limit = int(os.getenv('OSSGPAPI_QUERY_LIMIT_UPSET'))
            querycount = count if count <= limit else limit
            govbase = Govbase().db
            records = govbase.query(Navdef).limit(querycount).all()
            resultlist = []
            for record in records:
                resultlist.append(record.name)
            return resultlist
        except Exception as exp:
            log.logger.error('Exception at Navdef.get_all_Navdef_names() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()

    def get_Navdef_count(self):
        try:
            govbase = Govbase().db
            return govbase.query(Navdef).count()
        except Exception as exp:
            log.logger.error('Exception at Navdef.get_Navdef_count() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()

    def get_all_Navdef(self):
        try:
            count = self.get_Navdef_count()
            limit = int(os.getenv('OSSGPAPI_QUERY_LIMIT_UPSET'))
            querycount = count if count <= limit else limit
            govbase = Govbase().db
            records = govbase.query(Navdef).limit(querycount).all()
            resultlist = []
            for record in records:
                resultlist.append(record.json)
            return resultlist
        except Exception as exp:
            log.logger.error('Exception at Navdef.get_all_Navdef() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()

    def get_Navdef_bykey(self,keystr):
        try:
            returnjson = {}
            returnjson['count'] = 0
            returnjson['data'] = []
            govbase = Govbase().db
            if govbase.has(Navdef,keystr):
                record = govbase.query(Navdef).by_key(keystr)
                #returnjson['count'] = 1
                #returnjson['data'].append(record.json)
                returnjson = record.json
            return returnjson
        except Exception as exp:
            log.logger.error('Exception at Navdef.get_Navdef_bykey() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()

    def get_Navdef_byname(self,name):
        try:
            returnjson = {}
            returnjson['count'] = 0
            returnjson['data'] = []
            govbase = Govbase().db
            if govbase.has(Navdef,name):
                records = govbase.query(Navdef).filter("name=='"+name+"'").all()
                if len(records) >= 1:
                    #returnjson['count'] = 1
                    #returnjson['data'].append(records[0].json)
                    returnjson = records[0].json
            return returnjson
        except Exception as exp:
            log.logger.error('Exception at Navdef.get_Navdef_bykey() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()

    def update_Navdef(self, jsonobj):
        try:
            govbase = Govbase().db
            updatejson = jsonobj
            if not updatejson.__contains__('_key'):
                updatejson['_key'] = updatejson['name']
            if govbase.has(Navdef, updatejson['_key']):
                updobj = Navdef._load(updatejson)
                govbase.update(updobj)
                return updobj.json
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at Navdef.update_Navdef() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()

    def delete_Navdef(self,keystr):
        try:
            govbase = Govbase().db
            if govbase.has(Navdef, keystr):
                return govbase.delete(govbase.query(Navdef).by_key(keystr))
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at Navdef.delete_Navdef() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()

    def query_Navdef(self,queryjson):
        try:
            govbase = Govbase().db
            filter = queryjson['filter'] if 'filter' in queryjson else None
            filteror = queryjson['filteror'] if 'filteror' in queryjson else None
            sort = queryjson['sort'] if 'sort' in queryjson else None
            limit = queryjson['limit'] if 'limit' in queryjson else None
            offset = queryjson['offset'] if 'offset' in queryjson else None

            query = govbase.query(Navdef)
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
            log.logger.error('Exception at Navdef.query_Navdef() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
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
    tonavdef= Navdef(name = 'home-alt',
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
    #log.logger.debug("tonavdef.has_Navdef_Collection(): %s" % tonavdef.has_Navdef_Collection())
    #log.logger.debug("tonavdef.existed_Navdef(): %s" % tonavdef.existed_Navdef())
    log.logger.debug('tonavdef.json: %s' % tonavdef.json)
    if not tonavdef.has_Navdef_Collection():
        govbase.create_collection(Navdef)
    if not tonavdef.existed_Navdef():
        resultstr = tonavdef.create_Navdef(tonavdef.json)
        log.logger.debug('resultstr: %s' % resultstr)
    count = tonavdef.get_Navdef_count()
    log.logger.debug('count: %s' % count)
    resultstr = tonavdef.get_all_Navdef()
    log.logger.debug('resultstr: %s' % resultstr)
    resultstr = tonavdef.get_Navdef_bykey('home')
    log.logger.debug('resultstr: %s' % resultstr)
    resultstr = tonavdef.get_Navdef_byname('home-alt')
    log.logger.debug('resultstr: %s' % resultstr)
    tonavdef.title = '首页二'
    resultstr = tonavdef.delete_Navdef(tonavdef.json)
    log.logger.debug('resultstr: %s' % resultstr)
    #resultstr = tonavdef.update_Navdef('home-alt')
    #log.logger.debug('resultstr: %s' % resultstr)
    '''