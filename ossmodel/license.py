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
from marshmallow.fields import Integer, Bool
from core.ossbase import Ossbase
from env.environment import Environment
from util import log

'''logging'''
env = Environment()
log = log.Logger(level=os.getenv('OSSGPAPI_APP_LOG_LEVEL'))

class License(Collection):
    __collection__ = 'license'
    _index = [{'type':'hash', 'fields':['name'], 'unique':True}]
    _key = String(required=True)
    name = String(required=True, allow_none=False)
    title = String(required=True, allow_none=False)
    version = String(required=True, allow_none=False)
    homepage = String(required=False, allow_none=True)
    introduce = String(required=False, allow_none=True)
    content = String(required=False, allow_none=True)
    contentCN = String(required=False, allow_none=True)
    licenseinclude = Bool(required=False, allow_none=True)
    sourceinclude = Bool(required=False, allow_none=True)
    linked = Bool(required=False, allow_none=True)
    statuschange = Bool(required=False, allow_none=True)
    businessuse = Bool(required=False, allow_none=True)
    distribution = Bool(required=False, allow_none=True)
    modification = Bool(required=False, allow_none=True)
    patentauth = Bool(required=False, allow_none=True)
    privateuse = Bool(required=False, allow_none=True)
    authresell = Bool(required=False, allow_none=True)
    unsecuredliability = Bool(required=False, allow_none=True)
    notrademark = Bool(required=False, allow_none=True)

    def hasLicenseCollection(self):
        try:
            ossbase = Ossbase().db
            if ossbase.has_collection(License):
                return True
            else:
                return False
        except Exception as exp:
            log.logger.error('Exception at License.hasLicenseCollection() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()
            return False;

    def existedLicense(self, document_name):
        try:
            ossbase = Ossbase().db
            if ossbase.has(License, document_name):
                return True
            else:
                return False
        except Exception as exp:
            log.logger.error('Exception at License.existedLicense() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()
            return False

    def createLicense(self, jsonobj):
        try:
            ossbase = Ossbase().db
            addjson = jsonobj
            if not addjson.__contains__('_key'):
                addjson['_key'] = addjson['name']
            if not ossbase.has(License, addjson['_key']):
                addobj = License._load(addjson)
                ossbase.add(addobj)
                return addobj.json
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at License.createLicense() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()


    def getallLicensenames(self):
        try:
            count = self.getLicensecount()
            limit = int(os.getenv('OSSGPADMIN_API_QUERY_LIMIT_UPSET'))
            querycount = count if count <= limit else limit
            ossbase = Ossbase().db
            records = ossbase.query(License).limit(querycount).all()
            resultlist = []
            for record in records:
                resultlist.append(record.name)
            return resultlist
        except Exception as exp:
            log.logger.error('Exception at License.getallLicensenames() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def getLicensecount(self):
        try:
            ossbase = Ossbase().db
            return ossbase.query(License).count()
        except Exception as exp:
            log.logger.error('Exception at License.getLicensecount() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def getallLicense(self):
        try:
            count = self.getLicensecount()
            limit = int(os.getenv('OSSGPADMIN_API_QUERY_LIMIT_UPSET'))
            querycount = count if count <= limit else limit
            ossbase = Ossbase().db
            records = ossbase.query(License).limit(querycount).all()
            resultlist = []
            for record in records:
                resultlist.append(record.json)
            return resultlist
        except Exception as exp:
            log.logger.error('Exception at License.getallLicense() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def getLicensebykey(self,keystr):
        try:
            returnjson = {}
            returnjson['count'] = 0
            returnjson['data'] = []
            ossbase = Ossbase().db
            if ossbase.has(License,keystr):
                record = ossbase.query(License).by_key(keystr)
                #returnjson['count'] = 1
                #returnjson['data'].append(record.json)
                returnjson = record.json
            return returnjson
        except Exception as exp:
            log.logger.error('Exception at License.getLicensebykey() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def getLicensebyname(self,name):
        try:
            returnjson = {}
            returnjson['count'] = 0
            returnjson['data'] = []
            ossbase = Ossbase().db
            if ossbase.has(License,name):
                records = ossbase.query(License).filter("name=='"+name+"'").all()
                if len(records) >= 1:
                    #returnjson['count'] = 1
                    #returnjson['data'].append(records[0].json)
                    returnjson = records[0].json
            return returnjson
        except Exception as exp:
            log.logger.error('Exception at License.getLicensebyname() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def updateLicense(self, jsonobj):
        try:
            ossbase = Ossbase().db
            updatejson = jsonobj
            if not updatejson.__contains__('_key'):
                updatejson['_key'] = updatejson['name']
            if ossbase.has(License, updatejson['_key']):
                updobj = License._load(updatejson)
                ossbase.update(updobj)
                return updobj.json
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at License.updateLicense() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def deleteLicense(self,keystr):
        try:
            ossbase = Ossbase().db
            if ossbase.has(License, keystr):
                return ossbase.delete(ossbase.query(License).by_key(keystr))
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at License.deleteLicense() %s ' % exp)
            if os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL"):
                traceback.print_exc()

    def queryLicense(self,queryjson):
        try:
            ossbase = Ossbase().db
            filter = queryjson['filter'] if 'filter' in queryjson else None
            filteror = queryjson['filteror'] if 'filteror' in queryjson else None
            sort = queryjson['sort'] if 'sort' in queryjson else None
            limit = queryjson['limit'] if 'limit' in queryjson else None
            offset = queryjson['offset'] if 'offset' in queryjson else None

            query = ossbase.query(License)
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
            log.logger.error('Exception at License.queryLicense() %s ' % exp)
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
    tolicense = License(name = 'ApacheLicense-v2',
                        title = 'Apache许可证',
                        version = 'v2',
                        homepage = '',
                        introduce = 'Apache许可证',
                        content = 'Apache许可证',
                        contentCN = 'Apache许可证',
                        licenseinclude = True,
                        sourceinclude = False,
                        linked = False,
                        statuschange = True,
                        businessuse = True,
                        distribution = True,
                        modification = True,
                        patentauth = True,
                        privateuse = True,
                        authresell = True,
                        unsecuredliability = True,
                        notrademark = True)
    log.logger.debug(tolicense.hasLicenseCollection())
    tljson = tolicense.json
    log.logger.debug(tljson)
    log.logger.debug(json.dumps(tljson))
    log.logger.debug("================================ create ================================")
    log.logger.debug(tolicense.createLicense(tljson))
    log.logger.debug("================================ get_all_License_names ================================")
    log.logger.debug(tolicense.getallLicensenames())


