"""                _               
  __      _____| |__   _____  __
  \ \ /\ / / _ \ '_ \ / _ \ \/ /
   \ V  V /  __/ |_) |  __/>  <         @WebexDevs
    \_/\_/ \___|_.__/ \___/_/\_\

"""

# -*- coding:utf-8 -*-
from webbrowser import get
import requests
import json
import os
import jwt

from flask import Flask, render_template, request, session

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.secret_key = os.urandom(24)

clientID = "YOUR CLIENT ID HERE"
secretID = "YOUR CLIENT SECRET HERE"
redirectURI = "http://0.0.0.0:10060/oauth" #This could be different if you publicly expose this endpoint.

# Function to parse JWT
def parse_jwt(token):
    """
    Parse JWT token

    :param token: JWT token
    :return: Decoded payload
    """
    return jwt.decode(token, options={"verify_signature": False})

def user_info():
    accessToken = session['access_token']
    url = "https://webexapis.com/v1/userinfo"
    headers = {'accept': 'application/json', 'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + accessToken}
    req = requests.get(url=url, headers=headers)
    results = json.loads(req.text)
    return results
"""
Function Name : get_tokens
Description : This is a utility function that takes in the 
              Authorization Code as a parameter. The code 
              is used to make a call to the access_token end 
              point on the webex api to obtain a id_token to 
              be used to get user_info
"""
def get_tokens(code):
    print("function : get_tokens()")
    print("code:", code)
    #STEP 3 : use code in response from webex api to collect the code parameter
    #to obtain an access token or refresh token
    url = "https://webexapis.com/v1/access_token"
    headers = {'accept':'application/json','content-type':'application/x-www-form-urlencoded'}
    payload = ("grant_type=authorization_code&client_id={0}&client_secret={1}&"
                    "code={2}&redirect_uri={3}").format(clientID, secretID, code, redirectURI)
    req = requests.post(url=url, data=payload, headers=headers)
    results = json.loads(req.text)
    
    id_token = results["id_token"]
    access_token = results["access_token"]
    session['id_token'] = id_token 
    session['access_token'] = access_token

    print("ID Token stored in session : ", session['id_token'])
    print("Access Token stored in session : ", session['access_token'])
    return 

"""
Function Name : main_page
Description : when using the browser to access server at
              http://127/0.0.1:10060 this function will 
              render the html file index.html. That file 
              contains the button that kicks off step 1
              of the Oauth process with the click of the 
              grant button
"""
@app.route("/") 

def main_page():
    """Main Grant page"""
    return render_template("index.html")

"""
Function Name : oauth
Description : After the grant button is click from index.html
              and the user logs into thier Webex account, the 
              are redirected here as this is the html file that
              this function renders upon successful authentication
              is granted.html. else, the user is sent back to index.html
              to try again. This function retrieves the authorization
              code and calls get_tokens() for further API calls against
              the Webex API endpoints. 
"""
@app.route("/oauth") #Endpoint acting as Redirect URI.

def oauth():
    print("function : oauth()")
    """Retrieves oauth code to generate tokens for users"""
    state = request.args.get("state")
    print('state : ' + state)
    if state == '1234abcd':
        code = request.args.get("code") # STEP 2 : Capture value of the 
                                        # authorization code.
        print("OAuth code:", code)
        print("OAuth state:", state)
        get_tokens(code)
        claims = parse_jwt(session['id_token'])
        print('claims : ', claims)
        user = user_info()
        return render_template("user.html", claims = claims, user = user)
    else:
        return render_template("index.html")

if __name__ == '__main__':
    app.run("0.0.0.0", port=10060, debug=False)