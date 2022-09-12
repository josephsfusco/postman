from data_service import authenticateToken
import log
import random
import string
import time

USERNAME = 'username'
PASSWORD = 'password'

HTTP_UNAUTHORIZED = 401

DEFAULT_TIMEOUT = 30


# Psudo In-Memory User Database 
# {'email': encrpted password}
Users = {
    'jsf.fusco@gmail.com' : 780,    #PW: postman
    'hello@gmail.com' : 1094        #PW: helloworld
}

# {'key': Token}
BearerTokens = {}
#LRU 

class BearerToken: 
    def __init__(self) -> None:
        self.key = generateKey()
        self.ttl = getSystemCurrentMoment() + DEFAULT_TIMEOUT #CONFIGUREABLE  #tokens are valid for 30 seconds 
        self.refreshCount = 0
        self.originalIssueTime = 0
 

def getBearerToken(body):
    """ Returns new token if username and password are known 
    Args:
        body {dict}
            username {string}
            password {string}
    Returns: 
        Response {Response}
    """

    username = body[USERNAME]
    password_hash = getPasswordHash(body[PASSWORD])

    if username in Users:
        if Users[username] == password_hash:
            return {'token' : generateToken()}

    return {'error' : 'unauthorized'}, HTTP_UNAUTHORIZED 

def isTokenValid(body): 
    """Returns True if token is valid and not stale
    Args:
        body {dict}
            token {string}
    Returns:
        {bool}
    """

    key = body['token']

    if key in BearerTokens:
        log.debug('authentication_service.isTokenValid','Token found')
        
        if BearerTokens[key].ttl >= getSystemCurrentMoment():
            reinfalteToken(key) #openclosed principal Slid solid 
            log.debug('authentication_service.isTokenValid','token still fresh')
            return True
    return False

def getSystemCurrentMoment():
    """Returns the systme current moment with Second precision
    Renturns: 
        {int}
    """
    return int(time.time())

def generateKeyChunk():
    """Returns a randomly generated token chunk
    Returns:
        {str}
    """
    return ''.join(random.sample(string.ascii_letters,4))

def generateKey():
    """Returns a key
    sample: asdf-asdf-asdf-asdf
    Returns:
        {str}
    """
    
    return '-'.join([generateKeyChunk() for i in range(4)])
    
def generateToken():
    """ Create a new Token Object and inserts it into the dictionary Tokens 
    using the Token key as the key in the dictionary
    Returns:
       token {string}
    """
    bearerToken = BearerToken()

    BearerTokens[bearerToken.key] = bearerToken
    return bearerToken.key

def getPasswordHash(password):
    """Hashes and returnsuser provided password for verification
    Args:
        password {string}
    Returns:
        hash {int}
    """
    hash = 0
    for c in password:
        hash+=ord(c)
    return hash+10

def reinfalteToken(key):
    """
    Reinflating token TTL, incrementing resetCount and moving it to the top of the list
    Args:
        token {str}
    Returns:
        None
    """
    token = BearerTokens[key]
    log.debug('authentication_service.reinflateToken - Original TTL:', token.ttl)
    token.ttl = getSystemCurrentMoment() + DEFAULT_TIMEOUT
    token.refreshCount+=1
    log.debug('authentication_service.reinflateToken - Reinflated TTL:', token.ttl)
    

    #BearerTokens[key] = token

    


#--------------------------------------------
#       Reaper Function
#--------------------------------------------

def cleanDeadTokens():
    """ Cleans stale tokens from cache
    Returns:
        None
    """
    systemCurrentMoment = getSystemCurrentMoment() 

    log.debug('authentication_service.cleanStaleTokens - Count:', len(BearerTokens))
    
    deadTokens = []
    for t in BearerTokens.items():
        key, ttl = t[1].key, t[1].ttl
        log.debug('authentication_service.cleanStaleTokens', (key, ttl))
        
        if ttl < systemCurrentMoment:
            deadTokens.append(key)
            log.debug('authentication_service.cleanStaleTokens - Removing Key', key)
    
    for s in deadTokens:
        BearerTokens.pop(s)
        



    
