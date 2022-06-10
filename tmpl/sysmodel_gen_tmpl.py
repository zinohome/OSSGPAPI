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
from marshmallow.fields import *

from core.govbase import Govbase
from env.environment import Environment
from util import log

'''logging'''
env = Environment()
log = log.Logger(level=os.getenv('OSSGPAPI_APP_LOG_LEVEL'))

class {{ defobj['name']|capitalize }}(Collection):
    {% for propkey, propvalue  in defobj['coldef'].items() %}
    {% if propkey == '__collection__' %}
    {{ propkey }} = '{{ propvalue }}'
    {% else %}
    {{ propkey }} = {{ propvalue }}
    {% endif %}
    {% endfor %}

    def has_{{ defobj['name']|capitalize }}_Collection(self):
        try:
            govbase = Govbase().db
            if govbase.has_collection({{ defobj['name']|capitalize }}):
                return True
            else:
                return False
        except Exception as exp:
            log.logger.error('Exception at {{ defobj['name']|capitalize }}.has_{{ defobj['name']|capitalize }}_schema() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()
            return False;

    def existed_{{ defobj['name']|capitalize }}(self, document_name):
        try:
            govbase = Govbase().db
            if govbase.has({{ defobj['name']|capitalize }}, document_name):
                return True
            else:
                return False
        except Exception as exp:
            log.logger.error('Exception at {{ defobj['name']|capitalize }}.existed_{{ defobj['name']|capitalize }}() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()
            return False

    def create_{{ defobj['name']|capitalize }}(self, jsonobj):
        try:
            govbase = Govbase().db
            addjson = jsonobj
            if not addjson.__contains__('_key'):
                addjson['_key'] = addjson['name']
            if not govbase.has({{ defobj['name']|capitalize }}, addjson['_key']):
                addobj = {{ defobj['name']|capitalize }}._load(addjson)
                govbase.add(addobj)
                return addobj.json
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at {{ defobj['name']|capitalize }}.create_{{ defobj['name']|capitalize }}() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()


    def get_all_{{ defobj['name']|capitalize }}_names(self):
        try:
            count = self.get_{{ defobj['name']|capitalize }}_count()
            limit = int(os.getenv('OSSGPAPI_QUERY_LIMIT_UPSET'))
            querycount = count if count <= limit else limit
            govbase = Govbase().db
            records = govbase.query({{ defobj['name']|capitalize }}).limit(querycount).all()
            resultlist = []
            for record in records:
                resultlist.append(record.name)
            return resultlist
        except Exception as exp:
            log.logger.error('Exception at {{ defobj['name']|capitalize }}.get_all_{{ defobj['name']|capitalize }}_names() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()

    def get_{{ defobj['name']|capitalize }}_count(self):
        try:
            govbase = Govbase().db
            return govbase.query({{ defobj['name']|capitalize }}).count()
        except Exception as exp:
            log.logger.error('Exception at {{ defobj['name']|capitalize }}.get_{{ defobj['name']|capitalize }}_count() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()

    def get_all_{{ defobj['name']|capitalize }}(self):
        try:
            count = self.get_{{ defobj['name']|capitalize }}_count()
            limit = int(os.getenv('OSSGPAPI_QUERY_LIMIT_UPSET'))
            querycount = count if count <= limit else limit
            govbase = Govbase().db
            records = govbase.query({{ defobj['name']|capitalize }}).limit(querycount).all()
            resultlist = []
            for record in records:
                resultlist.append(record.json)
            return resultlist
        except Exception as exp:
            log.logger.error('Exception at {{ defobj['name']|capitalize }}.get_all_{{ defobj['name']|capitalize }}() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()

    def get_{{ defobj['name']|capitalize }}_bykey(self,keystr):
        try:
            returnjson = {}
            returnjson['count'] = 0
            returnjson['data'] = []
            govbase = Govbase().db
            if govbase.has({{ defobj['name']|capitalize }},keystr):
                record = govbase.query({{ defobj['name']|capitalize }}).by_key(keystr)
                #returnjson['count'] = 1
                #returnjson['data'].append(record.json)
                returnjson = record.json
            return returnjson
        except Exception as exp:
            log.logger.error('Exception at {{ defobj['name']|capitalize }}.get_{{ defobj['name']|capitalize }}_bykey() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()

    def get_{{ defobj['name']|capitalize }}_byname(self,name):
        try:
            returnjson = {}
            returnjson['count'] = 0
            returnjson['data'] = []
            govbase = Govbase().db
            if govbase.has({{ defobj['name']|capitalize }},name):
                records = govbase.query({{ defobj['name']|capitalize }}).filter("name=='"+name+"'").all()
                if len(records) >= 1:
                    #returnjson['count'] = 1
                    #returnjson['data'].append(records[0].json)
                    returnjson = records[0].json
            return returnjson
        except Exception as exp:
            log.logger.error('Exception at {{ defobj['name']|capitalize }}.get_{{ defobj['name']|capitalize }}_bykey() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()

    def update_{{ defobj['name']|capitalize }}(self, jsonobj):
        try:
            govbase = Govbase().db
            updatejson = jsonobj
            if not updatejson.__contains__('_key'):
                updatejson['_key'] = updatejson['name']
            if govbase.has({{ defobj['name']|capitalize }}, updatejson['_key']):
                updobj = {{ defobj['name']|capitalize }}._load(updatejson)
                govbase.update(updobj)
                return updobj.json
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at {{ defobj['name']|capitalize }}.update_{{ defobj['name']|capitalize }}() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()

    def delete_{{ defobj['name']|capitalize }}(self,keystr):
        try:
            govbase = Govbase().db
            if govbase.has({{ defobj['name']|capitalize }}, keystr):
                return govbase.delete(govbase.query({{ defobj['name']|capitalize }}).by_key(keystr))
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at {{ defobj['name']|capitalize }}.delete_{{ defobj['name']|capitalize }}() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()

    def query_{{ defobj['name']|capitalize }}(self,queryjson):
        try:
            govbase = Govbase().db
            filter = queryjson['filter'] if 'filter' in queryjson else None
            filteror = queryjson['filteror'] if 'filteror' in queryjson else None
            sort = queryjson['sort'] if 'sort' in queryjson else None
            limit = queryjson['limit'] if 'limit' in queryjson else None
            offset = queryjson['offset'] if 'offset' in queryjson else None

            query = govbase.query({{ defobj['name']|capitalize }})
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
            log.logger.error('Exception at {{ defobj['name']|capitalize }}.query_{{ defobj['name']|capitalize }}() %s ' % exp)
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
    to{{ defobj['name'] }}= {{ defobj['name']|capitalize }}(name = 'home-alt',
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
    #log.logger.debug("to{{ defobj['name'] }}.has_{{ defobj['name']|capitalize }}_Collection(): %s" % to{{ defobj['name'] }}.has_{{ defobj['name']|capitalize }}_Collection())
    #log.logger.debug("to{{ defobj['name'] }}.existed_{{ defobj['name']|capitalize }}(): %s" % to{{ defobj['name'] }}.existed_{{ defobj['name']|capitalize }}())
    log.logger.debug('to{{ defobj['name'] }}.json: %s' % to{{ defobj['name'] }}.json)
    if not to{{ defobj['name'] }}.has_{{ defobj['name']|capitalize }}_Collection():
        govbase.create_collection({{ defobj['name']|capitalize }})
    if not to{{ defobj['name'] }}.existed_{{ defobj['name']|capitalize }}():
        resultstr = to{{ defobj['name'] }}.create_{{ defobj['name']|capitalize }}(to{{ defobj['name'] }}.json)
        log.logger.debug('resultstr: %s' % resultstr)
    count = to{{ defobj['name'] }}.get_{{ defobj['name']|capitalize }}_count()
    log.logger.debug('count: %s' % count)
    resultstr = to{{ defobj['name'] }}.get_all_{{ defobj['name']|capitalize }}()
    log.logger.debug('resultstr: %s' % resultstr)
    resultstr = to{{ defobj['name'] }}.get_{{ defobj['name']|capitalize }}_bykey('home')
    log.logger.debug('resultstr: %s' % resultstr)
    resultstr = to{{ defobj['name'] }}.get_{{ defobj['name']|capitalize }}_byname('home-alt')
    log.logger.debug('resultstr: %s' % resultstr)
    to{{ defobj['name'] }}.title = '首页二'
    resultstr = to{{ defobj['name'] }}.delete_{{ defobj['name']|capitalize }}(to{{ defobj['name'] }}.json)
    log.logger.debug('resultstr: %s' % resultstr)
    #resultstr = to{{ defobj['name'] }}.update_{{ defobj['name']|capitalize }}('home-alt')
    #log.logger.debug('resultstr: %s' % resultstr)
    '''
