from flask import Flask, request
import threading
import time
import data_service as data
import authentication_service as auth


app = Flask(__name__)

#########################################
#             AUTH SERVICE              #
#########################################

@app.get("/basicAuthentication")
def getBasicAuthenticationController():
    """ Returns a bearer token for users who provide valid username and password
    body:
        username (email) {string}
        password {string}
    returns: 
        bearer token {string}
    """
    body = dict(request.form)

    return {'token' : auth.getBasicAuthenticationService(body)}

@app.get("/tokenAuthentication")
def getTokenAuthenticationController():
    """ Returns True if bearer token is authenticated, False if not """

    body = dict(request.form)

    return {'authenticated' : auth.getTokenAuthenticationService(body)}



#########################################
#         CORE BUSINESS SERVICE         #
#########################################

@app.get("/data")
async def getDataController():
    """Returns data for users providing valid Bearer token

    headers: 
        Token {string}
    returns: 
        data {dict} (json)
    """

    headers = dict(request.headers)
    
    return {'data' : data.getDataService(headers)}




#########################################
#               TESTING                 #
#########################################

@app.get('/helloWorld')
def getHelloWorld():
    return "Hello World!"

@app.get("/allTokens")
def getAllTokensController():
    return auth.Tokens




#########################################
#            APPLICATION                #
#########################################

def cleanupThread():
    while True:
        auth.cleanUp()
        time.sleep(10)

if __name__ == "__main__":
    #cleaner = threading.Thread(target=cleanupThread)
    #cleaner.start()
    app.run(debug=True) #, host="0.0.0.0", port=80)%debug=True) #, host="0.0.0.0", port=80)%