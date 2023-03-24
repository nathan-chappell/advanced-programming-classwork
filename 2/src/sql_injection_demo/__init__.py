"""
Ensure proper importing and configuration

you can hit an endpoint from powershell like:

# normal request
Invoke-RestMethod 127.0.0.1:8000/get-secrets -Method Post -Body '{"username":"user1", "password":"password1"}'

# sql injection
Invoke-RestMethod 127.0.0.1:8000/get-secrets -Method Post -Body '{"username":"'' or true --", "password":"password1"}'

"""

import logging

from sanic import Request
from sanic import Sanic
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

app = Sanic("app")

import sql_injection_demo.server
