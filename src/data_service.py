from urllib.error import HTTPError
import requests


def getDataService(headers):
    """ Mock service which returns data to the user if authenticated
    Args:
        headers {dict}
    Returns:
        Response {Response}
    """
    isAuthenticated = authenticateToken(headers)
    
    if isAuthenticated:
        return {'data' : 'Hello, Postman!'}

    return {'error' : 'Unauthorized'}, 401

def authenticateToken(headers):
    """ Requests authentication status of token from 
    Args:
        headers {dict}
            Host
            Token 
    Returns:
        isAuthenticated {bool} 
    """
    isAuthenticated = False

    try:
        hostname = headers['Host']
        token = headers['Token']

        response = requests.get('http://' + hostname + '/tokenAuthentication', data={
            'token' : token
        })
        print(f'response {response.json()}')
        if response.status_code == 200: 
            isAuthenticated = response.json()['authenticated']

    except KeyError as e:
        print(e, 'Missing Required Arguments')
    
    except HTTPError as e:
        print(e)
    
    return isAuthenticated
