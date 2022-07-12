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
import importlib
import os
import traceback

from arango_orm import Relation

from core.ossbase import Ossbase
from env.environment import Environment
from sysmodel.graph import Graph
from sysmodel.relation import Relation as OSSRelation
from util import log


'''logging'''
env = Environment()
log = log.Logger(level=os.getenv('OSSGPAPI_APP_LOG_LEVEL'))

def create_relation(modelname, key, graphname, getallmodel):
    try:
        ossbase = Ossbase().db
        fromclsimport = importlib.import_module('ossmodel.' + modelname.strip().lower())
        fromcls = getattr(fromclsimport, modelname.strip().capitalize())()
        fromcol = ossbase.collection(modelname)
        fromdoc = fromcol.get({'_key': key})
        if not fromdoc is None:
            relationjson = get_all_relations(modelname, graphname, getallmodel)
            fromrelation = relationjson['from']
            torelation = relationjson['to']
            for raname, radef in fromrelation.items():
                #log.logger.debug(radef)
                graphkey = fromdoc[radef['fromkey']]
                graphrelation = radef['relation']
                toclsimport = importlib.import_module('ossmodel.' + radef['tomodel'].lower())
                tocls = getattr(toclsimport, radef['tomodel'].capitalize())()
                redocqrystr = ''
                if graphrelation.lower() == 'equal':
                    # check Equal
                    redocqrystr = 'FOR doc IN ' + radef['tomodel'] + ' FILTER doc.' + radef[
                        'tokey'] + ' == "' + graphkey.strip() + '" RETURN doc'
                    # log.logger.debug('redocqrystr is : %s' % redocqrystr)
                elif graphrelation.lower() == 'contains':
                    # check Contains
                    docvallist = graphkey.strip().strip('[').strip(']').split(',')
                    docvalliststr = '[' + ','.join('"' + li.strip() + '"' for li in docvallist) + ']'
                    redocqrystr = 'FOR doc IN ' + radef['tomodel'] + ' FILTER doc.' + radef[
                        'tokey'] + ' IN ' + docvalliststr + ' RETURN doc'
                    # log.logger.debug('redocqrystr is : %s' % redocqrystr)
                else:
                    # check Belongs
                    redocqrystr = 'FOR doc IN ' + radef['tomodel'] + ' FILTER doc.' + radef[
                        'tokey'] + ' LIKE "%' + graphkey.strip() + ',%" or doc.' + radef[
                                      'tokey'] + ' LIKE "%,' + graphkey.strip() + '%"  RETURN doc'
                    # log.logger.debug('redocqrystr is : %s' % redocqrystr)
                relationdoccursor = ossbase.aql.execute(redocqrystr, batch_size=100, count=True)
                for redoc in relationdoccursor:
                    ra = Relation(collection_name=radef['name'], _collections_from=fromcls,
                                  _collections_to=tocls, _from=radef['frommodel'] + '/' + fromdoc['_key'],
                                  _to=radef['tomodel'] + '/' + redoc['_key'],
                                  _key='kra_' + radef['frommodel'] + '_' + fromdoc['_key'] + '_' + radef[
                                      'tomodel'] + '_' + redoc['_key'])
                    ossbase.add(ra, if_present='update')
            for raname, radef in torelation.items():
                #log.logger.debug(radef)
                graphkey = fromdoc[radef['tokey']]
                graphrelation = radef['relation']
                fromclsimport = importlib.import_module('ossmodel.' + radef['frommodel'].lower())
                fromcls = getattr(fromclsimport, radef['frommodel'].capitalize())()
                toclsimport = importlib.import_module('ossmodel.' + modelname.strip().lower())
                tocls = getattr(toclsimport, modelname.strip().capitalize())()
                redocqrystr = ''
                if graphrelation.lower() == 'equal':
                    # check Equal
                    redocqrystr = 'FOR doc IN ' + radef['frommodel'] + ' FILTER doc.' + radef[
                        'fromkey'] + ' == "' + graphkey.strip() + '" RETURN doc'
                    # log.logger.debug('redocqrystr is : %s' % redocqrystr)
                elif graphrelation.lower() == 'contains':
                    # check Contains
                    redocqrystr = 'FOR doc IN ' + radef['frommodel'] + ' FILTER doc.' + radef[
                        'fromkey'] + ' LIKE "%' + graphkey.strip() + ',%" or doc.' + radef[
                                      'fromkey'] + ' LIKE "%,' + graphkey.strip() + '%"  RETURN doc'
                    # log.logger.debug('redocqrystr is : %s' % redocqrystr)
                else:
                    # check Belongs
                    docvallist = graphkey.strip().strip('[').strip(']').split(',')
                    docvalliststr = '[' + ','.join('"' + li.strip() + '"' for li in docvallist) + ']'
                    redocqrystr = 'FOR doc IN ' + radef['frommodel'] + ' FILTER doc.' + radef[
                        'fromkey'] + ' IN ' + docvalliststr + ' RETURN doc'
                    # log.logger.debug('redocqrystr is : %s' % redocqrystr)
                relationdoccursor = ossbase.aql.execute(redocqrystr, batch_size=100, count=True)
                for redoc in relationdoccursor:
                    ra = Relation(collection_name=radef['name'], _collections_from=fromcls,
                                  _collections_to=tocls, _from=radef['frommodel'] + '/' + redoc['_key'],
                                  _to=radef['tomodel'] + '/' + fromdoc['_key'],
                                  _key='kra_' + radef['frommodel'] + '_' + redoc['_key'] + '_' + radef[
                                      'tomodel'] + '_' + fromdoc['_key'])
                    ossbase.add(ra, if_present='update')
    except Exception as exp:
        log.logger.error('Exception at reloadrelation.create_relation() %s ' % exp)
        if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
            traceback.print_exc()

