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
import os
import traceback

from arango_orm import Relation

from core.ossbase import Ossbase
import simplejson as json
from env.environment import Environment
from sysmodel.graph import Graph
from sysmodel.relation import Relation as OSSRelation
from util import log


'''logging'''
env = Environment()
log = log.Logger(level=os.getenv('OSSGPAPI_APP_LOG_LEVEL'))

def refresh_relations(graphname):
    log.logger.debug('Refresh OSS Relations: 1. Check Graph information:')
    graphmodels = get_model_from_graph(graphname)
    log.logger.debug('Refresh OSS Relations: 2. Clear old relations:')
    clear_relation(graphname)
    log.logger.debug('Refresh OSS Relations: 3. Rebuild relation: Starting')
    rebuild_relation(graphmodels)

def rebuild_relation(graphmodels):
    try:
        ossbase = Ossbase().db
        total = 0
        for modelname in graphmodels.keys():
            log.logger.debug('Refresh OSS Relations: 3. Rebuild relation: for Model [ %s ]' % modelname)
            fromclsimport = importlib.import_module('ossmodel.' + modelname.strip().lower())
            fromcls = getattr(fromclsimport, modelname.strip().capitalize())()
            docqrystr = 'FOR doc IN ' + modelname + ' RETURN doc'
            #log.logger.debug('docqrystr is : %s' % docqrystr)
            maindoccursor = ossbase.aql.execute(docqrystr, batch_size=100, count=True)
            for doc in maindoccursor:
                #log.logger.debug('doc is: %s' % doc)
                for relationdef in graphmodels[modelname]:
                    log.logger.debug('Refresh OSS Relations: 3. Rebuild relation: for Model document [ %s ] - Relation [ %s ]' % (doc['_key'],relationdef['name']))
                    graphfromkey = doc[relationdef['fromkey']]
                    graphrelation = relationdef['relation']
                    toclsimport = importlib.import_module('ossmodel.' + relationdef['tomodel'].lower())
                    tocls = getattr(toclsimport, relationdef['tomodel'].capitalize())()
                    redocqrystr = ''
                    if graphrelation.lower() == 'equal':
                        #check Equal
                        redocqrystr = 'FOR doc IN ' + relationdef['tomodel'] + ' FILTER doc.' + relationdef[
                            'tokey'] + ' == "' + graphfromkey.strip() + '" RETURN doc'
                        #log.logger.debug('redocqrystr is : %s' % redocqrystr)
                    elif graphrelation.lower() == 'contains':
                        #check Contains
                        docvallist = graphfromkey.strip().strip('[').strip(']').split(',')
                        docvalliststr = '['+','.join('"' + li.strip() + '"' for li in docvallist)+']'
                        redocqrystr = 'FOR doc IN ' + relationdef['tomodel'] + ' FILTER doc.' + relationdef[
                            'tokey'] + ' IN ' + docvalliststr + ' RETURN doc'
                        #log.logger.debug('redocqrystr is : %s' % redocqrystr)
                    else:
                        #check Belongs
                        redocqrystr = 'FOR doc IN ' + relationdef['tomodel'] + ' FILTER doc.' + relationdef[
                            'tokey'] + ' LIKE "%' + graphfromkey.strip() + ',%" or doc.' + relationdef[
                            'tokey'] + ' LIKE "%,' + graphfromkey.strip() + '%"  RETURN doc'
                        #log.logger.debug('redocqrystr is : %s' % redocqrystr)
                    relationdoccursor = ossbase.aql.execute(redocqrystr, batch_size=100, count=True)
                    #log.logger.debug('redoc count is : %s' % relationdoccursor.count())
                    log.logger.debug(
                        'Refresh OSS Relations: 3. Rebuild relation: for Model document [ %s ] - Relation [ %s ], rebuild %s relation documents' % (
                        doc['_key'], relationdef['name'], relationdoccursor.count()))
                    total = total + relationdoccursor.count()
                    for redoc in relationdoccursor:
                        ra = Relation(collection_name=relationdef['name'], _collections_from=fromcls,
                                      _collections_to=tocls, _from=relationdef['frommodel'] + '/' + doc['_key'],
                                      _to=relationdef['tomodel'] + '/' + redoc['_key'],
                                      _key='kra_' + relationdef['frommodel'] + '_' + doc['_key'] + '_' + relationdef[
                                          'tomodel'] + '_' + redoc['_key'])
                        ossbase.add(ra, if_present='update')
        log.logger.debug('Refresh OSS Relations complete, %s relation documents rebuild' % total )
    except Exception as exp:
        log.logger.error('Exception at reloadgraph.rebuild_relation() %s ' % exp)
        if str(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")).strip().lower() == 'true':
            traceback.print_exc()

def clear_relation(graphname):
    try:
        ossbase = Ossbase().db
        graph = Graph().get_Graph_byname(graphname)
        ralist = graph['relations'].strip().strip('[').strip(']').split(',')
        raliststr = '['+','.join('"' + li.strip() + '"' for li in ralist)+']'
        qjson = {
            'filter': ['name IN ' + raliststr],
            'sort': 'name ASC'
        }
        relations = OSSRelation().query_Relation(qjson)['data']
        for ra in relations:
            if ossbase.has_collection(ra['name']):
                racollection = ossbase.collection(ra['name'])
                racollection.truncate()
    except Exception as exp:
        log.logger.error('Exception at reloadgraph.clear_relation() %s ' % exp)
        if str(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")).strip().lower() == 'true':
            traceback.print_exc()

def get_model_from_graph(graphname):
    try:
        graph = Graph().get_Graph_byname(graphname)
        ralist = graph['relations'].strip().strip('[').strip(']').split(',')
        raliststr = '['+','.join('"' + li.strip() + '"' for li in ralist)+']'
        qjson = {
            'filter': ['name IN ' + raliststr],
            'sort': 'name ASC'
        }
        relations = OSSRelation().query_Relation(qjson)['data']
        returnjson = {}
        for ra in relations:
            if ra['frommodel'] in returnjson.keys():
                returnjson[ra['frommodel']].append(ra)
            else:
                returnjson[ra['frommodel']] = []
                returnjson[ra['frommodel']].append(ra)
        return returnjson
    except Exception as exp:
        log.logger.error('Exception at reloadgraph.get_model_from_graph() %s ' % exp)
        if str(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")).strip().lower() == 'true':
            traceback.print_exc()


if __name__ == '__main__':
    #refresh_relations('university')
    graphmodels = get_model_from_graph('university')
    log.logger.debug(graphmodels)
    #clear_relation('university')
    #rebuild_relation(graphmodels)
