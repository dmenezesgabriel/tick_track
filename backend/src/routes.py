from sanic.response import json
from src.controllers.activity import DefaultActivity as Activity


def setup_routes(app):
    """
    Define routes
    :app:Receives a Sanic app instance
    """
    @app.route('/load-all', methods=['GET'])
    async def load_all(request):
        return json(Activity.load_all())

    @app.route('/load-today', methods=['GET'])
    async def load_today(request):
        return json(Activity.load_today())
