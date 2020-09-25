import unittest

from Phen2GeneTests import *

suite = unittest.TestSuite()

suite.addTest(Phen2GeneQueryTests())
suite.addTest(Phen2GeneCalcTests())
suite.addTest(Phen2GeneExecTests())

unittest.TextTestRunner(verbosity=2).run(suite)

