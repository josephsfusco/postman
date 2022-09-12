#-----------------------------------------------
#       Core App & Service Controllers            
#-----------------------------------------------
#from http.client import BAD_REQUEST
from flask import Flask, request
import authentication_service
import data_service
import log
import threading
import time

app = Flask(__name__)

HTTP_FORBIDDEN  = 403
HTTP_BADREQUEST = 400


#-----------------------------------------------
#       Authenticaton Controller            
#-----------------------------------------------

@app.post("/login") 
def getBearerToken():
    """ Returns a bearer token for users who provide valid username and password
    Args:
        body {dict}
            username (email) {string}
            password {string}
    Returns: 
        Response {Response}
    """
    body = dict(request.form)
    url = request.url #TODO get url from request
    log.debug('server.getBearerToken', body)

    if 'username' not in body or 'password' not in body:
        return {'error' : 'Forbidden'}, HTTP_FORBIDDEN  
    
    return authentication_service.getBearerToken(body) 

@app.get("/validateToken")
def isTokenValid(): 
    """ Returns True if bearer token is authenticated, False if not 
    Args:
        body {dict}
            token {string}
    Returns:
        Response {Response}
    """

    body = dict(request.form)
    log.debug('server.isTokenValid', body)

    if 'token' not in body:
        return {'error' : 'Missing Token'}, HTTP_BADREQUEST

    return {'authenticated' : authentication_service.isTokenValid(body)} 



#-----------------------------------------------
#       Core Business Controller       
#-----------------------------------------------

@app.get("/data")
def getData(): 
    """Returns data for users providing valid Bearer token
    Args:
        headers {dict}
            Token {string}
    returns: 
        Response {Response}
    """
    headers = dict(request.headers)
    log.debug('server.getData', headers)

    if 'Token' not in headers:
        return {'error' : 'Forbidden'}, HTTP_FORBIDDEN

    return data_service.getData(headers)



#-----------------------------------------------
#       Testing                
#-----------------------------------------------

@app.get('/helloWorld')
def getHelloWorld():
    return "Hello World!"

@app.get("/allTokens")
def getAllTokens():
    return {'count'  : len(authentication_service.BearerTokens),
            'tokens' : authentication_service.BearerTokens
           }



#-----------------------------------------------
#            APPLICATION                
#-----------------------------------------------

def reaperThread():
    while True:
        authentication_service.cleanDeadTokens()
        time.sleep(15)

if __name__ == "__main__":
    reaper = threading.Thread(target=reaperThread)
    reaper.start()
    app.run(debug=False) 

