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
import os
import traceback

from core.ossbase import Ossbase
import simplejson as json
from env.environment import Environment
from sysmodel.graph import Graph
from util import log


'''logging'''
env = Environment()
log = log.Logger(level=os.getenv('OSSGPAPI_APP_LOG_LEVEL'))


def get_model_from_graph(graphname):
    try:
        pass
        graph = Graph().get_Graph_byname(graphname)
        log.logger.debug(graph)
    except Exception as exp:
        log.logger.error('Exception at Graph.get_model_from_graph() %s ' % exp)
        if distutils.util.strtobool(os.getenv("OSSGPAPI_APP_EXCEPTION_DETAIL")):
            traceback.print_exc()


if __name__ == '__main__':
    get_model_from_graph('university')