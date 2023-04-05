import os
import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google_auth_httplib2 import AuthorizedHttp

# Load environment variables
client_id = os.environ["GOOGLE_CLIENT_ID"]
client_secret = os.environ["GOOGLE_CLIENT_SECRET"]

# Setup OAuth2 flow

def authenticate():
    flow = Flow.from_client_config(client_config = 
                                  {"web":{"client_id":client_id,
                                          "auth_uri":"https://accounts.google.com/o/oauth2/auth",
                                          "token_uri":"https://accounts.google.com/o/oauth2/token",
                                          "client_secret":client_secret,
                                          }}, 
                                  scopes = ["openid","https://www.googleapis.com/auth/userinfo.email","https://www.googleapis.com/auth/userinfo.profile"])
    flow.redirect_uri ="http://localhost:8501"
    return flow

def main():
            flow = authenticate()
            authorization_url, _ = flow.authorization_url(prompt='consent')
            st.write(f"Please login using following link: { authorization_url }")
            try:
                if "code" in st.experimental_get_query_params():
                    code = st.experimental_get_query_params()["code"][0]
                    print(f"the code is ",code)
                    flow.fetch_token(code=code)
                    session = flow.authorized_session()
                    person= session.get('https://www.googleapis.com/userinfo/v2/me').json()
                    print(person)
                    name= person["name"]
                    email= person["email"]
                    st.write(f"Welecome",{name,email})
            except Exception as e:
                print(e)

if __name__ == "__main__":
    main()

    
