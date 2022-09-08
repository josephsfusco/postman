#--------------------------------------------
#       Basic Unit Testing
#--------------------------------------------  

import unittest
import sys

sys.path.append('.')
sys.path.append('./src')
from src import server


class Testdata(unittest.TestCase):
    def test_basic_authentication_controller(self):
        expected = server.getBasicAuthenticationController()
        result = None
        self.assertEqual(result, expected)

    
if __name__ == '__main__':
    unittest.main()