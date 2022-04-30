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
from datetime import timedelta

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.openapi.docs import get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html, get_redoc_html
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse, JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from core import security, apimodel
from env.environment import Environment
from ossmodels.users import Users
from sysmodels.coldef import Coldef
from util import log
import traceback
import simplejson as json

'''logging'''
env = Environment()
log = log.Logger(level=os.getenv('OSSGPAPI_APP_LOG_LEVEL'))

'''app_dir'''
app_dir = os.path.dirname(os.path.abspath(__file__))

'''Users'''
apiusers = Users()

'''Coldef'''
coldef = Coldef()

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

@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()

@app.get("/apiredoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
        redoc_favicon_url="/static/favicon.ico",
        with_google_fonts=False,
    )

@app.post(prefix + "/token",
          response_model=security.Token,
          tags=["Security"],
          summary="Login to get access token.",
          description="",
          )
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    log.logger.debug('Access \'/token\' : run in login_for_access_token(), '
                     'input data username: [%s]' % form_data.username)
    user = security.authenticate_user(apiusers, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(os.getenv("OSSGPAPI_APP_AUTH_TOKEN_EXPIRE_MINUTES")))
    name = 'admin'
    role = '[admin]'
    active = 'True'
    access_token = security.create_access_token(
        data={"name": user.name, "role":user.role, "active":user.active}, expires_delta=access_token_expires
    )
    # return {"access_token": access_token, "token_type": "bearer"}
    rcontent = {"access_token": access_token, "token_type": "bearer"}
    return JSONResponse(status_code=status.HTTP_200_OK, content=rcontent)

@app.get(prefix + "/users",
         response_model=security.User,
         tags=["Security"],
         summary="Retrieve user information.",
         description="",
         )
async def read_users_me(current_user: security.User = Depends(security.get_current_active_user)):
    log.logger.debug('Access \'/users/\' : run in read_users_me()')
    return current_user

