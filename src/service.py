import requests


def getDataService(headers):
    isAuthenticated = authenticateToken(headers)

    if isAuthenticated:
        return "Hello, Postman!"
    return "Invalid Token"

# Calls "Auth Service"
def authenticateToken(headers):
    hostname = headers['Host']
    token = headers['Token']

    response = requests.get('http://' + hostname + '/authenticateToken', data={
        'token' : token
    })

    return response.json()['authenticated']
