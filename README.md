# OSSGPAPI
OSS Governance Platform API

uvicorn main:app --host 0.0.0.0 --port 6880 --reload --no-server-header --no-date-header --workers 1

uvicorn main:app --host 0.0.0.0 --port 6880 --no-server-header --no-date-header --workers 1

hypercorn -c config/hypercorn.py -w 1 --reload main:app