''' Read API'''
if services_model >= 1:
    @app.get(prefix + "/_collection/documentcount/{collection_name}",
             tags=["Data - Collection Level"],
             summary="Retrieve document count. ",
             description="",
             )
    async def get_data(collection_name: str):
        """
                        Parameters
                        - **collection_name** (path): **Required** - Name of the collection to perform operations on.
        """
        log.logger.debug(
            'Access \'/_collection/{collection_name}\' : run in get_data(), input data collection_name: [%s]' % collection_name)
        if not coldef.has_Coldef_schema(collection_name):
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail='Collection [ %s ] not found' % collection_name
            )
        ossmodelcls = importlib.import_module('ossmodels.' + collection_name.strip().lower())
        ossmodel = getattr(ossmodelcls, collection_name.strip().capitalize())()
        return getattr(ossmodel, 'get' + collection_name.strip().capitalize() + 'count')()

    @app.get(prefix + "/_collection/{collection_name}",
             tags=["Data - Collection Level"],
             summary="Retrieve one or more documents. ",
             description="",
             )
    async def get_data(collection_name: str, filter: str = Header(None),filteror: str = Header(None),sort: str = Header(None), limit: int = Header(int(os.getenv('OSSGPADMIN_API_QUERY_DEFAULT_LIMIT')), gt=0, le=int(os.getenv('OSSGPADMIN_API_QUERY_LIMIT_UPSET'))),
                       offset: int = Header(int(os.getenv('OSSGPADMIN_API_QUERY_DEFAULT_OFFSET')), gt=-1)):
        """
                                Parameters
                                - **collection_name** (path): **Required** - Name of the collection to perform operations on.
                                - **"filter"** (header): "string",  -- Optional - SQL-like filter to limit the records to retrieve. ex: ['name=="qname1"', 'name=="qname2"']
                                - **"filteror"** (header): "string",  -- Optional - SQL-like filter Parameter to limit the records to retrieve. ex: ['name=="qname1"', 'name=="qname2"']
                                - **"sort** (header)": "string",  -- Optional - SQL-like order containing field and direction for filter results. ex: 'phone_number ASC'
                                - **"limit"** (header): 0,  -- Optional - Set to limit the filter results.
                                - **"offset"** (header): 0,  -- Optional - Set to offset the filter results to a particular record count.
        """
        log.logger.debug(
            'Access \'/_collection/{collection_name}\' : run in get_data(), input data collection_name: [%s]' % collection_name)
        queryjson = {}
        queryjson['filter'] = filter
        queryjson['filteror'] = filteror
        queryjson['sort'] = sort
        queryjson['limit'] = limit
        queryjson['offset'] = offset
        log.logger.debug('queryjson: [%s]' % queryjson)
        if not coldef.has_Coldef_schema(collection_name):
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail='Collection [ %s ] not found' % collection_name
            )
        ossmodelcls = importlib.import_module('ossmodels.' + collection_name.strip().lower())
        ossmodel = getattr(ossmodelcls, collection_name.strip().capitalize())()
        return getattr(ossmodel, 'query' + collection_name.strip().capitalize())(queryjson)

    @app.post(prefix + "/_collection/_query/{collection_name}",
              tags=["Data - Collection Level"],
              summary="Retrieve one or more documents. ",
              description="", )
    async def query_data(collection_name: str, querybody: apimodel.CollectionQueryBody):
        """
                        Parameters
                        - **collection_name** (path): **Required** - Name of the table to perform operations on.
                        - **query body: **Required**
                        ```
                            {
                             "filter": "string",  -- Optional - SQL-like filter to limit the records to retrieve. ex: ['name=="qname1"', 'name=="qname2"']
                             "filteror": 'False',  -- Optional , SQL-like filter Parameter to limit the records to retrieve. ex: ['name=="qname1"', 'name=="qname2"']
                             "sort": "string",  -- Optional - SQL-like order containing field and direction for filter results. ex: 'phone_number ASC'
                             "limit": 0,  -- Optional - Set to limit the filter results.
                             "offset": 0,  -- Optional - Set to offset the filter results to a particular record count.
                             }
                        ```
                    """
        log.logger.debug(
            'Access \'/_collection/_query{collection_name}/\' : run in query_data(), input data collection_name: [%s]' % collection_name)
        log.logger.debug('querybody: [%s]' % querybody.json())
        ossmodelcls = importlib.import_module('ossmodels.' + collection_name.strip().lower())
        ossmodel = getattr(ossmodelcls, collection_name.strip().capitalize())()
        return getattr(ossmodel, 'query' + collection_name.strip().capitalize())(querybody)

    @app.get(prefix + "/_collection/{collection_name}/{key}",
             tags=["Data - Document Level"],
             summary="Retrieve one Document by key.",
             description="",
             )
    async def get_data_by_id(collection_name: str, key: str):
        log.logger.debug(
            'Access \'/_collection/{collection_name}/{key}\' : run in get_data_by_id(), input data collection_name: [%s]' % collection_name)
        log.logger.debug('key: [%s]' % key)
        if not coldef.has_Coldef_schema(collection_name):
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail='Collection [ %s ] not found' % collection_name
            )
        ossmodelcls = importlib.import_module('ossmodels.' + collection_name.strip().lower())
        ossmodel = getattr(ossmodelcls, collection_name.strip().capitalize())()
        return getattr(ossmodel, 'get' + collection_name.strip().capitalize() + 'bykey')(key)

