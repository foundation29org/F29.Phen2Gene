import unittest

from Phen2GeneTests import *

suite = unittest.TestSuite()

#suite.addTest(CalculationTests())
suite.addTest(Phen2GeneQueryTests())
suite.addTest(Phen2GeneCalcTests())

unittest.TextTestRunner(verbosity=2).run(suite)

