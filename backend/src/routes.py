from sanic.response import json
from src.controllers.activity import DefaultActivity as Activity
from src.controllers.metrics import metrics_bundle


def setup_routes(app):
    """
    Define routes
    :app:Receives a Sanic app instance
    """
    @app.route('/activities/all', methods=['POST'])
    async def load_all(request):
        drill_level = request.form.get('drill_level', 'main_description')
        return json(metrics_bundle(Activity.load_all(), drill_level))

    @app.route('/activities/today', methods=['POST'])
    async def load_today(request):
        drill_level = request.form.get('drill_level', 'main_description')
        return json(metrics_bundle(Activity.load_today(), drill_level))

    @app.route('/activities/date.range', methods=['POST'])
    async def load_date_range(request):
        drill_level = request.form.get('drill_level', 'main_description')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        return json(metrics_bundle(
            Activity.load_range(start_date, end_date), drill_level))

    @app.route('/activities/search', methods=['POST'])
    async def search_activity(request):
        drill_level = request.form.get('drill_level', 'main_description')
        start_date = request.form.get('start_date', '1900-01-01')
        end_date = request.form.get('end_date', '3000-01-01')
        text = request.form.get('text')
        return json(metrics_bundle(Activity.full_text_search(
            text, start_date, end_date), drill_level))