else:
    @app.get(prefix + "/_sysdef/{collection_name}",
             tags=["System Define"],
             summary="Retrieve system define information.",
             description="",
             )
    async def get_sysdef(collection_name: str, current_user_role: bool = Depends(security.get_super_permission)):
        """
                This describes the collection
        """
        log.logger.debug(
            'Access \'/_sysdef/{collection_name}\' : run in get_sysdef, input collection_name: [ %s ]' % collection_name)


    @app.get(prefix + "/_collection/documentcount/{collection_name}",
             tags=["Data - Collection Level"],
             summary="Retrieve document count. ",
             description="",
             )
    async def get_data(collection_name: str,
                       current_user: security.User = Depends(security.get_current_active_user)):
        """
                        Parameters
                        - **collection_name** (path): **Required** - Name of the collection to perform operations on.
        """
        log.logger.debug(
            'Access \'/_collection/{collection_name}\' : run in get_data(), input data collection_name: [%s]' % collection_name)
        if not coldef.has_Coldef_schema(collection_name):
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail='Collection [ %s ] not found' % collection_name
            )
        ossmodelcls = importlib.import_module('ossmodels.' + collection_name.strip().lower())
        ossmodel = getattr(ossmodelcls, collection_name.strip().capitalize())()
        return getattr(ossmodel, 'get' + collection_name.strip().capitalize() + 'count')()

    @app.get(prefix + "/_collection/{collection_name}",
             tags=["Data - Collection Level"],
             summary="Retrieve one or more documents. ",
             description="",
             )
    async def get_data(collection_name: str, filter: str = Header(None), filteror: str = Header(None),
                       sort: str = Header(None), limit: int = Header(int(os.getenv('OSSGPADMIN_API_QUERY_DEFAULT_LIMIT')), gt=0, le=int(os.getenv('OSSGPADMIN_API_QUERY_LIMIT_UPSET'))),
                       offset: int = Header(int(os.getenv('OSSGPADMIN_API_QUERY_DEFAULT_OFFSET')), gt=-1),
                       current_user: security.User = Depends(security.get_current_active_user)):
        """
                        Parameters
                        - **collection_name** (path): **Required** - Name of the collection to perform operations on.
                        - **"filter"** (header): "string",  -- Optional - SQL-like filter to limit the records to retrieve. ex: ['name=="qname1"', 'name=="qname2"']
                        - **"filteror"** (header): "string",  -- Optional - SQL-like filter Parameter to limit the records to retrieve. ex: ['name=="qname1"', 'name=="qname2"']
                        - **"sort** (header)": "string",  -- Optional - SQL-like order containing field and direction for filter results. ex: 'phone_number ASC'
                        - **"limit"** (header): 0,  -- Optional - Set to limit the filter results.
                        - **"offset"** (header): 0,  -- Optional - Set to offset the filter results to a particular record count.
        """
        log.logger.debug(
            'Access \'/_collection/{collection_name}\' : run in get_data(), input data collection_name: [%s]' % collection_name)
        queryjson = {}
        queryjson['filter'] = filter
        queryjson['filteror'] = filteror
        queryjson['sort'] = sort
        queryjson['limit'] = limit
        queryjson['offset'] = offset
        log.logger.debug('queryjson: [%s]' % queryjson)
        if not coldef.has_Coldef_schema(collection_name):
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail='Collection [ %s ] not found' % collection_name
            )
        ossmodelcls = importlib.import_module('ossmodels.' + collection_name.strip().lower())
        ossmodel = getattr(ossmodelcls, collection_name.strip().capitalize())()
        return getattr(ossmodel, 'query' + collection_name.strip().capitalize())(queryjson)

    @app.post(prefix + "/_collection/_query/{collection_name}",
              tags=["Data - Collection Level"],
              summary="Retrieve one or more documents. ",
              description="", )
    async def query_data(collection_name: str, querybody: apimodel.CollectionQueryBody,
                         current_user: security.User = Depends(security.get_current_active_user)):
        """
                        Parameters
                        - **collection_name** (path): **Required** - Name of the table to perform operations on.
                        - **query body: **Required**
                        ```
                            {
                             "filter": "string",  -- Optional - SQL-like filter to limit the records to retrieve. ex: ['name=="qname1"', 'name=="qname2"']
                             "filteror": 'False',  -- Optional , SQL-like filter Parameter to limit the records to retrieve. ex: ['name=="qname1"', 'name=="qname2"']
                             "sort": "string",  -- Optional - SQL-like order containing field and direction for filter results. ex: 'phone_number ASC'
                             "limit": 0,  -- Optional - Set to limit the filter results.
                             "offset": 0,  -- Optional - Set to offset the filter results to a particular record count.
                             }
                        ```
                    """
        log.logger.debug(
            'Access \'/_collection/_query{collection_name}/\' : run in query_data(), input data collection_name: [%s]' % collection_name)
        log.logger.debug('querybody: [%s]' % querybody.json())
        if not coldef.has_Coldef_schema(collection_name):
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail='Collection [ %s ] not found' % collection_name
            )
        ossmodelcls = importlib.import_module('ossmodels.' + collection_name.strip().lower())
        ossmodel = getattr(ossmodelcls, collection_name.strip().capitalize())()
        return getattr(ossmodel, 'query' + collection_name.strip().capitalize())(querybody)

    @app.get(prefix + "/_collection/{collection_name}/{key}",
             tags=["Data - Document Level"],
             summary="Retrieve one Document by key.",
             description="",
             )
    async def get_data_by_id(collection_name: str, key: str,
                             current_user: security.User = Depends(security.get_current_active_user)):
        log.logger.debug(
            'Access \'/_collection/{collection_name}/{key}\' : run in get_data_by_id(), input data collection_name: [%s]' % collection_name)
        log.logger.debug('key: [%s]' % key)
        if not coldef.has_Coldef_schema(collection_name):
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail='Collection [ %s ] not found' % collection_name
            )
        ossmodelcls = importlib.import_module('ossmodels.' + collection_name.strip().lower())
        ossmodel = getattr(ossmodelcls, collection_name.strip().capitalize())()
        return getattr(ossmodel, 'get' + collection_name.strip().capitalize() + 'bykey')(key)

