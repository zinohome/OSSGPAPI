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
from core.ossbase import Ossbase
from env.environment import Environment
from util import log

'''logging'''
env = Environment()
log = log.Logger(level=os.getenv('OSSGPAPI_APP_LOG_LEVEL'))

class Adminnav(Collection):
    __collection__ = 'adminnav'
    _index = [{'type':'hash', 'fields':['name'], 'unique':True}]
    _key = String(required=True)
    name = String(required=True, allow_none=False)
    title = String(required=True, allow_none=False)
    level = Integer(required=True, allow_none=False)
    order = Integer(required=True, allow_none=False)
    segment = String(required=False, allow_none=True)
    liclass = String(required=False, allow_none=True)
    hrefclass = String(required=False, allow_none=True)
    navclass = String(required=True, allow_none=False)
    href = String(required=False, allow_none=True)
    icon = String(required=False, allow_none=True)
    createdate = Date()

    def has_Adminnav_Collection(self):
        try:
            govbase = Govbase().db
            if govbase.has_collection(self.__collection__):
                return True
            else:
                return False
        except Exception as exp:
            log.logger.error('Exception at Adminnav.has_Adminnav_schema() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()
            return False;

    def existed_Adminnav(self):
        try:
            govbase = Govbase().db
            if govbase.has(Adminnav,self.name):
                return True
            else:
                return False
        except Exception as exp:
            log.logger.error('Exception at Adminnav.existed_Adminnav() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()
            return False

    def create_Adminnav(self, jsonobj):
        try:
            govbase = Govbase().db
            addjson = jsonobj
            if not addjson.__contains__('_key'):
                addjson['_key'] = addjson['name']
            if not govbase.has(Adminnav, addjson['_key']):
                addobj = Adminnav._load(addjson)
                govbase.add(addobj)
                return addobj.json
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at Adminnav.create_Adminnav() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def get_Adminnav_count(self):
        try:
            govbase = Govbase().db
            return govbase.query(Adminnav).count()
        except Exception as exp:
            log.logger.error('Exception at Adminnav.get_Adminnav_count() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def get_all_Adminnav(self):
        try:
            count = self.get_Adminnav_count()
            limit = int(os.getenv('OSSGPAPI_QUERY_LIMIT_UPSET'))
            querycount = count if count <= limit else limit
            govbase = Govbase().db
            records = govbase.query(Adminnav).limit(querycount).all()
            resultlist = []
            for record in records:
                resultlist.append(record.json)
            return resultlist
        except Exception as exp:
            log.logger.error('Exception at Adminnav.get_all_Adminnav() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def get_Adminnav_bykey(self,keystr):
        try:
            returnjson = {}
            returnjson['count'] = 0
            returnjson['data'] = []
            govbase = Govbase().db
            if govbase.has(Adminnav,keystr):
                record = govbase.query(Adminnav).by_key(keystr)
                returnjson['count'] = 1
                returnjson['data'].append(record.json)
            return returnjson
        except Exception as exp:
            log.logger.error('Exception at Adminnav.get_Adminnav_bykey() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def get_Adminnav_byname(self,name):
        try:
            returnjson = {}
            returnjson['count'] = 0
            returnjson['data'] = []
            govbase = Govbase().db
            if govbase.has(Adminnav,name):
                records = govbase.query(Adminnav).filter("name=='"+name+"'").all()
                if len(records) >= 1:
                    returnjson['count'] = 1
                    returnjson['data'].append(records[0].json)
            return returnjson
        except Exception as exp:
            log.logger.error('Exception at Adminnav.get_Adminnav_bykey() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def update_Adminnav(self, jsonobj):
        try:
            govbase = Govbase().db
            updatejson = jsonobj
            if not updatejson.__contains__('_key'):
                updatejson['_key'] = updatejson['name']
            if govbase.has(Adminnav, updatejson['_key']):
                updobj = Adminnav._load(updatejson)
                govbase.update(updobj)
                return updobj.json
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at Adminnav.update_Adminnav() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def delete_Adminnav(self,keystr):
        try:
            govbase = Govbase().db
            if govbase.has(Adminnav, keystr):
                return govbase.delete(govbase.query(Adminnav).by_key(keystr))
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at Adminnav.delete_Adminnav() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def query_Adminnav(self,queryjson):
        try:
            govbase = Govbase().db
            filter = queryjson['filter'] if 'filter' in queryjson else None
            filteror = queryjson['filteror'] if 'filteror' in queryjson else None
            sort = queryjson['sort'] if 'sort' in queryjson else None
            limit = queryjson['limit'] if 'limit' in queryjson else None
            offset = queryjson['offset'] if 'offset' in queryjson else None

            query = govbase.query(Adminnav)
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
            log.logger.error('Exception at Adminnav.query_Adminnav() %s ' % exp)
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
    adminav = Adminnav(name = 'home-alt',
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
    #log.logger.debug("adminav.has_Adminnav_Collection(): %s" % adminav.has_Adminnav_Collection())
    #log.logger.debug("adminav.existed_Adminnav(): %s" % adminav.existed_Adminnav())
    log.logger.debug('adminav.json: %s' % adminav.json)
    if not adminav.has_Adminnav_Collection():
        govbase.create_collection(Adminnav)
    if not adminav.existed_Adminnav():
        resultstr = adminav.create_Adminnav(adminav.json)
        log.logger.debug('resultstr: %s' % resultstr)
    count = adminav.get_Adminnav_count()
    log.logger.debug('count: %s' % count)
    resultstr = adminav.get_all_Adminnav()
    log.logger.debug('resultstr: %s' % resultstr)
    resultstr = adminav.get_Adminnav_bykey('home')
    log.logger.debug('resultstr: %s' % resultstr)
    resultstr = adminav.get_Adminnav_byname('home-alt')
    log.logger.debug('resultstr: %s' % resultstr)
    adminav.title = '首页二'
    resultstr = adminav.delete_Adminnav(adminav.json)
    log.logger.debug('resultstr: %s' % resultstr)
    #resultstr = adminav.update_Adminnav('home-alt')
    #log.logger.debug('resultstr: %s' % resultstr)


