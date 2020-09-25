import unittest

from ._common import *

from Phen2Gene import Phen2Gene

FOLDER = 'query'

KBASE_PATH = os.environ.get('KBASE_PATH', '/kbase')

class Phen2GeneQueryTests(unittest.TestCase):
    def __init__(self):
        super().__init__(methodName='runTest')
        self.phen2gene = Phen2Gene(KBASE_PATH)

    def test_validate(self):
        res = self.phen2gene.validate(None)
        assert res == {}
        res = self.phen2gene.validate('')
        assert res == {}
        res = self.phen2gene.validate('ABC:0000')
        assert res == {'ABC:0000': {'id': 'ABC:0000', 'status': 'invalid'}}, '  ' + str(res)
        res = self.phen2gene.validate('HP_9999999')
        assert res == {'HP_9999999': {'id': 'HP:9999999', 'status': 'unknown'}}, '  ' + str(res)

        HPOS = 'HP_0030422, HP_0030152, HP_0045013'
        res = self.phen2gene.validate(HPOS.split(','))
        assert file_equal(FOLDER, res, F'validation-obs.json')
        res = self.phen2gene.validate([None, '', 'XY:0000000', 'HP:9999999', 'HP_0030152', 'HP_0030152', 'HP:0000010'])
        assert file_equal(FOLDER, res, F'validation-mix.json')

    def test_build_query(self):
        res = self.phen2gene.build_query(None)
        assert res == {}
        res = self.phen2gene.build_query('')
        assert res == {}
        res = self.phen2gene.build_query('ABC:0000')
        assert res == {'ABC:0000': {'id': 'ABC:0000', 'status': 'invalid', 'target': None}}, '  ' + str(res)
        res = self.phen2gene.build_query('HP_9999999')
        assert res == {'HP_9999999': {'id': 'HP:9999999', 'status': 'unknown', 'target': None}}, '  ' + str(res)

        HPOS = 'HP_0030422, HP_0030152, HP_0045013'
        res = self.phen2gene.build_query(HPOS.split(','))
        assert file_equal(FOLDER, res, F'query-obs.json')
        res = self.phen2gene.build_query([None, '', 'XY:0000000', 'HP:9999999', 'HP_0030152', 'HP_0030152', 'HP:0000010'])
        assert file_equal(FOLDER, res, F'query-mix.json')

    def test_calc_empty(self):
        res = self.phen2gene.calculate([''])
        assert res == {}
        res = self.phen2gene.calculate(['', ''])
        assert res == {}

    def runTest(self):
        self.test_validate()
        self.test_build_query()
        self.test_calc_empty()
