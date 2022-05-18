#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2022 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2022
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: OSSGPAPI
import os
import traceback
from jinja2 import Environment, FileSystemLoader
from env.environment import Environment as osenv
from util import log

'''logging'''
env = osenv()
log = log.Logger(level=os.getenv('OSSGPAPI_APP_LOG_LEVEL'))

def genossmodel(namelist):
    basepath = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
    apppath = os.path.abspath(os.path.join(basepath, os.pardir))
    tmplpath = os.path.abspath(os.path.join(apppath, 'tmpl'))
    sysmodelspath = os.path.abspath(os.path.join(apppath, 'ossmodel'))
    for name in namelist:
        if name == 'users':
            pass
        else:
            log.logger.debug('Generate Model for %s ......' % name)
            modelfilepath = os.path.abspath(os.path.join(sysmodelspath, name.lower() + ".py"))
            log.logger.debug('Model will save at file: [ %s ]' % modelfilepath)
            renderenv = Environment(loader=FileSystemLoader(tmplpath), trim_blocks=True, lstrip_blocks=True)
            template = renderenv.get_template('ossmodel_tmpl.py')
            gencode = template.render({'name':name})
            with open(modelfilepath, 'w', encoding='utf-8') as gencodefile:
                gencodefile.write(gencode)
                gencodefile.close()
            log.logger.debug('Model file: [ %s ] saved !' % modelfilepath)

if __name__ == '__main__':
    modelnames = ['license']
    genossmodel(modelnames)
