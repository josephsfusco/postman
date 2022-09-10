#--------------------------------------------
#       Basic Unit Testing
#--------------------------------------------

import unittest
import sys
 
sys.path.append('.')
from src import authentication_service


class AuthTestCase(unittest.TestCase):
    def test_getBearerToken_passing (self):
        body = {'username' : 'jsf.fusco@gmail.com',
                'password' : 'postman'
        }
                        
        expected = 'abcd-0123456789'
        result = authentication_service.getBearerToken(body)['token']
        self.assertEqual(len(result), len(expected))
        self.assertEqual(result.index('-'), expected.index('-'))
    
    def test_getBearerToken_failure (self):
        body = {'username' : 'jsf.fusco@gmail.com',
                'password' : '123'
        }

        expected = {'error' : 'unauthorized'}, 401
        result = authentication_service.getBearerToken(body)
        self.assertEqual(result, expected)    
    

    def test_isTokenValid_passing(self):
        #need to use an authentic key here
        token = authentication_service.generateToken()
        authentication_service.Tokens.append(token)
        body = {'token' : token}

        result = authentication_service.isTokenValid(body)
        expected = True
        self.assertEqual(result, expected)
    
    def test_isTokenValid_failure(self):
        authentication_service.Tokens.append(3456)
        body = {'token' : 6543}

        result = authentication_service.isTokenValid(body)
        expected = False
        self.assertEqual(result, expected)

    
    def test_getPasswordHash(self):
        password = 'helloworld'

        result = authentication_service.getPasswordHash(password)
        expected = 1094
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
