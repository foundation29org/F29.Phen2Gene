import unittest

from Phen2GeneTests import *

suite = unittest.TestSuite()

suite.addTest(CalculationTests())

unittest.TextTestRunner(verbosity=2).run(suite)

