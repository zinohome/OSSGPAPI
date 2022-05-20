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

from core.ossbase import Ossbase
from env.environment import Environment
from util import log

'''logging'''
env = Environment()
log = log.Logger(level=os.getenv('OSSGPAPI_APP_LOG_LEVEL'))

class Risk(Collection):
    __collection__ = 'risk'
    _index = [{'type':'hash', 'fields':['name'], 'unique':True}]
    _key = String(required=True)
    name = String(required=True, allow_none=False)
    title = String(required=True, allow_none=False)
    type = String(required=True, allow_none=False)
    software = String(required=True, allow_none=False)
    platform = String(required=True, allow_none=False)
    level = String(required=True, allow_none=False)
    source = String(required=True, allow_none=False)
    link = String(required=True, allow_none=False)
    content = String(required=True, allow_none=False)
    solution = String(required=True, allow_none=False)
    createdate = Date()

    def hasRiskCollection(self):
        try:
            ossbase = Ossbase().db
            if ossbase.has_collection(Risk):
                return True
            else:
                return False
        except Exception as exp:
            log.logger.error('Exception at Risk.hasRisk() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()
            return False;

    def existedRisk(self, document_name):
        try:
            ossbase = Ossbase().db
            if ossbase.has(Risk, document_name):
                return True
            else:
                return False
        except Exception as exp:
            log.logger.error('Exception at Risk.existedRisk() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()
            return False

    def createRisk(self, jsonobj):
        try:
            ossbase = Ossbase().db
            addjson = jsonobj
            if not addjson.__contains__('_key'):
                addjson['_key'] = addjson['name']
            if not ossbase.has(Risk, addjson['_key']):
                addobj = Risk._load(addjson)
                ossbase.add(addobj)
                return addobj.json
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at Risk.createRisk() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()


    def getallRisknames(self):
        try:
            count = self.getRiskcount()
            limit = int(os.getenv('OSSGPAPI_QUERY_LIMIT_UPSET'))
            querycount = count if count <= limit else limit
            ossbase = Ossbase().db
            records = ossbase.query(Risk).limit(querycount).all()
            resultlist = []
            for record in records:
                resultlist.append(record.name)
            return resultlist
        except Exception as exp:
            log.logger.error('Exception at Risk.getallRisknames() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def getRiskcount(self):
        try:
            ossbase = Ossbase().db
            return ossbase.query(Risk).count()
        except Exception as exp:
            log.logger.error('Exception at Risk.getRiskcount() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def getallRisk(self):
        try:
            count = self.getRiskcount()
            limit = int(os.getenv('OSSGPAPI_QUERY_LIMIT_UPSET'))
            querycount = count if count <= limit else limit
            ossbase = Ossbase().db
            records = ossbase.query(Risk).limit(querycount).all()
            resultlist = []
            for record in records:
                resultlist.append(record.json)
            return resultlist
        except Exception as exp:
            log.logger.error('Exception at Risk.getallRisk() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def getRiskbykey(self,keystr):
        try:
            returnjson = {}
            returnjson['count'] = 0
            returnjson['data'] = []
            ossbase = Ossbase().db
            if ossbase.has(Risk,keystr):
                record = ossbase.query(Risk).by_key(keystr)
                #returnjson['count'] = 1
                #returnjson['data'].append(record.json)
                returnjson = record.json
            return returnjson
        except Exception as exp:
            log.logger.error('Exception at Risk.getRiskbykey() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def getRiskbyname(self,name):
        try:
            returnjson = {}
            returnjson['count'] = 0
            returnjson['data'] = []
            ossbase = Ossbase().db
            if ossbase.has(Risk,name):
                records = ossbase.query(Risk).filter("name=='"+name+"'").all()
                if len(records) >= 1:
                    #returnjson['count'] = 1
                    #returnjson['data'].append(records[0].json)
                    returnjson = records[0].json
            return returnjson
        except Exception as exp:
            log.logger.error('Exception at Risk.getRiskbyname() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def updateRisk(self, jsonobj):
        try:
            ossbase = Ossbase().db
            updatejson = jsonobj
            if not updatejson.__contains__('_key'):
                updatejson['_key'] = updatejson['name']
            if ossbase.has(Risk, updatejson['_key']):
                updobj = Risk._load(updatejson)
                ossbase.update(updobj)
                return updobj.json
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at Risk.updateRisk() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def deleteRisk(self,keystr):
        try:
            ossbase = Ossbase().db
            if ossbase.has(Risk, keystr):
                return ossbase.delete(ossbase.query(Risk).by_key(keystr))
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at Risk.deleteRisk() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def queryRisk(self,queryjson):
        try:
            ossbase = Ossbase().db
            filter = queryjson['filter'] if 'filter' in queryjson else None
            filteror = queryjson['filteror'] if 'filteror' in queryjson else None
            sort = queryjson['sort'] if 'sort' in queryjson else None
            limit = queryjson['limit'] if 'limit' in queryjson else None
            offset = queryjson['offset'] if 'offset' in queryjson else None

            query = ossbase.query(Risk)
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
            log.logger.error('Exception at Risk.queryRisk() %s ' % exp)
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
    ossbase = Ossbase().db
    torisk = Risk(name='CVE-2022-29885',
                  title='CVE-2022-29885',
                  type='CVE',
                  software='Apache Tomcat',
                  platform='Linux,Windows,Mac,AIX',
                  level='High',
                  source='CVE',
                  link='https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-29885',
                  content='The documentation of Apache Tomcat 10.1.0-M1 to 10.1.0-M14, 10.0.0-M1 to 10.0.20, 9.0.13 to 9.0.62 and 8.5.38 to 8.5.78 for the EncryptInterceptor incorrectly stated it enabled Tomcat clustering to run over an untrusted network. This was not correct. While the EncryptInterceptor does provide confidentiality and integrity protection, it does not protect against all risks associated with running over any untrusted network, particularly DoS risks.',
                  solution='None',
                  createdate='2022-04-28')
    log.logger.debug(torisk.hasRiskCollection())
    tljson = torisk.json
    log.logger.debug(tljson)
    log.logger.debug(json.dumps(tljson))
    log.logger.debug("================================ create ================================")
    log.logger.debug(torisk.createRisk(tljson))
    log.logger.debug("================================ get_all_Risk_names ================================")
    log.logger.debug(torisk.getallRisknames())