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
from core.govbase import Govbase
from env.environment import Environment
from ossmodel.users import Users
from sysmodel.coldef import Coldef
from util import log
import traceback
import simplejson as json
from core.systembase import Systembase

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

log.logger.debug('services_model=%s' % services_model)

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
    # Init databases
    log.logger.info(os.getenv('OSSGPAPI_APP_NAME') + ' Check and Init databases ....')
    sysbase = Systembase()
    sysbase.initgovbase()
    sysbase.inituserbase()
    # Init system define
    log.logger.info(os.getenv('OSSGPAPI_APP_NAME') + ' Check and Init system define ....')
    # TODO add govbase define and init

    # Init system User
    log.logger.info(os.getenv('OSSGPAPI_APP_NAME') + ' Check and Init system users ....')
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

# =========================== sys api ===========================
@app.get(prefix + "/_sysdef/sysdefcount/{syscol_name}",
         tags=["System Define - Collection Level"],
         summary="Retrieve system definitions count.",
         description="",
         )
async def get_sysdef_count(syscol_name: str, current_user_role: bool = True if services_model >= 1 else Depends(
    security.get_super_permission)):
    """
            This describes the document count
    """
    log.logger.debug(
        'Access \'/_sysdef/sysdefcount/{syscol_name}\' : run in get_sysdef_count, input syscol_name: [ %s ]' % syscol_name)
    govbase = Govbase().db
    if not govbase.has_collection(syscol_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Collection [ %s ] not found' % syscol_name
        )
    sysmodelcls = importlib.import_module('sysmodel.' + syscol_name.strip().lower())
    sysmodel = getattr(sysmodelcls, syscol_name.strip().capitalize())()
    return getattr(sysmodel, 'get_' + syscol_name.strip().capitalize() + '_count')()


@app.get(prefix + "/_sysdef/sysdefnames/{syscol_name}",
         tags=["System Define - Collection Level"],
         summary="Retrieve system definitions name list.",
         description="",
         )
async def get_sysdef_names(syscol_name: str, current_user_role: bool = True if services_model >= 1 else Depends(
    security.get_super_permission)):
    """
            Parameters
            - **syscol_name** (path): **Required** - Name of the collection to perform operations on.
    """
    log.logger.debug(
        'Access \'/_sysdef/sysdefnames/{syscol_name}\' : run in get_sysdef_names, input syscol_name: [ %s ]' % syscol_name)
    govbase = Govbase().db
    if not govbase.has_collection(syscol_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Collection [ %s ] not found' % syscol_name
        )
    sysmodelcls = importlib.import_module('sysmodel.' + syscol_name.strip().lower())
    sysmodel = getattr(sysmodelcls, syscol_name.strip().capitalize())()
    return getattr(sysmodel, 'get_all_' + syscol_name.strip().capitalize() + '_names')()


@app.get(prefix + "/_sysdef/{syscol_name}/{sysdoc_name}",
         tags=["System Define - Document Level"],
         summary="Retrieve one system definition document by name.",
         description="",
         )
async def get_sysdef_byname(syscol_name: str, sysdoc_name: str,
                            current_user_role: bool = True if services_model >= 1 else Depends(
    security.get_super_permission)):
    """
            Parameters
            - **syscol_name** (path): **Required** - Name of the collection to perform operations on.
            - **sysdoc_name** (path): **Required** - Name of the document to perform operations on.
    """
    log.logger.debug(
        'Access \'/_sysdef/{syscol_name}/{sysdoc_name}\' : run in get_sysdef_byname, input syscol_name: [ %s ]' % syscol_name)
    log.logger.debug(
        'Access \'/_sysdef/{syscol_name}/{sysdoc_name}\' : run in get_sysdef_byname, input sysdoc_name: [ %s ]' % sysdoc_name)
    govbase = Govbase().db
    if not govbase.has_collection(syscol_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Collection [ %s ] not found' % syscol_name
        )
    sysmodelcls = importlib.import_module('sysmodel.' + syscol_name.strip().lower())
    sysmodel = getattr(sysmodelcls, syscol_name.strip().capitalize())()
    docexist = getattr(sysmodel, 'existed_' + syscol_name.strip().capitalize())(sysdoc_name)
    if not docexist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Document [ %s ] not found' % sysdoc_name
        )
    return getattr(sysmodel, 'get_' + syscol_name.strip().capitalize() + '_byname')(sysdoc_name)


