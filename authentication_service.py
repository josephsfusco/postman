import time
import random
import string




# Psudo In-Memory User Database 
# {'email': encrpted password}
Users = {
    'jsf.fusco@gmail.com' : 780, #PW: postman
    'hello@gmail.com' : 1094 #helloworld
}

Tokens = []

def getBasicAuthenticationService(body):
    """ Returns new token if username and password are known 
    Body: {dict}
        username {string}
        password {string}
    Returns: 
        Response {Response}
    """

    username = body['username']
    password_hash = getPasswordHash(body['password'])

    if username in Users:
        if Users[username] == password_hash:
            return {'token' : generateToken()}

    return {'error' : 'unauthorized'}, 401

def getTokenAuthenticationService(body):
    """Returns True if token is valid and not stale
    Returns:
        {bool}
    """

    token = body['token']

    if token in Tokens:
        print("token Found")
        tokenTimeStamp = int(token.split("-")[1])

        #tokens are valid for 30 seconds 
        if tokenTimeStamp+30 >= getSystemCurrentMoment():
            print("token still fresh")
            return True
    return False

def getSystemCurrentMoment():
    """Returns the systme current moment with Second precision
    Renturns: 
        {int}
    """

    print('system Current Moment')

    return int(time.time())

def getPrefix():
    """Returns a randomly generated token prefix
    Returns:
        {str}
    """
    return ''.join(random.sample(string.ascii_lowercase,4))

def generateToken():
    """ Returns new token after generation and storing in memeory
    Returns:
       token {string}
    """
    currentMoment = getSystemCurrentMoment()
    prefix = getPrefix()

    newToken = prefix + '-' + str(currentMoment)

    Tokens.append(newToken)
    return newToken

def getPasswordHash(password):
    """ Returns encyrpted password hash
    Returns:
        hash {int}
    """
    hash = 0
    for c in password:
        hash+=ord(c)
    print(hash)
    return hash+10

def cleanUp():
    """ Cleans stale keys
    Returns:
        None
    """
    systemCurrentMoment = getSystemCurrentMoment() 

    for t in Tokens:
        tokenTimeStamp = int(t.split('-')[1])
        if tokenTimeStamp+30 < systemCurrentMoment:
            print(f'Removing: {t}')
            Tokens.remove(t)
        break



    
