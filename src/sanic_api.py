import asyncio
import logging
from sanic import Sanic
from sanic.response import json
import src.api as api


_logger = logging.getLogger("Sanic")


app = Sanic(__name__)


@app.route("/load/activities", methods=["GET"])
async def load_activities(request):
    return json(api.load_activities())


@app.route("/", methods=["GET"])
async def index(request):
    return json("Hello world!")


def start():
    _logger.info("Starting")
    loop = asyncio.get_event_loop()
    server = app.create_server(
        host="0.0.0.0", port=8080, return_asyncio_server=True)
    loop.create_task(server)