@app.get(prefix + "/_sysdef/{syscol_name}/{key}",
         tags=["System Define - Document Level"],
         summary="Retrieve one system definition document by key.",
         description="",
         )
async def get_sysdef_bykey(syscol_name: str, key: str,
                           current_user_role: bool = True if services_model >= 1 else Depends(
    security.get_super_permission)):
    """
            Parameters
            - **syscol_name** (path): **Required** - Name of the collection to perform operations on.
            - **key** (path): **Required** - key of the document to perform operations on.
    """
    log.logger.debug(
        'Access \'/_sysdef/{syscol_name}/{key}\' : run in get_sysdef_bykey, input syscol_name: [ %s ]' % syscol_name)
    log.logger.debug(
        'Access \'/_sysdef/{syscol_name}/{key}\' : run in get_sysdef_bykey, input key: [ %s ]' % key)
    govbase = Govbase().db
    if not govbase.has_collection(syscol_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Collection [ %s ] not found' % syscol_name
        )
    sysmodelcls = importlib.import_module('sysmodel.' + syscol_name.strip().lower())
    sysmodel = getattr(sysmodelcls, syscol_name.strip().capitalize())()
    return getattr(sysmodel, 'get_' + syscol_name.strip().capitalize() + '_bykey')(key)


@app.get(prefix + "/_sysdef/{syscol_name}",
         tags=["System Define - Collection Level"],
         summary="Retrieve one or more system definition documents. ",
         description="",
         )
async def query_sysdef(syscol_name: str, filter: str = Header(None), filteror: str = Header(None),
                       sort: str = Header(None),
                       limit: int = Header(int(os.getenv('OSSGPAPI_QUERY_DEFAULT_LIMIT')), gt=0,
                                           le=int(os.getenv('OSSGPAPI_QUERY_LIMIT_UPSET'))),
                       offset: int = Header(int(os.getenv('OSSGPAPI_QUERY_DEFAULT_OFFSET')), gt=-1),
                       current_user_role: bool = True if services_model >= 1 else Depends(
    security.get_read_permission)):
    """
                    Parameters
                    - **syscol_name** (path): **Required** - Name of the collection to perform operations on.
                    - **"filter"** (header): "string",  -- Optional - SQL-like filter to limit the records to retrieve. ex: name=="qname1", name=="qname2"
                    - **"filteror"** (header): "string",  -- Optional - SQL-like filter Parameter to limit the records to retrieve. ex: name=="qname1"', name=="qname2"
                    - **"sort** (header)": "string",  -- Optional - SQL-like order containing field and direction for filter results. ex: 'phone_number ASC'
                    - **"limit"** (header): 0,  -- Optional - Set to limit the filter results.
                    - **"offset"** (header): 0,  -- Optional - Set to offset the filter results to a particular record count.
    """
    log.logger.debug(
        'Access \'/_sysdef/{syscol_name}\' : run in query_sysdef(), input data syscol_name: [%s]' % syscol_name)
    queryjson = {}
    queryjson['filter'] = filter.split(',') if filter is not None else None
    queryjson['filteror'] = filteror.split(',') if filteror is not None else None
    queryjson['sort'] = sort
    queryjson['limit'] = limit
    queryjson['offset'] = offset
    log.logger.debug('queryjson: [%s]' % queryjson)
    govbase = Govbase().db
    if not govbase.has_collection(syscol_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Collection [ %s ] not found' % syscol_name
        )
    sysmodelcls = importlib.import_module('sysmodel.' + syscol_name.strip().lower())
    sysmodel = getattr(sysmodelcls, syscol_name.strip().capitalize())()
    return getattr(sysmodel, 'query_' + syscol_name.strip().capitalize())(queryjson)


# =========================== oss api ===========================

@app.get(prefix + "/_collection/documentcount/{collection_name}",
         tags=["OSS Data - Collection Level"],
         summary="Retrieve document count. ",
         description="",
         )
