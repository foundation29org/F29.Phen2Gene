import os
import json

from flask import current_app, request
from flask_restplus import Resource

from ._api import API

from Phen2Gene import Phen2Gene

KBASE_PATH = os.environ.get('KBASE_PATH', '/kbase')

phen2gene = Phen2Gene(KBASE_PATH)

@API.doc(params={
    'weight_model': {'description': 'methods to merge gene scores (sk, ic, w, u, s)', 'in': 'query', 'default': 'sk'},
    'normalize': {'description': 'normalize score', 'in': 'query', 'type': 'bool', 'default': True},
    'rows': {'description': 'number of rows', 'in': 'query', 'type': 'int', 'default': 100}
    })
@API.route('/calc')
class Calculate(Resource):
    def __init__(self, api=None):
        super().__init__(api=api)

    @API.doc(params={ 'hpos': {'description': 'list of HPO IDs', 'in': 'query'} })
    def get(self):
        model = request.args.get('weight_model') or 'sk'
        normalize = not (str(request.args.get('normalize')).lower() == 'false')
        rows = int(request.args.get('rows') or 100)
        hpos = request.args.get('hpos')
        hpos = [hpo.strip() for hpo in hpos.split(',')]
        return phen2gene.execute(hpos, weight_model=model, normalize=normalize, rows=rows)

    @API.doc(params={ 'hpos': {'description': 'list of HPO IDs', 'in': 'body'} })
    def post(self):
        model = request.args.get('weight_model') or 'sk'
        normalize = not (str(request.args.get('normalize')).lower() == 'false')
        rows = int(request.args.get('rows') or 100)
        data = request.data
        if data:
            hpos = json.loads(request.data)
            return phen2gene.execute(hpos, weight_model=model, normalize=normalize, rows=rows)
        return {}
