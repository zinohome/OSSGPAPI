#!/usr/bin/env python3
# -*- coding: utf-8 -*-

loglevel = "debug"
workers = 4
bind = "0.0.0.0:6843"
insecure_bind = "0.0.0.0:6880"
graceful_timeout = 120
worker_class = "trio"
keepalive = 5
errorlog = "/Users/zhangjun/PycharmProjects/OSSGPAPI/log/hypercorn_error.log"
accesslog = "/Users/zhangjun/PycharmProjects/OSSGPAPI/log/hypercorn_access.log"
keyfile = "/Users/zhangjun/PycharmProjects/OSSGPAPI/cert/key.pem"
certfile = "/Users/zhangjun/PycharmProjects/OSSGPAPI/cert/cert.pem"