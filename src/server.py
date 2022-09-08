#-----------------------------------------------
#       Core App & Service Controllers            
#-----------------------------------------------

from flask import Flask, request
import data_service as data
import authentication_service as auth
import threading
import time


app = Flask(__name__)

#-----------------------------------------------
#       Authenticaton Service            
#-----------------------------------------------

@app.get("/basicAuthentication")
def getBasicAuthenticationController():
    """ Returns a bearer token for users who provide valid username and password
    Args:
        body {dict}
            username (email) {string}
            password {string}
    Returns: 
        Response {Response}
    """
    body = dict(request.form)
    if 'username' not in body or 'password' not in body:
        return {'error' : 'Forbidden'}, 403
    
    return auth.getBasicAuthenticationService(body)

@app.get("/tokenAuthentication")
def getTokenAuthenticationController():
    """ Returns True if bearer token is authenticated, False if not 
    Args:
        body {dict}
            token {string}
    Returns:
        Response {Response}
    """

    body = dict(request.form)
    if 'token' not in body:
        return {'error' : 'Missing Token'}, 400

    return {'authenticated' : auth.getTokenAuthenticationService(body)}



#-----------------------------------------------
#       Core Business Service       
#-----------------------------------------------

@app.get("/data")
def getDataController():
    """Returns data for users providing valid Bearer token
    Args:
        headers {dict}
            Token {string}
    returns: 
        Response {Response}
    """
    headers = dict(request.headers)
    if 'Token' not in headers:
        return {'error' : 'Forbidden'}, 403

    return data.getDataService(headers)



#-----------------------------------------------
#       Testing                
#-----------------------------------------------

@app.get('/helloWorld')
def getHelloWorld():
    return "Hello World!"

@app.get("/allTokens")
def getAllTokensController():
    return {'count'  : len(auth.Tokens),
            'tokens' : auth.Tokens
           }



#-----------------------------------------------
#            APPLICATION                
#-----------------------------------------------

def cleanupThread():
    while True:
        auth.cleanUp()
        time.sleep(5)

if __name__ == "__main__":
    cleaner = threading.Thread(target=cleanupThread)
    cleaner.start()
    app.run(debug=False) 