def del_relation(modelname, key, graphname, getallmodel):
    try:
        ossbase = Ossbase().db
        fromclsimport = importlib.import_module('ossmodel.' + modelname.strip().lower())
        fromcls = getattr(fromclsimport, modelname.strip().capitalize())()
        fromcol = ossbase.collection(modelname)
        fromdoc = fromcol.get({'_key': key})
        if not fromdoc is None:
            relationjson = get_all_relations(modelname, graphname, getallmodel)
            fromrelation = relationjson['from']
            torelation = relationjson['to']
            for raname, radef in fromrelation.items():
                redocqrystr = 'FOR doc IN ' + raname + ' FILTER doc._from == "' + modelname + '/' + key + '" REMOVE { _key: doc._key } IN ' + raname
                #log.logger.debug(redocqrystr)
                ossbase.aql.execute(redocqrystr, batch_size=100, count=True)
            for raname, radef in torelation.items():
                redocqrystr = 'FOR doc IN ' + raname + ' FILTER doc._to == "' + modelname + '/' + key + '" REMOVE { _key: doc._key } IN ' + raname
                #log.logger.debug(redocqrystr)
                ossbase.aql.execute(redocqrystr, batch_size=100, count=True)
    except Exception as exp:
        log.logger.error('Exception at reloadrelation.del_relation() %s ' % exp)
        if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
            traceback.print_exc()

def get_all_relations(modelname, graphname, getallmodel):
    try:
        returnjson = {'from':{},'to':{}}
        if not getallmodel:
            graph = Graph().get_Graph_byname(graphname)
            ralist = graph['relations'].strip().strip('[').strip(']').split(',')
            raliststr = '[' + ','.join('"' + li.strip() + '"' for li in ralist) + ']'
            qjson = {
                'filter': ['name IN ' + raliststr],
                'sort': 'name ASC'
            }
            relations = OSSRelation().query_Relation(qjson)['data']
            for ra in relations:
                if ra['frommodel'].strip().lower() == modelname:
                    returnjson['from'][ra['name']] = ra
                if ra['tomodel'].strip().lower() == modelname:
                    returnjson['to'][ra['name']] = ra
        else:
            graphs = Graph().get_all_Graph()
            for graph in graphs:
                ralist = graph['relations'].strip().strip('[').strip(']').split(',')
                raliststr = '[' + ','.join('"' + li.strip() + '"' for li in ralist) + ']'
                qjson = {
                    'filter': ['name IN ' + raliststr],
                    'sort': 'name ASC'
                }
                relations = OSSRelation().query_Relation(qjson)['data']
                for ra in relations:
                    if ra['frommodel'].strip().lower() == modelname:
                        returnjson['from'][ra['name']] = ra
                    if ra['tomodel'].strip().lower() == modelname:
                        returnjson['to'][ra['name']] = ra
        return returnjson
    except Exception as exp:
        log.logger.error('Exception at reloadrelation.get_all_relations() %s ' % exp)
        if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
            traceback.print_exc()

if __name__ == '__main__':
    ralist = get_all_relations('teacher','university',True)
    log.logger.debug(ralist)
    ossbase = Ossbase().db
    graphs = Graph().get_all_Graph()
    log.logger.debug(graphs)
    graph = ossbase.graph('university')
    clasname = 'student'
    fromclsimport = importlib.import_module('ossmodel.' + clasname.lower())
    fromcls = getattr(fromclsimport, clasname.capitalize())()
    st1 = ossbase.query(fromcls).by_key("student1")
    log.logger.debug(st1._id)
    results = graph.traverse(start_vertex=st1._id,
                             direction='outbound',
                             strategy='dfs',
                             edge_uniqueness='global',
                             vertex_uniqueness='global',)
    log.logger.debug(results)
    log.logger.debug(results.keys())
    log.logger.debug(len(results['vertices']))
    log.logger.debug(len(results['paths']))
    for vert in results['vertices']:
        log.logger.debug(vert)
        #log.logger.debug(vert['_id'].split("/")[0])
    for path in results['paths']:
        log.logger.debug(path)
    #log.logger.debug(results['paths'])

    #create_relation('student', 'student1', 'university', True)
    #del_relation('student', 'student2', 'university', True)
    #del_relation('subject', 'subject2', 'university', True)
    #del_relation('teacher', 'teacher2', 'university', True)
    #create_relation('student', 'student2', 'university', True)
    #create_relation('subject', 'subject2', 'university', True)
    #create_relation('teacher', 'teacher2', 'university', True)
    #create_relation('subject', 'subject1', 'university', True)
    #create_relation('subject', 'subject2', 'university', True)
    #create_relation('subject', 'subject4', 'university', True)

    '''
    create_relation('student', 'student2', 'university', True)
    create_relation('student', 'student3', 'university', True)
    create_relation('teacher', 'teacher1', 'university', True)
    create_relation('teacher', 'teacher2', 'university', True)
    create_relation('teacher', 'teacher3', 'university', True)
    '''