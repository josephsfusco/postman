from urllib.error import HTTPError
import log
import requests

HTTP_UNAUTHORIZED = 401

def getData(headers): 
    """ Mock service which returns data to the user if authenticated
    In practice this would enter a business logic flow which could return any data for an authorized user
    Args:
        headers {dict}
    Returns:
        Response {Response}
    """
    isAuthenticated = authenticateToken(headers)
    log.debug('data_service.getData', isAuthenticated)
    
    if isAuthenticated:
        return {'data' : 'Hello, Postman!'}

    return {'error' : 'Unauthorized'}, HTTP_UNAUTHORIZED

def authenticateToken(headers):
    log.debug('data_service.authenticateToken - headers' , headers)
    
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
        log.debug('data_service.authenticateToken - response' , response.json())
        if response.status_code == 200: 
            isAuthenticated = response.json()['authenticated']

    except KeyError as e:
        log.error(e, 'data_service.authenticateToken - Missing Required Arguments')
    
    except:
        log.error('Error caught but not handled', 'data_service.authenticateToken')
    
    return isAuthenticated
