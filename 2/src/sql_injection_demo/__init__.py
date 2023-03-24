"""
Ensure proper importing and configuration
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
