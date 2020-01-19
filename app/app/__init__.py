from flask import Flask, Blueprint
from app.views.view import view

app = Flask(__name__)


app.register_blueprint(view)