async def get_document_count(collection_name: str,
                             current_user_role: bool = True if services_model >= 1 else Depends(
    security.get_read_permission)):
    """
                    Parameters
                    - **collection_name** (path): **Required** - Name of the collection to perform operations on.
    """
    log.logger.debug(
        'Access \'/_collection/documentcount/{collection_name}\' : run in get_document_count(), input collection_name: [%s]' % collection_name)
    if not coldef.has_Coldef_schema(collection_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Collection [ %s ] not found' % collection_name
        )
    ossmodelcls = importlib.import_module('ossmodel.' + collection_name.strip().lower())
    ossmodel = getattr(ossmodelcls, collection_name.strip().capitalize())()
    return getattr(ossmodel, 'get' + collection_name.strip().capitalize() + 'count')()


@app.get(prefix + "/_collection/{collection_name}",
         tags=["OSS Data - Collection Level"],
         summary="Retrieve one or more documents. ",
         description="",
         )
async def query_document(collection_name: str, filter: str = Header(None), filteror: str = Header(None),
                         sort: str = Header(None),
                         limit: int = Header(int(os.getenv('OSSGPAPI_QUERY_DEFAULT_LIMIT')), gt=0,
                                             le=int(os.getenv('OSSGPAPI_QUERY_LIMIT_UPSET'))),
                         offset: int = Header(int(os.getenv('OSSGPAPI_QUERY_DEFAULT_OFFSET')), gt=-1),
                         current_user_role: bool = True if services_model >= 1 else Depends(
    security.get_read_permission)):
    """
                    Parameters
                    - **collection_name** (path): **Required** - Name of the collection to perform operations on.
                    - **"filter"** (header): "string",  -- Optional - SQL-like filter to limit the records to retrieve. ex: name=="qname1", name=="qname2"
                    - **"filteror"** (header): "string",  -- Optional - SQL-like filter Parameter to limit the records to retrieve. ex: name=="qname1"', name=="qname2"
                    - **"sort** (header)": "string",  -- Optional - SQL-like order containing field and direction for filter results. ex: 'phone_number ASC'
                    - **"limit"** (header): 0,  -- Optional - Set to limit the filter results.
                    - **"offset"** (header): 0,  -- Optional - Set to offset the filter results to a particular record count.
    """
    log.logger.debug(
        'Access \'/_collection/{collection_name}\' : run in query_document(), input data collection_name: [%s]' % collection_name)
    queryjson = {}
    queryjson['filter'] = filter.split(',') if filter is not None else None
    queryjson['filteror'] = filteror.split(',') if filteror is not None else None
    queryjson['sort'] = sort
    queryjson['limit'] = limit
    queryjson['offset'] = offset
    log.logger.debug('queryjson: [%s]' % queryjson)
    if not coldef.has_Coldef_schema(collection_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Collection [ %s ] not found' % collection_name
        )
    ossmodelcls = importlib.import_module('ossmodel.' + collection_name.strip().lower())
    ossmodel = getattr(ossmodelcls, collection_name.strip().capitalize())()
    return getattr(ossmodel, 'query' + collection_name.strip().capitalize())(queryjson)


@app.post(prefix + "/_collection/_query/{collection_name}",
          tags=["OSS Data - Collection Level"],
          summary="Retrieve one or more documents. ",
          description="", )
async def query_document_post(collection_name: str, querybody: apimodel.CollectionQueryBody,
                              current_user_role: bool = True if services_model >= 1 else Depends(
    security.get_read_permission)):
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
        'Access \'/_collection/_query{collection_name}/\' : run in query_document_post(), input data collection_name: [%s]' % collection_name)
    log.logger.debug('querybody: [%s]' % querybody.json())
    if not coldef.has_Coldef_schema(collection_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Collection [ %s ] not found' % collection_name
        )
    ossmodelcls = importlib.import_module('ossmodel.' + collection_name.strip().lower())
    ossmodel = getattr(ossmodelcls, collection_name.strip().capitalize())()
    return getattr(ossmodel, 'query' + collection_name.strip().capitalize())(querybody)


@app.get(prefix + "/_collection/{collection_name}/{key}",
         tags=["OSS Data - Document Level"],
         summary="Retrieve one Document by key.",
         description="",
         )