'''Write API'''

if services_model >= 2:
    @app.post(prefix + "/_collection/{collection_name}",
              tags=["Data - Collection Level"],
              summary="Create one document.",
              description="",
              )
    async def post_data(collection_name: str, docpost: apimodel.DocumentBody):
        """
                    Parameters
                    - **collection_name** (path): **Required** - Name of the collection to perform operations on.
                    - **request body: Required**
                    ```
                        {
                         "data": [{"name":"jack","phone":"55789"}]  -- **Required** - Json formated fieldname-fieldvalue pair. ex: '[{"name":"jack","phone":"55789"}]'
                         }
                    ```
        """
        log.logger.debug(
            'Access \'/_collection/{collection_name}\' : run in post_data(), input data collection_name: [%s]' % collection_name)
        log.logger.debug('body data: [%s]' % docpost.json())
        if not coldef.has_Coldef_schema(collection_name):
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail='Collection [ %s ] not found' % collection_name
            )
        ossmodelcls = importlib.import_module('ossmodels.' + collection_name.strip().lower())
        ossmodel = getattr(ossmodelcls, collection_name.strip().capitalize())()
        log.logger.debug(json.loads(docpost.json())['data'])
        return getattr(ossmodel, 'create' + collection_name.strip().capitalize())(json.loads(docpost.json())['data'])

    @app.put(prefix + "/_collection/{collection_name}",
             tags=["Data - Collection Level"],
             summary="Update one document.",
             description="",
             deprecated=False
             )
    async def put_data(collection_name: str, docput: apimodel.DocumentBody):
        """
                Parameters
                - **collection_name** (path): **Required** - Name of the collection to perform operations on.
                - **request body: Required**
                ```
                    {
                     "data": [{"name":"jack","phone":"55789"}]  -- **Required** - Json formated fieldname-fieldvalue pair. ex: '[{"name":"jack","phone":"55789"}]'
                     }
                ```
        """
        log.logger.debug(
            'Access \'/_collection/{collection_name}\' : run in put_data(), input data collection_name: [%s]' % collection_name)
        log.logger.debug('body: [%s]' % docput.json())
        if not coldef.has_Coldef_schema(collection_name):
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail='Collection [ %s ] not found' % collection_name
            )
        ossmodelcls = importlib.import_module('ossmodels.' + collection_name.strip().lower())
        ossmodel = getattr(ossmodelcls, collection_name.strip().capitalize())()
        return getattr(ossmodel, 'update' + collection_name.strip().capitalize())(json.loads(docput.json())['data'])

    @app.delete(prefix + "/_collection/{collection_name}",
                tags=["Data - Collection Level"],
                summary="Delete one document.",
                description="",
                )
    async def delete_data(collection_name: str,
                          keystr: str = Header(None),
                          current_user_role: bool = Depends(security.get_write_permission)):
        """
            Parameters
            - **collection_name** (path): **Required** - Name of the collection to perform operations on.
            - **keystr** (header): Optional - Key of the document need to be deleted
        """
        log.logger.debug(
            'Access \'/_collection/{collection_name}\' : run in delete_data(), input data collection_name: [%s]' % collection_name)
        log.logger.debug('keystr: [%s]' % keystr)
        if not coldef.has_Coldef_schema(collection_name):
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail='Collection [ %s ] not found' % collection_name
            )
        ossmodelcls = importlib.import_module('ossmodels.' + collection_name.strip().lower())
        ossmodel = getattr(ossmodelcls, collection_name.strip().capitalize())()
        return getattr(ossmodel, 'delete' + collection_name.strip().capitalize())(keystr)

    @app.put(prefix + "/_collection/{collection_name}/{key}",
             tags=["Data - Document Level"],
             summary="Replace the content of one document by key.",
             description="",
             )
    async def put_data_by_id(collection_name: str, key: str,
                             docput: apimodel.DocumentBody):
        """
                Parameters
                - **collection_name** (path): **Required** - Name of the collection to perform operations on.
                - **key** (path): **Required** - The key of document
                - **request body: Required**
                ```
                    {
                     "data": [{"name":"jack","phone":"55789"}]  -- **Required** - Json formated fieldname-fieldvalue pair. ex: '[{"name":"jack","phone":"55789"}]'
                     }
                ```
        """
        log.logger.debug(
            'Access \'/_collection/{collection_name}/{key}\' : run in put_data_by_id(), input data collection_name: [%s]' % collection_name)
        log.logger.debug('body: [%s]' % docput)
        log.logger.debug('key: [%s]' % key)
        if not coldef.has_Coldef_schema(collection_name):
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail='Collection [ %s ] not found' % collection_name
            )
        ossmodelcls = importlib.import_module('ossmodels.' + collection_name.strip().lower())
        ossmodel = getattr(ossmodelcls, collection_name.strip().capitalize())()
        upjson = json.loads(docput.json())['data']
        upjson['_key'] = key
        return getattr(ossmodel, 'update' + collection_name.strip().capitalize())(upjson)

    @app.delete(prefix + "/_collection/{collection_name}/{key}",
                tags=["Data - Document Level"],
                summary="Delete one document by key.",
                description="",
                )
    async def delete_data_by_id(collection_name: str, key: str):

        """
                    Parameters
                    - **collection_name** (path): **Required** - Name of the collection to perform operations on.
                    - **key** (header): Optional - Key of the document need to be deleted
        """
        log.logger.debug(
            'Access \'/_collection/{collection_name}/{key}\' : run in delete_data_by_id(), input data collection_name: [%s]' % collection_name)
        log.logger.debug('key: [%s]' % key)
        if not coldef.has_Coldef_schema(collection_name):
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail='Collection [ %s ] not found' % collection_name
            )
        ossmodelcls = importlib.import_module('ossmodels.' + collection_name.strip().lower())
        ossmodel = getattr(ossmodelcls, collection_name.strip().capitalize())()
        return getattr(ossmodel, 'delete' + collection_name.strip().capitalize())(key)

