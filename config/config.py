#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: OSSGPAPI

from unipath import Path
from decouple import config


class Config(object):
    BASE_DIR = Path(__file__).parent
    config.encoding = 'utf-8'
    config.search_path = BASE_DIR

class Application_Config(Config):
    app_name = config('app_name', default = 'OSSGPAPI')
    app_version = config('app_version', default = 'v1.0.2')
    app_description = config('app_description', default = 'OSS Governance Platform API')
    app_prefix = config('app_prefix', default = '/api/v1')
    app_cors_origins = config('app_cors_origins', default = '*')
    app_service_model = config('app_service_model', default = 'Standalone') # Standalone|OpenReader|OpenWriter
    app_log_level = config('app_log_level', default = 'INFO')
    app_exception_detail = config('app_exception_detail', default = True, cast = bool)
    app_admin_use_https = config('app_admin_use_https', default = True, cast = bool)
    app_confirm_key = config('app_confirm_key', default = 'Confirmed')
    app_http_port = config('app_http_port', default = 6880, cast = int)
    app_https_port = config('app_https_port', default = 6843, cast = int)
    app_http_timeout = config('app_http_timeout', default = 3, cast = int)

class Schema_Config(Config):
    schema_cache_enabled = config('schema_cache_enabled', default = True, cast = bool)

class Query_Config(Config):
    query_limit_upset = config('query_limit_upset', default = 2000, cast = int)
    query_default_limit = config('query_default_limit', default = 20, cast = int)
    query_default_offset = config('query_default_offset', default = 0, cast = int)

class Security_Config(Config):
    security_key = config('security_key', default = '47051d5e3bafcfcba3c80d6d1119a7adf78d2967a8972b00af1ea231ca61f589')
    security_algorithm = config('security_algorithm', default = 'HS256')
    access_token_expire_minutes = config('access_token_expire_minutes', default = 30, cast = int)

class Database_Config(Config):
    db_uri = config('db_uri', default = 'mysql+pymysql://suser:passw0rd@192.168.122.151:3306/ossgovdb')
    aragodb_url = config('aragodb_url', default = 'http://192.168.122.151:8529')

class Connection_Config(Config):
    con_pool_size = config('con_pool_size', default = 20, cast = int)
    con_max_overflow = config('con_max_overflow', default = 5, cast = int)
    con_pool_use_lifo = config('con_pool_use_lifo', default = True, cast = bool)
    con_pool_pre_ping = config('con_pool_pre_ping', default = True, cast = bool)
    con_pool_recycle = config('con_pool_recycle', default = 3600, cast = int)

class Admin_Config(Config):
    DEBUG = config('DEBUG', default = False, cast = bool)
    SECRET_KEY = config('SECRET_KEY', default = 'bgt56yhn@Passw0rd')
    SESSION_COOKIE_HTTPONLY = config('SESSION_COOKIE_HTTPONLY', default = True, cast = bool)
    REMEMBER_COOKIE_HTTPONLY = config('REMEMBER_COOKIE_HTTPONLY', default = True, cast = bool)
    REMEMBER_COOKIE_DURATION = config('REMEMBER_COOKIE_DURATION', default = 3600, cast = int)

# Load all possible configurations
app_config = {
    'Application_Config': Application_Config,
    'Schema_Config': Schema_Config,
    'Query_Config': Query_Config,
    'Security_Config': Security_Config,
    'Database_Config': Database_Config,
    'Connection_Config': Connection_Config,
    'Admin_Config': Admin_Config
}
def recofig():
    Application_Config = None
    Schema_Config = None
    Query_Config = None
    Security_Config = None
    Database_Config = None
    Connection_Config = None
    Admin_Config = None
    app_config = {}
    app_config['Application_Config'] = Application_Config
    app_config['Schema_Config'] = Schema_Config
    app_config['Query_Config'] = Query_Config
    app_config['Security_Config'] = Security_Config
    app_config['Database_Config'] = Database_Config
    app_config['Connection_Config'] = Connection_Config
    app_config['Admin_Config'] = Admin_Config




if __name__ == '__main__':
    #print(dir(app_config['Application_Config']))
    #print(app_config['Application_Config'].__dict__)
    #print(app_config['Application_Config'].app_description)
    #print(app_config['Schema_Config'].schema_fetch_tables)
    #print(app_config['Database_Config'].db_uri)
    #print(app_config['Database_Config'].db_exclude_tablespaces)
    #print(app_config['Schema_Config'].schema_fetch_tables)
    recofig()
    print(app_config['Application_Config'].__dict__)
    print(app_config['Schema_Config'].__dict__)
    print(app_config['Query_Config'].__dict__)
    print(app_config['Security_Config'].__dict__)
    print(app_config['Database_Config'].__dict__)
    print(app_config['Connection_Config'].__dict__)
    print(app_config['Admin_Config'].__dict__)