async def get_document_by_key(collection_name: str, key: str, relation: str = Header('false'),
                              current_user_role: bool = True if services_model >= 1 else Depends(
    security.get_read_permission)):
    log.logger.debug(
        'Access \'/_collection/{collection_name}/{key}\' : run in get_document_by_key(), input data collection_name: [%s] with relation :[%s]' % (collection_name,relation))
    log.logger.debug('key: [%s]' % key)
    if not coldef.has_Coldef_schema(collection_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Collection [ %s ] not found' % collection_name
        )
    ossmodelcls = importlib.import_module('ossmodel.' + collection_name.strip().lower())
    ossmodel = getattr(ossmodelcls, collection_name.strip().capitalize())()
    return getattr(ossmodel, 'get' + collection_name.strip().capitalize() + 'bykey')(key,relation)


'''Write API'''

# =========================== sysdef api ===========================
@app.post(prefix + "/_sysdef/{syscol_name}",
          tags=["System Define - Collection Level"],
          summary="Create one system definition document.",
          description="",
          )
async def post_sysdef(syscol_name: str, docpost: apimodel.DocumentBody,
                      current_user_role: bool = True if services_model >= 2 else Depends(security.get_write_permission)):
    """
                Parameters
                - **syscol_name** (path): **Required** - Name of the collection to perform operations on.
                - **request body: Required**
                ```
                    {
                     "data": [{"name":"jack","phone":"55789"}]  -- **Required** - Json formated fieldname-fieldvalue pair. ex: '[{"name":"jack","phone":"55789"}]'
                     }
                ```
    """
    log.logger.debug(
        'Access \'/_sysdef/{syscol_name}\' : run in post_sysdef(), input data collection_name: [%s]' % syscol_name)
    log.logger.debug('body data: [%s]' % docpost.json())
    govbase = Govbase().db
    if not govbase.has_collection(syscol_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Collection [ %s ] not found' % syscol_name
        )
    sysmodelcls = importlib.import_module('sysmodel.' + syscol_name.strip().lower())
    sysmodel = getattr(sysmodelcls, syscol_name.strip().capitalize())()
    # log.logger.debug(json.loads(docpost.json())['data'])
    return getattr(sysmodel, 'create_' + syscol_name.strip().capitalize())(json.loads(docpost.json())['data'])


@app.put(prefix + "/_sysdef/{syscol_name}",
         tags=["System Define - Collection Level"],
         summary="Update one system definition document.",
         description="",
         deprecated=False
         )
async def put_sysdef(syscol_name: str, docput: apimodel.DocumentBody,
                     current_user_role: bool = True if services_model >= 2 else Depends(security.get_write_permission)):
    """
            Parameters
            - **syscol_name** (path): **Required** - Name of the collection to perform operations on.
            - **request body: Required**
            ```
                {
                 "data": [{"name":"jack","phone":"55789"}]  -- **Required** - Json formated fieldname-fieldvalue pair. ex: '[{"name":"jack","phone":"55789"}]'
                 }
            ```
    """
    log.logger.debug(
        'Access \'/_sysdef/{syscol_name}\' : run in put_sysdef(), input data collection_name: [%s]' % syscol_name)
    log.logger.debug('body: [%s]' % docput.json())
    govbase = Govbase().db
    if not govbase.has_collection(syscol_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Collection [ %s ] not found' % syscol_name
        )
    sysmodelcls = importlib.import_module('sysmodel.' + syscol_name.strip().lower())
    sysmodel = getattr(sysmodelcls, syscol_name.strip().capitalize())()
    return getattr(sysmodel, 'update_' + syscol_name.strip().capitalize())(json.loads(docput.json())['data'])


@app.delete(prefix + "/_sysdef/{syscol_name}",
            tags=["System Define - Collection Level"],
            summary="Delete one system definition document.",
            description="",
            )
