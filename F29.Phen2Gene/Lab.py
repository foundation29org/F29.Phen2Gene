import os

from Phen2GeneTests import *

from Phen2Gene import Phen2Gene

KBASE_PATH = os.environ.get('KBASE_PATH', '/kbase')

pg = Phen2Gene(KBASE_PATH)
ppf(pg.obsoletes)

