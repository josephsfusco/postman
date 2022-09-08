#--------------------------------------------
#       Basic Unit Testing
#--------------------------------------------

import unittest
import sys
 
sys.path.append('.')
from src import authentication_service as auth


class AuthTestCase(unittest.TestCase):
    def test_get_basic_auth_service_passing (self):
        body = {'username' : 'jsf.fusco@gmail.com',
                'password' : 'postman'
        }
                        
        expected = 'abcd-0123456789'
        result = auth.getBasicAuthenticationService(body)['token']
        self.assertEqual(len(result), len(expected))
        self.assertEqual(result.index('-'), expected.index('-'))
    
    def test_get_basic_auth_service_failure (self):
        body = {'username' : 'jsf.fusco@gmail.com',
                'password' : '123'
        }
        expected = {'error' : 'unauthorized'}, 401
        self.assertEqual(auth.getBasicAuthenticationService(body), expected)    
    

    def test_get_token_authentication_service_passing(self):
        #need to use an authentic key here
        token = auth.generateToken()
        auth.Tokens.append(token)
        body = {'token' : token}
        expected = True
        self.assertEqual(auth.getTokenAuthenticationService(body), expected)
    
    def test_get_token_authentication_service_failure(self):
        auth.Tokens.append(3456)
        body = {'token' : 6543}
        expected = False
        self.assertEqual(auth.getTokenAuthenticationService(body), expected)

    
    def test_get_password_hash(self):
        password = 'helloworld'
        expected = 1094

        self.assertEqual(auth.getPasswordHash(password), expected)


if __name__ == '__main__':
    unittest.main()
