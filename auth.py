import google
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
import json
from time import sleep

# Define the required scopes
scopes = [
  "https://www.googleapis.com/auth/userinfo.email",
  "https://www.googleapis.com/auth/firebase.database"
]

# Authenticate a credential with the service account
credentials = service_account.Credentials.from_service_account_file(
    "serviceAccountKey.json", scopes=scopes)

# Use the credentials object to authenticate a Requests session.
authed_session = AuthorizedSession(credentials)
response = authed_session.get(
    "https://nyxserver-bb04f.firebaseio.com/monitor.json")

testvar = json.loads(response.text)
print(testvar)

# Or, use the token directly, as described in the "Authenticate with an
# access token" section below. (not recommended)
request = google.auth.transport.requests.Request()
credentials.refresh(request)
access_token = credentials.token

print(access_token)

print(authed_session.patch("https://nyxserver-bb04f.firebaseio.com/monitor.json", data='{"temp": 90}')) #Save file to firebase

print(authed_session.request(
    'GET', 'https://nyxserver-bb04f.firebaseio.com/monitor'
))

response = authed_session.get("https://nyxserver-bb04f.firebaseio.com/monitor.json")

testvar = json.loads(response.text)
print(testvar)

def auth():
    # Define the required scopes
    scopes = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/firebase.database"
    ]

    # Authenticate a credential with the service account
    credentials = service_account.Credentials.from_service_account_file(
        "serviceAccountKey.json", scopes=scopes)

    # Use the credentials object to authenticate a Requests session.
    authed_session = AuthorizedSession(credentials)
    response = authed_session.get(
        "https://nyxserver-bb04f.firebaseio.com/monitor.json")

    testvar = json.loads(response.text)
    print(testvar)

    # Or, use the token directly, as described in the "Authenticate with an
    # access token" section below. (not recommended)
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    access_token = credentials.token

    print(access_token)

    print(authed_session.patch("https://nyxserver-bb04f.firebaseio.com/monitor.json", data='{"temp": 90}')) #Save file to firebase
