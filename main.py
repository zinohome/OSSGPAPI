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

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from env.environment import Environment
from ossmodels.users import Users
from util import log
import traceback
import simplejson as json

'''logging'''
env = Environment()
log = log.Logger(level=os.getenv('OSSGPAPI_APP_LOG_LEVEL'))

'''app_dir'''
app_dir = os.path.dirname(os.path.abspath(__file__))

'''services_model'''
services_model = 0 #'Standalone'
if os.getenv('OSSGPAPI_APP_SERVICE_MODEL') == 'OpenReader':
    services_model = 1 #'OpenReader'
if os.getenv('OSSGPAPI_APP_SERVICE_MODEL') == 'OpenWriter':
    services_model = 2 #'OpenWriter'

'''API prefix'''
prefix = os.getenv('OSSGPAPI_APP_PREFIX')
if prefix.startswith('/'):
    pass
else:
    prefix = '/' + prefix
log.logger.info(os.getenv('OSSGPAPI_APP_NAME') + ' Start Up ....')
log.logger.info("API prefix is: [ %s ]" % prefix)

'''API define'''
app = FastAPI(
    title=os.getenv('OSSGPAPI_APP_NAME'),
    description=os.getenv('OSSGPAPI_APP_DESCRIPTION'),
    version=os.getenv('OSSGPAPI_APP_VERSION'),
    openapi_url=prefix+"/openapi.json",
    docs_url=None,
    redoc_url=None
)

favicon_path = 'static/favicon.ico'
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup_event():
    log.logger.info(os.getenv('OSSGPAPI_APP_NAME') + ' Starting ....')
    apiusers = Users()
    apiusers.initsysUsers()
    log.logger.info(os.getenv('OSSGPAPI_APP_NAME') + ' Started')

@app.on_event("shutdown")
def shutdown_event():
    log.logger.info(os.getenv('OSSGPAPI_APP_NAME')  + ' Shutting Down ....')

'''CORS'''
origins = []
# Set all CORS enabled origins
if os.getenv('OSSGPAPI_APP_CORS_ORIGINS'):
    origins_raw = os.getenv('OSSGPAPI_APP_CORS_ORIGINS').split(",")
    for origin in origins_raw:
        use_origin = origin.strip()
        origins.append(use_origin)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

'''app route'''

@app.get("/",
         tags=["Default"],
         summary="Get information for this application.",
         description="Return application information",
         include_in_schema=False)
async def app_root():
    log.logger.debug('Access \'/\' : run in app_root()')
    return {
        "Application_Name": os.getenv('OSSGPAPI_APP_NAME'),
        "Version": os.getenv('OSSGPAPI_APP_VERSION'),
        "Author": "ibmzhangjun@139.com",
        "Description": os.getenv('OSSGPAPI_APP_DESCRIPTION')
    }

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(os.path.join(app_dir, 'static/favicon.ico'))

@app.get("/apidocs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_favicon_url="/static/favicon.ico",
        swagger_css_url="/static/swagger-ui.css",
    )