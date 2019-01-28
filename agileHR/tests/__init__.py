import unittest

def suite():
    return unittest.TestLoader().discover("agileHR.tests", pattern="*.py")