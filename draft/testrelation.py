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

from arango_orm import GraphConnection, Graph, Collection, Relation
from marshmallow.fields import String

from core.ossbase import Ossbase
import simplejson as json
from env.environment import Environment
from util import log
from ossmodel.student import Student
from ossmodel.teacher import Teacher
from ossmodel.subject import Subject
from sysmodel.relation import Relation as OssRelation

'''logging'''
env = Environment()
log = log.Logger(level=os.getenv('OSSGPAPI_APP_LOG_LEVEL'))


if __name__ == '__main__':
    ossbase = Ossbase().db
    tst = Student()
    tsu = Subject()
    ttc = Teacher()
    newtst1 = '{"name": "student1","age": 18,"subjects":"[subject1,subject2]","teachers":"[teacher1,teacher2]"}'
    newtst2 = '{"name": "student2","age": 19,"subjects":"[subject2,subject3]","teachers":"[teacher2,teacher3]"}'
    newtst3 = '{"name": "student3","age": 20,"subjects":"[subject1,subject3]","teachers":"[teacher1,teacher3]"}'
    newtst4 = '{"name": "student4","age": 21,"subjects":"[subject2,subject3]","teachers":"[teacher1,teacher4]"}'
    newtsu1 = '{"name": "subject1","credit_hours": 40,"has_labs":false}'
    newtsu2 = '{"name": "subject2","credit_hours": 40,"has_labs":true}'
    newtsu3 = '{"name": "subject3","credit_hours": 40,"has_labs":false}'
    newttc1 = '{"name": "teacher1","age": 36,"subjects":"[subject1]","expertsubs":"[subject1,subject3]"}'
    newttc2 = '{"name": "teacher2","age": 46,"subjects":"[subject2]","expertsubs":"[subject2,subject1]"}'
    newttc3 = '{"name": "teacher3","age": 51,"subjects":"[subject3]","expertsubs":"[subject3,subject2]"}'
    newttc4 = '{"name": "teacher4","age": 35,"subjects":"[subject3,subject1]","expertsubs":"[subject1,subject3]"}'
    tst1 = tst.createStudent(json.loads(newtst1))
    tst2 = tst.createStudent(json.loads(newtst2))
    tst3 = tst.createStudent(json.loads(newtst3))
    tst4 = tst.createStudent(json.loads(newtst4))
    tsu1 = tsu.createSubject(json.loads(newtsu1))
    tsu1 = tsu.createSubject(json.loads(newtsu2))
    tsu1 = tsu.createSubject(json.loads(newtsu3))
    ttc1 = ttc.createTeacher(json.loads(newttc1))
    ttc2 = ttc.createTeacher(json.loads(newttc2))
    ttc3 = ttc.createTeacher(json.loads(newttc3))
    ttc4 = ttc.createTeacher(json.loads(newttc4))
    #log.logger.debug(ttc.loadfromjson(ttc.getTeacherbykey('teacher3')))

    '''
    allrelation = OssRelation().get_all_Relation()
    for relation in allrelation:
        fromclsimport = importlib.import_module('ossmodel.' + relation['frommodel'].lower())
        fromcls = getattr(fromclsimport, relation['frommodel'].capitalize())()
        toclsimport = importlib.import_module('ossmodel.' + relation['tomodel'].lower())
        tocls = getattr(fromclsimport, relation['frommodel'].capitalize())()
        ra = Relation(collection_name=relation['name'],_collections_from=fromcls,_collections_to=tocls)
        if not ossbase.has_collection(relation['name']):
            ossbase.create_collection(ra, edge=True)
        #if ossbase.has_collection(relation['name']):
        #    ossbase.delete_collection(relation['name'])

    graph_connections = []
    for relation in allrelation:
        log.logger.debug(relation)
        fromclsimport = importlib.import_module('ossmodel.' + relation['frommodel'].lower())
        fromcls = getattr(fromclsimport, relation['frommodel'].capitalize())()
        toclsimport = importlib.import_module('ossmodel.' + relation['tomodel'].lower())
        tocls = getattr(toclsimport, relation['tomodel'].capitalize())()
        graph_connections.append(GraphConnection(fromcls, Relation(relation['name']), tocls))
    tgraph = Graph('university',graph_connections,ossbase)
    if not ossbase.has_graph('university'):
        ossbase.create_graph(tgraph)

    ra1 = Relation(collection_name='ra_student_subject_study', _collections_from=Student, _collections_to=Subject, _from = 'student/student1', _to = 'subject/subject1', _key = 'kra_student_student1_subject_subject1')
    ra2 = Relation(collection_name='ra_student_subject_study', _collections_from=Student, _collections_to=Subject, _from = 'student/student1', _to = 'subject/subject2', _key = 'kra_student_student1_subject_subject2')
    ra3 = Relation(collection_name='ra_student_subject_study', _collections_from=Student, _collections_to=Subject, _from = 'student/student2', _to = 'subject/subject2', _key = 'kra_student_student2_subject_subject2')
    ra4 = Relation(collection_name='ra_student_subject_study', _collections_from=Student, _collections_to=Subject, _from = 'student/student2', _to = 'subject/subject3', _key = 'kra_student_student2_subject_subject3')
    ra5 = Relation(collection_name='ra_student_subject_study', _collections_from=Student, _collections_to=Subject, _from = 'student/student3', _to = 'subject/subject1', _key = 'kra_student_student3_subject_subject1')
    ra6 = Relation(collection_name='ra_student_subject_study', _collections_from=Student, _collections_to=Subject, _from = 'student/student3', _to = 'subject/subject3', _key = 'kra_student_student3_subject_subject3')

    ossbase.add(ra1,if_present='update')
    ossbase.add(ra2,if_present='update')
    ossbase.add(ra3,if_present='update')
    ossbase.add(ra4,if_present='update')
    ossbase.add(ra5,if_present='update')
    ossbase.add(ra6,if_present='update')
    
    ossbase.add(tgraph.relation(tst.loadfromjson(json.loads(newtst1)), Relation("ra_student_subject_study"), tsu.loadfromjson(json.loads(newtsu1))),if_present='update')
    ossbase.add(tgraph.relation(tst.loadfromjson(json.loads(newtst1)), Relation("ra_student_subject_study"), tsu.loadfromjson(json.loads(newtsu2))),if_present='update')
    ossbase.add(tgraph.relation(tst.loadfromjson(json.loads(newtst2)), Relation("ra_student_subject_study"), tsu.loadfromjson(json.loads(newtsu2))),if_present='update')
    ossbase.add(tgraph.relation(tst.loadfromjson(json.loads(newtst2)), Relation("ra_student_subject_study"), tsu.loadfromjson(json.loads(newtsu3))),if_present='update')
    ossbase.add(tgraph.relation(tst.loadfromjson(json.loads(newtst3)), Relation("ra_student_subject_study"), tsu.loadfromjson(json.loads(newtsu1))),if_present='update')
    ossbase.add(tgraph.relation(tst.loadfromjson(json.loads(newtst3)), Relation("ra_student_subject_study"), tsu.loadfromjson(json.loads(newtsu3))),if_present='update')

'''





