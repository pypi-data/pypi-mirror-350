import unittest

class TestPackage(unittest.TestCase):

    def test_import(self):
        from rgevolve.wet_3.flavio._version import __version__
        self.assertIsInstance(__version__, str)

