from sanic.response import json
import logging
from src.models.activity import Activity
from src.controllers.metrics import metrics_bundle


_logger = logging.getLogger("Routes")


def setup_routes(app):
    """
    Define routes
    :app:Receives a Sanic app instance
    """

    @app.route("/activities/all", methods=["POST"])
    async def load_all(request):
        data = request.json
        drill_level = data.get("drill_level", "main_description")
        return json(metrics_bundle(Activity.load_all(), drill_level))

    @app.route("/activities/today", methods=["POST"])
    async def load_today(request):
        data = request.json
        drill_level = data.get("drill_level", "main_description")
        return json(metrics_bundle(Activity.load_today(), drill_level))

    @app.route("/activities/date.range", methods=["POST"])
    async def load_date_range(request):
        data = request.json
        drill_level = data.get("drill_level", "main_description")
        start_date = data.get("start_date", "1900-01-01")
        end_date = data.get("end_date", "3000-01-01")
        return json(
            metrics_bundle(
                Activity.load_range(start_date, end_date), drill_level
            )
        )

    @app.route("/activities/search", methods=["POST"])
    async def search_activity(request):
        data = request.json
        drill_level = data.get("drill_level", "main_description")
        start_date = data.get("start_date", "1900-01-01")
        end_date = data.get("end_date", "3000-01-01")
        text = data.get("text")
        return json(
            metrics_bundle(
                Activity.full_text_search(text, start_date, end_date),
                drill_level,
            )
        )
