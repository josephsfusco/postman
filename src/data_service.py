from urllib.error import HTTPError
from requests.models import Response

import requests



def getDataService(headers):
    isAuthenticated = authenticateToken(headers)


    if isAuthenticated:
        
        return "Hello, Postman!"
    return "Invalid Token"

# Calls "Auth Service"
def authenticateToken(headers):
    isAuthenticated = False
    try:
        hostname = headers['Host']
        token = headers['Token']

        response = requests.get('http://' + '/tokenAuthentication', data={
            'token' : token
        })

        isAuthenticated = response.json()['authenticated']
        
    except KeyError as e:
        print(e, 'Missing Required Arguments')
    
    except HTTPError as e:
        print(e)
    except:
        print('NAME ERROR')


    return isAuthenticated