else:
    @app.post(prefix + "/_collection/{collection_name}",
              tags=["Data - Collection Level"],
              summary="Create one document.",
              description="",
              )
    async def post_data(collection_name: str, docpost: apimodel.DocumentBody,
                        current_user_role: bool = Depends(security.get_write_permission)):
        """
                    Parameters
                    - **collection_name** (path): **Required** - Name of the collection to perform operations on.
                    - **request body: Required**
                    ```
                        {
                         "data": [{"name":"jack","phone":"55789"}]  -- **Required** - Json formated fieldname-fieldvalue pair. ex: '[{"name":"jack","phone":"55789"}]'
                         }
                    ```
        """
        log.logger.debug(
            'Access \'/_collection/{collection_name}\' : run in post_data(), input data collection_name: [%s]' % collection_name)
        log.logger.debug('body data: [%s]' % docpost.json())
        if not coldef.has_Coldef_schema(collection_name):
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail='Collection [ %s ] not found' % collection_name
            )
        ossmodelcls = importlib.import_module('ossmodels.' + collection_name.strip().lower())
        ossmodel = getattr(ossmodelcls, collection_name.strip().capitalize())()
        log.logger.debug(json.loads(docpost.json())['data'])
        return getattr(ossmodel, 'create' + collection_name.strip().capitalize())(json.loads(docpost.json())['data'])

    @app.put(prefix + "/_collection/{collection_name}",
             tags=["Data - Collection Level"],
             summary="Update one document.",
             description="",
             deprecated=False
             )
    async def put_data(collection_name: str, docput: apimodel.DocumentBody,
                       current_user_role: bool = Depends(security.get_write_permission)):
        """
                Parameters
                - **collection_name** (path): **Required** - Name of the collection to perform operations on.
                - **request body: Required**
                ```
                    {
                     "data": [{"name":"jack","phone":"55789"}]  -- **Required** - Json formated fieldname-fieldvalue pair. ex: '[{"name":"jack","phone":"55789"}]'
                     }
                ```
        """
        log.logger.debug(
            'Access \'/_collection/{collection_name}\' : run in put_data(), input data collection_name: [%s]' % collection_name)
        log.logger.debug('body: [%s]' % docput.json())
        if not coldef.has_Coldef_schema(collection_name):
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail='Collection [ %s ] not found' % collection_name
            )
        ossmodelcls = importlib.import_module('ossmodels.' + collection_name.strip().lower())
        ossmodel = getattr(ossmodelcls, collection_name.strip().capitalize())()
        return getattr(ossmodel, 'update' + collection_name.strip().capitalize())(json.loads(docput.json())['data'])

    @app.delete(prefix + "/_collection/{collection_name}",
                tags=["Data - Collection Level"],
                summary="Delete one document.",
                description="",
                )
    async def delete_data(collection_name: str,
                          keystr: str = Header(None),
                          current_user_role: bool = Depends(security.get_write_permission)):
        """
            Parameters
            - **collection_name** (path): **Required** - Name of the collection to perform operations on.
            - **keystr** (header): Optional - Key of the document need to be deleted
        """
        log.logger.debug(
            'Access \'/_collection/{collection_name}\' : run in delete_data(), input data collection_name: [%s]' % collection_name)
        log.logger.debug('keystr: [%s]' % keystr)
        if not coldef.has_Coldef_schema(collection_name):
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail='Collection [ %s ] not found' % collection_name
            )
        ossmodelcls = importlib.import_module('ossmodels.' + collection_name.strip().lower())
        ossmodel = getattr(ossmodelcls, collection_name.strip().capitalize())()
        return getattr(ossmodel, 'delete' + collection_name.strip().capitalize())(keystr)

    @app.put(prefix + "/_collection/{collection_name}/{key}",
             tags=["Data - Document Level"],
             summary="Replace the content of one document by key.",
             description="",
             )
    async def put_data_by_id(collection_name: str, key: str,
                             docput: apimodel.DocumentBody,
                             current_user_role: bool = Depends(security.get_write_permission)):
        """
                Parameters
                - **collection_name** (path): **Required** - Name of the collection to perform operations on.
                - **key** (path): **Required** - The key of document
                - **request body: Required**
                ```
                    {
                     "data": [{"name":"jack","phone":"55789"}]  -- **Required** - Json formated fieldname-fieldvalue pair. ex: '[{"name":"jack","phone":"55789"}]'
                     }
                ```
        """
        log.logger.debug(
            'Access \'/_collection/{collection_name}/{key}\' : run in put_data_by_id(), input data collection_name: [%s]' % collection_name)
        log.logger.debug('body: [%s]' % docput)
        log.logger.debug('key: [%s]' % key)
        if not coldef.has_Coldef_schema(collection_name):
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail='Collection [ %s ] not found' % collection_name
            )
        ossmodelcls = importlib.import_module('ossmodels.' + collection_name.strip().lower())
        ossmodel = getattr(ossmodelcls, collection_name.strip().capitalize())()
        upjson = json.loads(docput.json())['data']
        upjson['_key'] = key
        return getattr(ossmodel, 'update' + collection_name.strip().capitalize())(upjson)

    @app.delete(prefix + "/_collection/{collection_name}/{key}",
                tags=["Data - Document Level"],
                summary="Delete one document by key.",
                description="",
                )
    async def delete_data_by_id(collection_name: str, key: str,
                                current_user_role: bool = Depends(security.get_write_permission)):

        """
                    Parameters
                    - **collection_name** (path): **Required** - Name of the collection to perform operations on.
                    - **key** (header): Optional - Key of the document need to be deleted
        """
        log.logger.debug(
            'Access \'/_collection/{collection_name}/{key}\' : run in delete_data_by_id(), input data collection_name: [%s]' % collection_name)
        log.logger.debug('key: [%s]' % key)
        if not coldef.has_Coldef_schema(collection_name):
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail='Collection [ %s ] not found' % collection_name
            )
        ossmodelcls = importlib.import_module('ossmodels.' + collection_name.strip().lower())
        ossmodel = getattr(ossmodelcls, collection_name.strip().capitalize())()
        return getattr(ossmodel, 'delete' + collection_name.strip().capitalize())(key)



