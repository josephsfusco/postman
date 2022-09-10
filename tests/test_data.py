#--------------------------------------------
#       Basic Unit Testing
#--------------------------------------------

import unittest
import sys
from mock import patch
from unittest import mock

sys.path.append('.')
from src import data_service


class Testdata(unittest.TestCase):

    @mock.patch('src.data_service.authenticateToken', return_value=True)
    def test_getData_passing(self, authenticateToken):
        result = data_service.getData({})['data']
        expected = 'Hello, Postman!'

        self.assertEqual(result, expected)
    
    @mock.patch('src.data_service.authenticateToken', return_value=False)
    def test_getData_failure(self, authenticateToken):
        result = data_service.getData({})[0]['error']
        expected = 'Unauthorized'

        self.assertEqual(result, expected)
    

if __name__ == '__main__':
    unittest.main()

