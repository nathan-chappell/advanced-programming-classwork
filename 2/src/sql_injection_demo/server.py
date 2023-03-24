"""
Simple sanic-server exposing a SQL injection vulnerability
"""

from typing import Literal

from sanic import Sanic
from sanic import Request
from sanic import json
from sanic.log import logger
from sanic.response import HTTPResponse
from sanic.views import HTTPMethodView

# from sql_injection_demo import app
from sql_injection_demo.models import User

app = Sanic.get_app("app")

# Endpoints

from sql_injection_demo.services import UserService


@app.post("/get-secrets")
async def get_user(request: Request) -> HTTPResponse:
    """Sql injection here"""
    service = UserService()
    json_body = request.json

    password = json_body.get("password", None)
    username = json_body.get("username", None)

    if username is None or password is None:
        return HTTPResponse("username and password required", 400)

    user = await service.get_user(username=username, password=password)
    if user is None:
        return HTTPResponse("incorrect login", 404)
    
    secrets = await service.get_secrets(username=username, password=password)

    return json({"secrets": secrets})


@app.put("/user")
async def put_user(request: Request) -> HTTPResponse:
    """Add user"""
    # get async session from request context
    # user service from context
    service = UserService()
    json_body = request.json

    username = json_body.get("username", None)
    password = json_body.get("password", None)
    secrets = json_body.get("secrets", None)

    if username is None or password is None:
        return HTTPResponse("username and password required", 400)

    user = await service.get_user(username=username, password=password)
    user_exists = await service.user_exists(username=username)

    logger.info(f"{user=} {user_exists=}")

    if user is None and user_exists:
        return HTTPResponse("invalid password", 400)

    await service.upsert_user(username=username, password=password, secrets=secrets)
    return HTTPResponse("okay", 200)


# middleware
