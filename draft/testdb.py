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

from env.environment import Environment
from core.systembase import Systembase
from core.govbase import Govbase
from core.userbase import Userbase

if __name__ == '__main__':
    basepath = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
    apppath = os.path.abspath(os.path.join(basepath, os.pardir))
    envpath = os.path.abspath(os.path.join(apppath, '.env'))
    print(envpath)


    env = Environment()
    sysbase = Systembase()
    print(sysbase.db)
    govbase = Govbase()
    print(govbase.db)
    userbase = Userbase()
    print(userbase.db)

