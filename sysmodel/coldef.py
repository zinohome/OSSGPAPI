#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2022 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2022
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: OSSGPAPI

import importlib
import traceback

import simplejson as json
import os
from datetime import date

from arango_orm import Collection
from arango_orm.fields import String, Date
from jinja2 import FileSystemLoader

from core.govbase import Govbase
from core.ossbase import Ossbase
from env.environment import Environment
from jinja2 import Environment as genenv
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

    def has_Coldef_schema(self, coldef_name):
        try:
            govbase = Govbase().db
            if govbase.has(Coldef, coldef_name):
                return True
            else:
                return False
        except Exception as exp:
            log.logger.error('Exception at coldef.has_Coldef_schema() %s ' % exp)
            if str(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")).strip().lower() == 'true':
                traceback.print_exc()
            return False;

    def existed_Coldef(self, collection_name):
        try:
            ossbase = Ossbase().db
            if ossbase.has_collection(collection_name):
                return True
            else:
                return False
        except Exception as exp:
            log.logger.error('Exception at coldef.existed_Coldef() %s ' % exp)
            if str(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")).strip().lower() == 'true':
                traceback.print_exc()
            return False

    def get_Coldef_count(self):
        try:
            govbase = Govbase().db
            return govbase.query(Coldef).count()
        except Exception as exp:
            log.logger.error('Exception at Coldef.get_Coldef_count() %s ' % exp)
            if str(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")).strip().lower() == 'true':
                traceback.print_exc()

    def get_all_Coldef(self):
        try:
            count = self.get_Coldef_count()
            limit = int(os.getenv('OSSGPAPI_QUERY_LIMIT_UPSET'))
            querycount = count if count <= limit else limit
            govbase = Govbase().db
            records = govbase.query(Coldef).limit(querycount).all()
            resultlist = []
            for record in records:
                resultlist.append(record.json)
            return resultlist
        except Exception as exp:
            log.logger.error('Exception at Coldef.get_all_Coldef() %s ' % exp)
            if str(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")).strip().lower() == 'true':
                traceback.print_exc()

    def get_all_Coldef_names(self):
        try:
            count = self.get_Coldef_count()
            limit = int(os.getenv('OSSGPAPI_QUERY_LIMIT_UPSET'))
            querycount = count if count <= limit else limit
            govbase = Govbase().db
            records = govbase.query(Coldef).limit(querycount).all()
            resultlist = []
            for record in records:
                resultlist.append(record.name)
            return resultlist
        except Exception as exp:
            log.logger.error('Exception at Coldef.get_all_Coldef_names() %s ' % exp)
            if str(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")).strip().lower() == 'true':
                traceback.print_exc()

    def create_Coldef(self, jsonobj):
        try:
            govbase = Govbase().db
            addjson = jsonobj
            if not addjson.__contains__('_key'):
                addjson['_key'] = addjson['name']
            if not govbase.has(Coldef, addjson['_key']):
                addobj = Coldef._load(addjson)
                govbase.add(addobj)
                log.logger.debug('===================== create coldef [ %s ] =====================' % addobj.name)
                self.genmodel(addobj.json)
                if self.has_Coldef_schema(addobj.name) and not self.existed_Coldef(addobj.name):
                    log.logger.debug('Create Collection %s in OSSBase' % addobj.name)
                    ossmodelcls = importlib.import_module('ossmodel.' + addobj.name.lower())
                    ossmodel = getattr(ossmodelcls, addobj.name.capitalize())()
                    ossbase = Ossbase().db
                    ossbase.create_collection(ossmodel)
                return addobj.json
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at Coldef.create_Coldef() %s ' % exp)
            if str(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")).strip().lower() == 'true':
                traceback.print_exc()

    def get_Coldef_bykey(self,keystr):
        try:
            returnjson = {}
            returnjson['count'] = 0
            returnjson['data'] = []
            govbase = Govbase().db
            if govbase.has(Coldef,keystr):
                record = govbase.query(Coldef).by_key(keystr)
                #returnjson['count'] = 1
                #returnjson['data'].append(record.json)
                returnjson = record.json
            return returnjson
        except Exception as exp:
            log.logger.error('Exception at Coldef.get_Coldef_bykey() %s ' % exp)
            if str(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")).strip().lower() == 'true':
                traceback.print_exc()

    def get_Coldef_byname(self,name):
        try:
            returnjson = {}
            returnjson['count'] = 0
            returnjson['data'] = []
            govbase = Govbase().db
            if govbase.has(Coldef,name):
                records = govbase.query(Coldef).filter("name=='"+name+"'").all()
                if len(records) >= 1:
                    #returnjson['count'] = 1
                    #returnjson['data'].append(records[0].json)
                    returnjson = records[0].json
            return returnjson
        except Exception as exp:
            log.logger.error('Exception at Coldef.get_Coldef_byname() %s ' % exp)
            if str(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")).strip().lower() == 'true':
                traceback.print_exc()

    def update_Coldef(self, jsonobj):
        try:
            govbase = Govbase().db
            updatejson = jsonobj
            if not updatejson.__contains__('_key'):
                updatejson['_key'] = updatejson['name']
            if govbase.has(Coldef, updatejson['_key']):
                updobj = Coldef._load(updatejson)
                govbase.update(updobj)
                log.logger.debug('===================== update coldef [ %s ] =====================' % updobj.name)
                if str(os.getenv("OSSGPAPI_OSSMODEL_UPDATE_SYNC")).strip().lower() == 'true':
                    self.genmodel(updobj.json)
                return updobj.json
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at Coldef.update_Coldef() %s ' % exp)
            if str(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")).strip().lower() == 'true':
                traceback.print_exc()

    def delete_Coldef(self,keystr):
        try:
            govbase = Govbase().db
            if govbase.has(Coldef, keystr):
                #log.logger.debug(govbase.delete(govbase.query(Coldef).by_key(keystr)))
                if not str(os.getenv("OSSGPAPI_OSSMODEL_SAFETY_DELETE")).strip().lower() == 'true':
                    log.logger.debug('===================== delete coldef [ %s ] =====================' % keystr)
                    #delete collection
                    log.logger.debug('===================== delete model [ %s ] =====================' % keystr)
                    ossmodelcls = importlib.import_module('ossmodel.' + keystr.lower())
                    ossmodel = getattr(ossmodelcls, keystr.capitalize())()
                    ossbase = Ossbase().db
                    if ossbase.has_collection(keystr):
                        ossbase.drop_collection(ossmodel)
                    #delete model
                    log.logger.debug('===================== delete model file [ %s ] =====================' % keystr)
                    self.delmodel(keystr)
                return govbase.delete(govbase.query(Coldef).by_key(keystr))
            else:
                return None
        except Exception as exp:
            log.logger.error('Exception at Coldef.delete_Coldef() %s ' % exp)
            if str(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")).strip().lower() == 'true':
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
            if str(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")).strip().lower() == 'true':
                traceback.print_exc()

    def genmodel(self,defjson):
        try:
            basepath = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
            apppath = os.path.abspath(os.path.join(basepath, os.pardir))
            tmplpath = os.path.abspath(os.path.join(apppath, 'tmpl'))
            sysmodelspath = os.path.abspath(os.path.join(apppath, 'ossmodel'))
            osskeeplist = os.getenv("OSSGPAPI_OSSMODEL_UPDATE_KEEP_LIST")
            defobj = defjson
            defobj['coldef'] = json.loads(defobj['coldef'])
            if defobj['name'] not in osskeeplist:
                log.logger.debug('Generate Model for [ %s ] ......' % defobj['name'])
                modelfilepath = os.path.abspath(os.path.join(sysmodelspath, defobj['name'].lower() + ".py"))
                log.logger.debug('Model will save at file: [ %s ]' % modelfilepath)
                renderenv = genenv(loader=FileSystemLoader(tmplpath), trim_blocks=True, lstrip_blocks=True)
                template = renderenv.get_template('ossmodel_gen_tmpl.py')
                gencode = template.render({'defobj':defobj})
                with open(modelfilepath, 'w', encoding='utf-8') as gencodefile:
                    gencodefile.write(gencode)
                    gencodefile.close()
                    log.logger.debug('Model file: [ %s ] saved !' % modelfilepath)
        except Exception as exp:
            log.logger.error('Exception at Coldef.genmodel() %s ' % exp)
            if str(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")).strip().lower() == 'true':
                traceback.print_exc()

    def delmodel(self,modelname):
        try:
            basepath = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
            apppath = os.path.abspath(os.path.join(basepath, os.pardir))
            sysmodelspath = os.path.abspath(os.path.join(apppath, 'ossmodel'))
            osskeeplist = os.getenv("OSSGPAPI_OSSMODEL_UPDATE_KEEP_LIST")
            if modelname not in osskeeplist:
                log.logger.debug('Delete Model for [ %s ] ......' % modelname)
                modelfilepath = os.path.abspath(os.path.join(sysmodelspath, modelname.lower() + ".py"))
                if os.path.exists(modelfilepath):
                    os.remove(modelfilepath)
                else:
                    log.logger.error('The file [ %s ] does not exist' % modelfilepath)
        except Exception as exp:
            log.logger.error('Exception at Coldef.delmodel() %s ' % exp)
            if str(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")).strip().lower() == 'true':
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
    coldef = Coldef()

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
                         coldef=json.dumps(userscoldefjson),  # 必须是string类型的json，不能是json对象
                         createdate=date.today())
    log.logger.debug("userscoldef.has_Coldef_schema(userscoldef.name): %s" % userscoldef.has_Coldef_schema(userscoldef.name))
    log.logger.debug("userscoldef.existed_Coldef(): %s" % userscoldef.existed_Coldef(userscoldef.name))
    '''
    if not userscoldef.has_Coldef_schema(userscoldef.name):
        govbase.add(userscoldef)
        if not userscoldef.existed_Coldef(userscoldef.name):
            govbase.add(userscoldef)
    log.logger.debug("Coldef.get_Coldef_bykey('users'): %s" % coldef.get_Coldef_bykey('users'))
    log.logger.debug("Coldef.get_Coldef_byname('users'): %s" % coldef.get_Coldef_byname('users'))
    '''
    log.logger.debug(coldef.get_all_Coldef())
    log.logger.debug(coldef.get_all_Coldef_names())
    log.logger.debug(coldef.get_Coldef_byname('users'))
    defobj = {'name': 'software1', 'coltype': 'document', 'keyfieldname': 'name', 'coldef': '{"__collection__":"software1","_index":"[{\'type\':\'hash\', \'fields\':[\'name\'], \'unique\':True}]","_key":"String(required=True)","name":"String(required=True, allow_none=False)","title":"String(required=True, allow_none=False)","content":"String(required=True, allow_none=False)","createdate":"Date()","type":"String(required=True, allow_none=False)","software":"String(required=True, allow_none=False)","platform":"String(required=True, allow_none=False)","level":"String(required=True, allow_none=False)","source":"String(required=True, allow_none=False)","link":"String(required=True, allow_none=False)","solution":"String(required=True, allow_none=False)"}', 'createdate': date.today()}
    log.logger.debug(defobj)
    coldef.genmodel(defobj)


