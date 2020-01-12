import asyncio
import logging
from sanic import Sanic
import src.api as api


_logger = logging.getLogger("Sanic")


app = Sanic(__name__)


@app.route("/load/activities", methods=["GET"])
async def load_activities():
    return json(api.load_activities())


def start():
    _logger.info("Starting")
    loop = asyncio.get_event_loop()
    server = app.create_server(host="0.0.0.0", port=8080, debug=False)
    loop.create_task(server)