async def delete_sysdef(syscol_name: str,
                        keystr: str = Header(None),
                        current_user_role: bool = True if services_model >= 2 else Depends(security.get_write_permission)):
    """
        Parameters
        - **syscol_name** (path): **Required** - Name of the collection to perform operations on.
        - **keystr** (header): - Key of the document need to be deleted
    """
    log.logger.debug(
        'Access \'/_collection/{collection_name}\' : run in delete_document(), input data collection_name: [%s]' % syscol_name)
    log.logger.debug('keystr: [%s]' % keystr)
    govbase = Govbase().db
    if not govbase.has_collection(syscol_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Collection [ %s ] not found' % syscol_name
        )
    sysmodelcls = importlib.import_module('sysmodel.' + syscol_name.strip().lower())
    sysmodel = getattr(sysmodelcls, syscol_name.strip().capitalize())()
    return getattr(sysmodel, 'delete_' + syscol_name.strip().capitalize())(keystr)


@app.put(prefix + "/_sysdef/{syscol_name}/{key}",
         tags=["System Define - Document Level"],
         summary="Replace the content of one system definition document by key.",
         description="",
         )
async def put_sysdef_by_key(syscol_name: str, key: str,
                            docput: apimodel.DocumentBody,
                            current_user_role: bool = True if services_model >= 2 else Depends(security.get_write_permission)):
    """
            Parameters
            - **syscol_name** (path): **Required** - Name of the collection to perform operations on.
            - **key** (path): **Required** - The key of document
            - **request body: Required**
            ```
                {
                 "data": [{"name":"jack","phone":"55789"}]  -- **Required** - Json formated fieldname-fieldvalue pair. ex: '[{"name":"jack","phone":"55789"}]'
                 }
            ```
    """
    log.logger.debug(
        'Access \'/_sysdef/{syscol_name}/{key}\' : run in put_sysdef_by_key(), input data collection_name: [%s]' % syscol_name)
    log.logger.debug('body: [%s]' % docput)
    log.logger.debug('key: [%s]' % key)
    govbase = Govbase().db
    if not govbase.has_collection(syscol_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Collection [ %s ] not found' % syscol_name
        )
    sysmodelcls = importlib.import_module('sysmodel.' + syscol_name.strip().lower())
    sysmodel = getattr(sysmodelcls, syscol_name.strip().capitalize())()
    upjson = json.loads(docput.json())['data']
    upjson['_key'] = key
    return getattr(sysmodel, 'update_' + syscol_name.strip().capitalize())(upjson)


@app.delete(prefix + "/_sysdef/{syscol_name}/{key}",
            tags=["System Define - Document Level"],
            summary="Delete one system definition document by key.",
            description="",
            )
async def delete_sysdef_by_key(syscol_name: str, key: str,
                               current_user_role: bool = True if services_model >= 2 else Depends(security.get_write_permission)):
    """
                Parameters
                - **syscol_name** (path): **Required** - Name of the collection to perform operations on.
                - **key** (path): **Required** - The key of document need to be deleted
    """
    log.logger.debug(
        'Access \'/_sysdef/{syscol_name}/{key}\' : run in delete_sysdef_by_key(), input data collection_name: [%s]' % syscol_name)
    log.logger.debug('key: [%s]' % key)
    govbase = Govbase().db
    if not govbase.has_collection(syscol_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Collection [ %s ] not found' % syscol_name
        )
    sysmodelcls = importlib.import_module('sysmodel.' + syscol_name.strip().lower())
    sysmodel = getattr(sysmodelcls, syscol_name.strip().capitalize())()
    return getattr(sysmodel, 'delete_' + syscol_name.strip().capitalize())(key)


# =========================== oss api ===========================

@app.post(prefix + "/_collection/{collection_name}",
          tags=["OSS Data - Collection Level"],
          summary="Create one document.",
          description="",
          )
async def post_document(collection_name: str, docpost: apimodel.DocumentBody,
                        current_user_role: bool = True if services_model >= 2 else Depends(security.get_write_permission)):
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
        'Access \'/_collection/{collection_name}\' : run in post_document(), input data collection_name: [%s]' % collection_name)
    log.logger.debug('body data: [%s]' % docpost.json())
    if not coldef.has_Coldef_schema(collection_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Collection [ %s ] not found' % collection_name
        )
    ossmodelcls = importlib.import_module('ossmodel.' + collection_name.strip().lower())
    ossmodel = getattr(ossmodelcls, collection_name.strip().capitalize())()
    # log.logger.debug(json.loads(docpost.json())['data'])
    return getattr(ossmodel, 'create' + collection_name.strip().capitalize())(json.loads(docpost.json())['data'])


