from sanic.response import json

from src.controllers.activity import DefaultActivity as Activity


def setup_routes(app):
    """
    Define routes
    :app:Receives a Sanic app instance
    """
    @app.route('/activities/all', methods=['GET'])
    async def load_all(request):
        return json(Activity.load_all())

    @app.route('/activities/today', methods=['GET'])
    async def load_today(request):
        return json(Activity.load_today())

    @app.route('/activities/date.range', methods=['POST'])
    async def load_date_range(request):
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        return json(Activity.load_range(start_date, end_date))

    @app.route('/activities/search', methods=['POST'])
    async def search_activity(request):
        text = request.form.get('text')
        return json(Activity.full_text_search(text))
