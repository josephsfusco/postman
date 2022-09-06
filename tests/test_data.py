#Basic unit testing
import unittest

class Testdata(unittest.TestCase):
    def test_data_service_passing(self):
        self.assertEqual(None, None)
    def test_data_service_failure(self):
        self.assertEqual(None, None)


    def test_authenticate_token(self):
        #mockRequest here
        self.assertEqual(None, None)


if __name__ == '__main__':
    unittest.main()

