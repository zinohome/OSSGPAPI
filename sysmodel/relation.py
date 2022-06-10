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
import distutils
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

class Relation(Collection):
    __collection__ = 'relation'
    _index = [{"type":"hash", "fields":["name"],"unique":True}]
    _key = String(required=True)
    name = String(required=True, allow_none=False)
    frommodel = String(required=True, allow_none=False)
    fromkey = String(required=True, allow_none=False)
    tomodel = String(required=True, allow_none=False)
    tokey = String(required=True, allow_none=False)
    createdate = String(required=True, allow_none=False)

    def has_Relation_Collection(self):
        try:
            govbase = Govbase().db
            if govbase.has_collection(Relation):
                return True
            else:
                return False
        except Exception as exp:
            log.logger.error('Exception at Relation.has_Relation_schema() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()
            return False;

    def existed_Relation(self, document_name):
        try:
            govbase = Govbase().db
            if govbase.has(Relation, document_name):
                return True
            else:
                return False
        except Exception as exp:
            log.logger.error('Exception at Relation.existed_Relation() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()
            return False

    def create_Relation(self, jsonobj):
        try:
            govbase = Govbase().db
            addjson = jsonobj
            if not addjson.__contains__('_key'):
                addjson['_key'] = addjson['name']
            if not govbase.has(Relation, addjson['_key']):
                addobj = Relation._load(addjson)
                govbase.add(addobj)
                return addobj.json
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at Relation.create_Relation() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()


    def get_all_Relation_names(self):
        try:
            count = self.get_Relation_count()
            limit = int(os.getenv('OSSGPAPI_QUERY_LIMIT_UPSET'))
            querycount = count if count <= limit else limit
            govbase = Govbase().db
            records = govbase.query(Relation).limit(querycount).all()
            resultlist = []
            for record in records:
                resultlist.append(record.name)
            return resultlist
        except Exception as exp:
            log.logger.error('Exception at Relation.get_all_Relation_names() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()

    def get_Relation_count(self):
        try:
            govbase = Govbase().db
            return govbase.query(Relation).count()
        except Exception as exp:
            log.logger.error('Exception at Relation.get_Relation_count() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()

    def get_all_Relation(self):
        try:
            count = self.get_Relation_count()
            limit = int(os.getenv('OSSGPAPI_QUERY_LIMIT_UPSET'))
            querycount = count if count <= limit else limit
            govbase = Govbase().db
            records = govbase.query(Relation).limit(querycount).all()
            resultlist = []
            for record in records:
                resultlist.append(record.json)
            return resultlist
        except Exception as exp:
            log.logger.error('Exception at Relation.get_all_Relation() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()

    def get_Relation_bykey(self,keystr):
        try:
            returnjson = {}
            returnjson['count'] = 0
            returnjson['data'] = []
            govbase = Govbase().db
            if govbase.has(Relation,keystr):
                record = govbase.query(Relation).by_key(keystr)
                #returnjson['count'] = 1
                #returnjson['data'].append(record.json)
                returnjson = record.json
            return returnjson
        except Exception as exp:
            log.logger.error('Exception at Relation.get_Relation_bykey() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()

    def get_Relation_byname(self,name):
        try:
            returnjson = {}
            returnjson['count'] = 0
            returnjson['data'] = []
            govbase = Govbase().db
            if govbase.has(Relation,name):
                records = govbase.query(Relation).filter("name=='"+name+"'").all()
                if len(records) >= 1:
                    #returnjson['count'] = 1
                    #returnjson['data'].append(records[0].json)
                    returnjson = records[0].json
            return returnjson
        except Exception as exp:
            log.logger.error('Exception at Relation.get_Relation_bykey() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()

    def update_Relation(self, jsonobj):
        try:
            govbase = Govbase().db
            updatejson = jsonobj
            if not updatejson.__contains__('_key'):
                updatejson['_key'] = updatejson['name']
            if govbase.has(Relation, updatejson['_key']):
                updobj = Relation._load(updatejson)
                govbase.update(updobj)
                return updobj.json
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at Relation.update_Relation() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()

    def delete_Relation(self,keystr):
        try:
            govbase = Govbase().db
            if govbase.has(Relation, keystr):
                return govbase.delete(govbase.query(Relation).by_key(keystr))
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at Relation.delete_Relation() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()

    def query_Relation(self,queryjson):
        try:
            govbase = Govbase().db
            filter = queryjson['filter'] if 'filter' in queryjson else None
            filteror = queryjson['filteror'] if 'filteror' in queryjson else None
            sort = queryjson['sort'] if 'sort' in queryjson else None
            limit = queryjson['limit'] if 'limit' in queryjson else None
            offset = queryjson['offset'] if 'offset' in queryjson else None

            query = govbase.query(Relation)
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
            log.logger.error('Exception at Relation.query_Relation() %s ' % exp)
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
    torelation= Relation(name = 'home-alt',
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
    #log.logger.debug("torelation.has_Relation_Collection(): %s" % torelation.has_Relation_Collection())
    #log.logger.debug("torelation.existed_Relation(): %s" % torelation.existed_Relation())
    log.logger.debug('torelation.json: %s' % torelation.json)
    if not torelation.has_Relation_Collection():
        govbase.create_collection(Relation)
    if not torelation.existed_Relation():
        resultstr = torelation.create_Relation(torelation.json)
        log.logger.debug('resultstr: %s' % resultstr)
    count = torelation.get_Relation_count()
    log.logger.debug('count: %s' % count)
    resultstr = torelation.get_all_Relation()
    log.logger.debug('resultstr: %s' % resultstr)
    resultstr = torelation.get_Relation_bykey('home')
    log.logger.debug('resultstr: %s' % resultstr)
    resultstr = torelation.get_Relation_byname('home-alt')
    log.logger.debug('resultstr: %s' % resultstr)
    torelation.title = '首页二'
    resultstr = torelation.delete_Relation(torelation.json)
    log.logger.debug('resultstr: %s' % resultstr)
    #resultstr = torelation.update_Relation('home-alt')
    #log.logger.debug('resultstr: %s' % resultstr)
    '''