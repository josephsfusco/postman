# Overview
The purpose of this project is to create a simple HTTP Server which provices authentication 

## Getting Started
This project is deployed on Heroku at the following domain {domain}

public endpoints

  ``` 
  /basicAuthentication
     Request body: { 'username' : <username>,
                     'password' : <password>
     }
  
     response: {'token' : <bearer token>}
  ```
  
  ```
  /data
      headers: {'token' : <bearer token>}
      
      response: {'data' : <data>}
  ```
