import asyncio
from datetime import datetime
import logging
from sanic import Sanic
from sanic.response import json
import src.api as api


_logger = logging.getLogger("Sanic")


app = Sanic(__name__)


@app.route("/load-all", methods=["GET"])
async def load_all(request):
    activities_list = await api.load_all()
    return json(activities_list)


@app.route("/load-today", methods=["GET"])
async def load_today(request):
    today_activities_list = await api.load_today()
    return json(today_activities_list)


@app.route(
    "/load-range/<selected_start_date>/<selected_end_date>",
    methods=["GET", "POST"])
async def load_today(request, selected_start_date, selected_end_date):
    start_date = datetime.strptime(selected_start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(selected_end_date, "%Y-%m-%d").date()
    today_activities_list = await api.load_range(start_date, end_date)
    return json(today_activities_list)


@app.route("/", methods=["GET"])
async def index(request):
    return json("Hello world!")


def start():
    _logger.info("Starting")
    loop = asyncio.get_event_loop()
    server = app.create_server(
        host="0.0.0.0", port=8081, return_asyncio_server=True)
    loop.create_task(server)
