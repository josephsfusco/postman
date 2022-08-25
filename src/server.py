from flask import Flask, request
import threading
import time
import service
import security


app = Flask(__name__)

#########################################
#                                       #
#             AUTH SERVICE              #
#                                       #
#########################################

# Returns a bearer token for users who provide valid username and password
#
# body: username (email) {string}
# body: password {string}
# returns: bearer token {string}
@app.get("/authenticate")
def getAuthenticateUserController():
    body = dict(request.form)

    return {'token' : security.getAuthenticateUserService(body)}

# Returns True if bearer token is authenticated, False if not
@app.get("/authenticateToken")
def getAuthenticatetokenController():
    body = dict(request.form)

    return {'authenticated' : security.getAuthenticateTokenService(body)}



#########################################
#                                       #
#         CORE BUSINESS SERVICE         #
#                                       #
#########################################

# Returns data for users providing valid Bearer token
# 
# headers: Token {string}
# returns: data {dict} (json)
@app.get("/data")
def getDataController():
    headers = dict(request.headers)
    
    return {'data' : service.getDataService(headers)}




#########################################
#               TESTING                 #
#########################################

@app.get('/helloWorld')
def getHelloWorld():
    return "Hello World!"

@app.get("/allTokens")
def getAllTokensController():
    return security.Tokens




#########################################
#            APPLICATION                #
#########################################

def cleanupThread():
    while True:
        security.cleanUp()
        time.sleep(10)

if __name__ == "__main__":
    #cleaner = threading.Thread(target=cleanupThread)
    #cleaner.start()
    app.run(debug=True) #, host="0.0.0.0", port=80)%debug=True) #, host="0.0.0.0", port=80)%