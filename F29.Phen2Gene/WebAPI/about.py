from flask import current_app
from flask_restplus import Resource

from ._api import API

@API.route('/version')
class About(Resource):
    def get(self): return current_app.config['VERSION']

