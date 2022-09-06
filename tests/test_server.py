# Basic Unit Testing

import unittest

class Testdata(unittest.TestCase):
    def test_basic_authentication_controller(self):
        self.assertEqual(None, None)

    def test_token_authentication_controller(self):
        self.assertEqual(None, None)

    def test_data_controller(self):
        self.assertEqual(None,None)

if __name__ == '__main__':
    unittest.main()