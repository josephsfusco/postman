#-----------------------------------------------
#       Core App & Service Controllers            
#-----------------------------------------------
from flask import Flask, request
import data_service
import authentication_service
import threading
import time


app = Flask(__name__)

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
    if 'username' not in body or 'password' not in body:
        return {'error' : 'Forbidden'}, 403 #400 bad request? look into this 
    
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
    print(body)
    if 'token' not in body:
        return {'error' : 'Missing Token'}, 400

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
    if 'Token' not in headers:
        return {'error' : 'Forbidden'}, 403

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

def cleanupThread():
    while True:
        authentication_service.cleanStaleTokens()
        time.sleep(5)

if __name__ == "__main__":
    reaper = threading.Thread(target=cleanupThread)
    reaper.start()
    app.run(debug=False) 