@app.put(prefix + "/_collection/{collection_name}",
         tags=["OSS Data - Collection Level"],
         summary="Update one document.",
         description="",
         deprecated=False
         )
async def put_document(collection_name: str, docput: apimodel.DocumentBody,
                       current_user_role: bool = True if services_model >= 2 else Depends(security.get_write_permission)):
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
        'Access \'/_collection/{collection_name}\' : run in put_document(), input data collection_name: [%s]' % collection_name)
    log.logger.debug('body: [%s]' % docput.json())
    if not coldef.has_Coldef_schema(collection_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Collection [ %s ] not found' % collection_name
        )
    ossmodelcls = importlib.import_module('ossmodel.' + collection_name.strip().lower())
    ossmodel = getattr(ossmodelcls, collection_name.strip().capitalize())()
    return getattr(ossmodel, 'update' + collection_name.strip().capitalize())(json.loads(docput.json())['data'])


@app.delete(prefix + "/_collection/{collection_name}",
            tags=["OSS Data - Collection Level"],
            summary="Delete one document.",
            description="",
            )
async def delete_document(collection_name: str,
                          keystr: str = Header(None),
                          current_user_role: bool = True if services_model >= 2 else Depends(security.get_write_permission)):
    """
        Parameters
        - **collection_name** (path): **Required** - Name of the collection to perform operations on.
        - **keystr** (header): **Required** - Key of the document need to be deleted
    """
    log.logger.debug(
        'Access \'/_collection/{collection_name}\' : run in delete_document(), input data collection_name: [%s]' % collection_name)
    log.logger.debug('keystr: [%s]' % keystr)
    if not coldef.has_Coldef_schema(collection_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Collection [ %s ] not found' % collection_name
        )
    ossmodelcls = importlib.import_module('ossmodel.' + collection_name.strip().lower())
    ossmodel = getattr(ossmodelcls, collection_name.strip().capitalize())()
    return getattr(ossmodel, 'delete' + collection_name.strip().capitalize())(keystr)


@app.put(prefix + "/_collection/{collection_name}/{key}",
         tags=["OSS Data - Document Level"],
         summary="Replace the content of one document by key.",
         description="",
         )
async def put_document_by_key(collection_name: str, key: str,
                              docput: apimodel.DocumentBody,
                              current_user_role: bool = True if services_model >= 2 else Depends(security.get_write_permission)):
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
        'Access \'/_collection/{collection_name}/{key}\' : run in put_document_by_key(), input data collection_name: [%s]' % collection_name)
    log.logger.debug('body: [%s]' % docput)
    log.logger.debug('key: [%s]' % key)
    if not coldef.has_Coldef_schema(collection_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Collection [ %s ] not found' % collection_name
        )
    ossmodelcls = importlib.import_module('ossmodel.' + collection_name.strip().lower())
    ossmodel = getattr(ossmodelcls, collection_name.strip().capitalize())()
    upjson = json.loads(docput.json())['data']
    upjson['_key'] = key
    return getattr(ossmodel, 'update' + collection_name.strip().capitalize())(upjson)


@app.delete(prefix + "/_collection/{collection_name}/{key}",
            tags=["OSS Data - Document Level"],
            summary="Delete one document by key.",
            description="",
            )
async def delete_document_by_key(collection_name: str, key: str,
                                 current_user_role: bool = True if services_model >= 2 else Depends(security.get_write_permission)):
    """
                Parameters
                - **collection_name** (path): **Required** - Name of the collection to perform operations on.
                - **key** (path): **Required** - The key of document need to be deleted
    """
    log.logger.debug(
        'Access \'/_collection/{collection_name}/{key}\' : run in delete_document_by_key(), input data collection_name: [%s]' % collection_name)
    log.logger.debug('key: [%s]' % key)
    if not coldef.has_Coldef_schema(collection_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Collection [ %s ] not found' % collection_name
        )
    ossmodelcls = importlib.import_module('ossmodel.' + collection_name.strip().lower())
    ossmodel = getattr(ossmodelcls, collection_name.strip().capitalize())()
    return getattr(ossmodel, 'delete' + collection_name.strip().capitalize())(key)
