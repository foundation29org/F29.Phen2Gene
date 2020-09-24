import unittest

from ._common import *

from Phen2Gene import Phen2Gene

FOLDER = 'calc'

KBASE_PATH = os.environ.get('KBASE_PATH', '/kbase')

class Phen2GeneCalcTests(unittest.TestCase):
    def __init__(self):
        super().__init__(methodName='runTest')
        self.phen2gene = Phen2Gene(KBASE_PATH)

    def test_calc_empty(self):
        res = self.phen2gene.calculate([''])
        assert res == {}
        res = self.phen2gene.calculate(['', ''])
        assert res == {}

    def test_calc_unknown(self):
        res = self.phen2gene.calculate(['ABC:00000001'])
        assert res == {}
        res = self.phen2gene.calculate(['HP:0099999', 'HP:99999999'])
        assert res == {}
        HPOS = 'HP:0012758, ABC:00000001, HP:0005484, HP:0099999, HP:0002384, HP:0002373, HP:0002266, HP:0200134, HP:0002197, HP:0002133, HP:0002123, HP:0002121, HP:0000992, HP:0002059, HP:0100704, HP:0025356, HP:0001250, HP:0001337, HP:0006813, HP:0001270, HP:0001268, HP:0001263, HP:0001252, HP:0001251, HP:0011151, HP:0007334, HP:0000708, HP:0002353'
        res = self.phen2gene.calculate(HPOS.split(','), normalize=False, rows=20)
        assert file_equal(FOLDER, res, F'dravet.json')
        res = self.phen2gene.calculate(HPOS.split(','), normalize=True, rows=20)
        assert file_equal(FOLDER, res, F'dravet-norm.json')

    def test_calc_dravet(self): # SCN1A
        HPOS = 'HP:0012758, HP:0005484, HP:0002384, HP:0002373, HP:0002266, HP:0200134, HP:0002197, HP:0002133, HP:0002123, HP:0002121, HP:0000992, HP:0002059, HP:0100704, HP:0025356, HP:0001250, HP:0001337, HP:0006813, HP:0001270, HP:0001268, HP:0001263, HP:0001252, HP:0001251, HP:0011151, HP:0007334, HP:0000708, HP:0002353'
        res = self.phen2gene.calculate(HPOS.split(','), normalize=False, rows=20)
        assert file_equal(FOLDER, res, F'dravet.json')
        res = self.phen2gene.calculate(HPOS.split(','), normalize=True, rows=20)
        assert file_equal(FOLDER, res, F'dravet-norm.json')

    def test_calc_sotos(self): # SETD2 APC2 NSD1
        HPOS = 'HP:0001363, HP:0004375, HP:0002857, HP:0002970, HP:0000028, HP:0002664, HP:0001671, HP:0002119, HP:0002007, HP:0010978, HP:0000494, HP:0000486, HP:0000463'
        res = self.phen2gene.calculate(HPOS.split(','), normalize=False, rows=20)
        assert file_equal(FOLDER, res, F'sotos.json')
        res = self.phen2gene.calculate(HPOS.split(','), normalize=True, rows=20)
        assert file_equal(FOLDER, res, F'sotos-norm.json')

    def test_calc_west(self): # NTRK2 PHACTR1 PLCB1 PIGA ARX CNPY3 SCN2A ST3GAL3 GRIN2B GUF1 SIK1 SPTAN1 CDKL5 STXBP1 WDR45
        HPOS = 'HP:0002521, HP:0002376, HP:0012469, HP:0001336, HP:0011121, HP:0000707'
        res = self.phen2gene.calculate(HPOS.split(','), normalize=False, rows=20)
        assert file_equal(FOLDER, res, F'west.json')
        res = self.phen2gene.calculate(HPOS.split(','), normalize=True, rows=20)
        assert file_equal(FOLDER, res, F'west-norm.json')

    def test_calc_skraban(self): # WDR26
        HPOS = 'HP:0430028, HP:0002119, HP:0002079, HP:0002064, HP:0002019, HP:0000486, HP:0000463, HP:0000403, HP:0000293, HP:0000280, HP:0005338, HP:0005280, HP:0000347, HP:0040082, HP:0000646, HP:0001250, HP:0001290, HP:0011968, HP:0001344, HP:0001263, HP:0001249, HP:0000215, HP:0031936, HP:0000687, HP:0002136'
        res = self.phen2gene.calculate(HPOS.split(','), normalize=False, rows=20)
        assert file_equal(FOLDER, res, F'skraban.json')
        res = self.phen2gene.calculate(HPOS.split(','), normalize=True, rows=20)
        assert file_equal(FOLDER, res, F'skraban-norm.json')

    def runTest(self):
        self.test_calc_empty()
        self.test_calc_unknown()
        self.test_calc_dravet()
        self.test_calc_sotos()
        self.test_calc_west()
        self.test_calc_skraban()
