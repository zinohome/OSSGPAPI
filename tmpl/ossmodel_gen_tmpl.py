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

from core import reloadrelation
from core.ossbase import Ossbase
from env.environment import Environment
from sysmodel.graph import Graph
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

    def has{{ defobj['name']|capitalize }}Collection(self):
        try:
            ossbase = Ossbase().db
            if ossbase.has_collection({{ defobj['name']|capitalize }}):
                return True
            else:
                return False
        except Exception as exp:
            log.logger.error('Exception at {{ defobj['name']|capitalize }}.has{{ defobj['name']|capitalize }}() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()
            return False;

    def existed{{ defobj['name']|capitalize }}(self, document_name):
        try:
            ossbase = Ossbase().db
            if ossbase.has({{ defobj['name']|capitalize }}, document_name):
                return True
            else:
                return False
        except Exception as exp:
            log.logger.error('Exception at {{ defobj['name']|capitalize }}.existed{{ defobj['name']|capitalize }}() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()
            return False

    def create{{ defobj['name']|capitalize }}(self, jsonobj):
        try:
            ossbase = Ossbase().db
            addjson = jsonobj
            if not addjson.__contains__('_key'):
                addjson['_key'] = addjson['name']
            if not ossbase.has({{ defobj['name']|capitalize }}, addjson['_key']):
                addobj = {{ defobj['name']|capitalize }}._load(addjson)
                ossbase.add(addobj)
                reloadrelation.create_relation('{{ defobj['name'] }}', addjson['_key'], 'graph', True)
                return addobj.json
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at {{ defobj['name']|capitalize }}.create{{ defobj['name']|capitalize }}() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()


    def getall{{ defobj['name']|capitalize }}names(self):
        try:
            count = self.get{{ defobj['name']|capitalize }}count()
            limit = int(os.getenv('OSSGPAPI_QUERY_LIMIT_UPSET'))
            querycount = count if count <= limit else limit
            ossbase = Ossbase().db
            records = ossbase.query({{ defobj['name']|capitalize }}).limit(querycount).all()
            resultlist = []
            for record in records:
                resultlist.append(record.name)
            return resultlist
        except Exception as exp:
            log.logger.error('Exception at {{ defobj['name']|capitalize }}.getall{{ defobj['name']|capitalize }}names() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()

    def get{{ defobj['name']|capitalize }}count(self):
        try:
            ossbase = Ossbase().db
            return ossbase.query({{ defobj['name']|capitalize }}).count()
        except Exception as exp:
            log.logger.error('Exception at {{ defobj['name']|capitalize }}.get{{ defobj['name']|capitalize }}count() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()

    def getall{{ defobj['name']|capitalize }}(self):
        try:
            count = self.get{{ defobj['name']|capitalize }}count()
            limit = int(os.getenv('OSSGPAPI_QUERY_LIMIT_UPSET'))
            querycount = count if count <= limit else limit
            ossbase = Ossbase().db
            records = ossbase.query({{ defobj['name']|capitalize }}).limit(querycount).all()
            resultlist = []
            for record in records:
                resultlist.append(record.json)
            return resultlist
        except Exception as exp:
            log.logger.error('Exception at {{ defobj['name']|capitalize }}.getall{{ defobj['name']|capitalize }}() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()

    def get{{ defobj['name']|capitalize }}bykey(self,keystr,relation='false'):
        try:
            returnjson = {}
            returnjson['count'] = 0
            returnjson['data'] = []
            ossbase = Ossbase().db
            if ossbase.has({{ defobj['name']|capitalize }},keystr):
                record = ossbase.query({{ defobj['name']|capitalize }}).by_key(keystr)
                #returnjson['count'] = 1
                #returnjson['data'].append(record.json)
                returnjson = record.json
                if not relation.strip().lower() == 'false':
                    sysgraphs = Graph().get_all_Graph()
                    for sysgra in sysgraphs:
                        graph = ossbase.graph(sysgra['name'])
                        results = graph.traverse(start_vertex=record._id,
                                                 direction='outbound',
                                                 strategy='dfs',
                                                 edge_uniqueness='global',
                                                 vertex_uniqueness='global',)
                        graphjson = {sysgra['name']:results}
                        returnjson['relation'] = graphjson
            return returnjson
        except Exception as exp:
            log.logger.error('Exception at {{ defobj['name']|capitalize }}.get{{ defobj['name']|capitalize }}bykey() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()

    def get{{ defobj['name']|capitalize }}byname(self,name,relation='false'):
        try:
            returnjson = {}
            returnjson['count'] = 0
            returnjson['data'] = []
            ossbase = Ossbase().db
            if ossbase.has({{ defobj['name']|capitalize }},name):
                records = ossbase.query({{ defobj['name']|capitalize }}).filter("name=='"+name+"'").all()
                if len(records) >= 1:
                    #returnjson['count'] = 1
                    #returnjson['data'].append(records[0].json)
                    returnjson = records[0].json
                    if not relation.strip().lower() == 'false':
                        sysgraphs = Graph().get_all_Graph()
                        for sysgra in sysgraphs:
                            graph = ossbase.graph(sysgra['name'])
                            results = graph.traverse(start_vertex=records[0]._id,
                                                     direction='outbound',
                                                     strategy='dfs',
                                                     edge_uniqueness='global',
                                                     vertex_uniqueness='global', )
                            graphjson = {sysgra['name']: results}
                            returnjson['relation'] = graphjson
            return returnjson
        except Exception as exp:
            log.logger.error('Exception at {{ defobj['name']|capitalize }}.get{{ defobj['name']|capitalize }}byname() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()

    def update{{ defobj['name']|capitalize }}(self, jsonobj):
        try:
            ossbase = Ossbase().db
            updatejson = jsonobj
            if not updatejson.__contains__('_key'):
                updatejson['_key'] = updatejson['name']
            if ossbase.has({{ defobj['name']|capitalize }}, updatejson['_key']):
                updobj = {{ defobj['name']|capitalize }}._load(updatejson)
                reloadrelation.del_relation('{{ defobj['name'] }}', updatejson['_key'], 'graph', True)
                ossbase.update(updobj)
                reloadrelation.create_relation('{{ defobj['name'] }}', updatejson['_key'], 'graph', True)
                return updobj.json
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at {{ defobj['name']|capitalize }}.update{{ defobj['name']|capitalize }}() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()

    def delete{{ defobj['name']|capitalize }}(self,keystr):
        try:
            ossbase = Ossbase().db
            if ossbase.has({{ defobj['name']|capitalize }}, keystr):
                reloadrelation.del_relation('{{ defobj['name'] }}', keystr, 'graph', True)
                return ossbase.delete(ossbase.query({{ defobj['name']|capitalize }}).by_key(keystr))
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at {{ defobj['name']|capitalize }}.delete{{ defobj['name']|capitalize }}() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()

    def query{{ defobj['name']|capitalize }}(self,queryjson):
        try:
            ossbase = Ossbase().db
            filter = queryjson['filter'] if 'filter' in queryjson else None
            filteror = queryjson['filteror'] if 'filteror' in queryjson else None
            sort = queryjson['sort'] if 'sort' in queryjson else None
            limit = queryjson['limit'] if 'limit' in queryjson else None
            offset = queryjson['offset'] if 'offset' in queryjson else None

            query = ossbase.query({{ defobj['name']|capitalize }})
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
            log.logger.error('Exception at {{ defobj['name']|capitalize }}.query{{ defobj['name']|capitalize }}() %s ' % exp)
            if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
                traceback.print_exc()

    def loadfromjson(self, jsonobj):
        try:
            ossbase = Ossbase().db
            if not jsonobj.__contains__('_key'):
                jsonobj['_key'] = jsonobj['name']
            if ossbase.has({{ defobj['name']|capitalize }}, jsonobj['_key']):
                obj = ossbase.query({{defobj['name'] | capitalize}}).by_key(jsonobj['_key'])
                return obj
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at Student.loadfromjson() %s ' % exp)
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
    ossbase = Ossbase().db
