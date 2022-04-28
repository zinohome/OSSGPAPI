#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: OSSGPAPI


from pydantic import BaseModel, Required
from pydantic.class_validators import Optional
from pydantic.types import Json, List, Dict

class CollectionQueryBody(BaseModel):
    filter: Optional[str] = None  # eg. "['name=="qname1"', 'name=="qname2"']"
    filteror: Optional[str] = None   # eg. "['name=="admin"']"
    sort: Optional[str] = None
    limit: Optional[int] = 10
    offset: Optional[int] = 0
    class Config:
        title = 'Collection Query Model'
        anystr_strip_whitespace = True

class DocumentBody(BaseModel):
    data: Dict = None
    class Config:
        title = 'Document Model'
        anystr_strip_whitespace = True

