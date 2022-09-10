from urllib.error import HTTPError
import requests


def getData(headers): 
    """ Mock service which returns data to the user if authenticated
    In practice this would enter a business logic flow which could return any data for an authorized user
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
    print(headers)
    """ Requests authentication status of token from Authentication service
    Returns true if token is valid 
    Args:
        headers {dict}
            Host {string}
            Token {string}
    Returns:
        isAuthenticated {bool} 
    """
    isAuthenticated = False

    try:
        hostname = headers['Host']
        token = headers['Token']

        response = requests.get('http://' + hostname + '/validateToken', data={
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
