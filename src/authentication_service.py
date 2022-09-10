import time
import random
import string

# Psudo In-Memory User Database 
# {'email': encrpted password}
Users = {
    'jsf.fusco@gmail.com' : 780,    #PW: postman
    'hello@gmail.com' : 1094        #PW: helloworld
}

class BearerToken: 
    def __init__(self) -> None:
        self.key = generateKey()
        self.ttl = getSystemCurrentMoment()+30
        self.refreshCount = 0

# {'key': Token}
BearerTokens = {}
#LRU least recently used 

def getBearerToken(body):
    """ Returns new token if username and password are known 
    Args:
        body {dict}
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
        print("token Found")
        
        #tokens are valid for 30 seconds 
        if BearerTokens[key].ttl >= getSystemCurrentMoment():
            reinfalteToken(key)
            print("token still fresh")
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
    #sample: asdf-asdf-asdf-asdf
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
    token = BearerTokens.pop(key)
    
    token.ttl = getSystemCurrentMoment()+30
    token.refreshCount+=1

    BearerTokens[key] = token

    


#--------------------------------------------
#       Reaper Function
#--------------------------------------------

def cleanStaleTokens():
    """ Cleans stale tokens from cache
    Returns:
        None
    """
    systemCurrentMoment = getSystemCurrentMoment() 

    #print(f'bearer Tokens {BearerTokens}')
    staleTokens = []
    for t in BearerTokens.items():
        key = t[1].key
        ttl = t[1].ttl
        print(f'TOKENS {key}, {ttl}')
        if ttl < systemCurrentMoment:
            staleTokens.append(key)
            print(f'Removing: {key}')
    for s in staleTokens:
        BearerTokens.pop(s)
        



    
