import os
VERIFY_MODE = os.getenv("VERIFY_MODE", "OFFLINE")
from jose import jwt
from jwt import PyJWKClient
import os
import urllib.request
import json

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL")
REALM = os.getenv('REALM')
CLIENT_ID = os.getenv('CLIENT_ID')
ISSUER = f"{KEYCLOAK_URL}/realms/{REALM}"
AUDIENCE = os.getenv('AUDIENCE','account')  # as per your token
JWKS_URL = f"{ISSUER}/protocol/openid-connect/certs"
import base64
import requests



class KeycloakOnlineDecoder:
    def __init__(self):
        print("ctor")


    def can_execute(self) -> bool:
        """
        Check if execution is permitted.
        """
        return VERIFY_MODE == "ONLINE"

    def execute(self, token):
        url = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/token/introspect"
        SHARED_SECRET = os.getenv('SHARED_SECRET')

        # 📤 Introspect request
        response = requests.post(
            url,
            data={'token': token},
            auth=(CLIENT_ID, SHARED_SECRET),
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )

        # 📥 Parse the response
        decoded_token = response.json()
        return decoded_token