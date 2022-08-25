import time

# {'email' : 'encrypted password'}
Users = {
    "jsf.fusco@gmail.com" : 212, #PW: 1234
    "hello@gmail.com" : 345
}

Tokens = []

# look up user name, hash password to see if given hash matches stored hash
# if match, generate token
def getAuthenticateUserService(body):
    username = body['username']
    password_hash = getPasswordHash(body['password'])
    #logging.debug(f'PASSWORD: {password_hash}')

    if username in Users:
        if Users[username] == password_hash:
            return generateToken()

    return denied()

# Returns True if token is valid and not stale
#
# {bool}
def getAuthenticateTokenService(body):
    print(body)
    token = body['token']

    if token in Tokens:
        print("token Found")
        
        #get system current moment and remove decimals
        systemCurrentMoment = int(time.time()) 

        #tokens are valid for 60 seconds 
        if (int(token)+600) >= int(systemCurrentMoment):
            print("token still fresh")
            return True
    return False

# Returns "Credentials Denied"
#
# {string}
def denied():
    return "Credentials Denied"

# Returns new token after generation and storing in memeory
#
# token {string}
def generateToken():
    # I realize the double casting is sub optomal, I explored alternate ways of accomplishing this.
    # in order to maintain contenuity with authenticateToken() I made a design decision to go with this approcach.
    # Happy to discuss more in the code review

    # using int() to remove deicmals
    newToken = int(time.time())

    # casting to string to return to the user
    newToken = str(newToken)
    Tokens.append(newToken)
    return newToken

# Returns encyrpted password hash
# 
# hash {int}    
def getPasswordHash(password):
    hash = 0
    for c in password:
        hash+=ord(c)
    return hash+10

def cleanUp():
    #print("CLEAN UP!")
    #get system current moment and remove decimals
    systemCurrentMoment = int(time.time()) 

    for t in Tokens:

        if int(t)+10 < systemCurrentMoment:
            Tokens.remove(t)
        break
    

#def printit():
#  
# 
#  threading.Timer(5.0, printit).start()
#   print 

# printit()
