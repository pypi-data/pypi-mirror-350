import os
VERIFY_MODE = os.getenv("VERIFY_MODE", "OFFLINE")
from jose import jwt
from jwt import PyJWKClient
import os
import urllib.request
import json

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL")
REALM = os.getenv('REALM')
ISSUER = f"{KEYCLOAK_URL}/realms/{REALM}"
AUDIENCE = os.getenv('AUDIENCE','account')  # as per your token
JWKS_URL = f"{ISSUER}/protocol/openid-connect/certs"
import base64

def get_jwt_header(token: str) -> dict:
    header_b64 = token.split('.')[0]
    header_b64 += '=' * (-len(header_b64) % 4)  # pad base64 if needed
    decoded = base64.urlsafe_b64decode(header_b64)
    return json.loads(decoded)

def extract_roles(payload):
    try:
        return payload['realm_access']['roles']
    except KeyError:
        return []


def get_public_key(token):
    try:
        jwk_client = PyJWKClient(JWKS_URL)
        signing_key = jwk_client.get_signing_key_from_jwt(token)
        return signing_key.key
    except Exception as e:
        raise Exception(f"Unable to fetch Keycloak signing key: {e}")

class CustomPyJWKClient(PyJWKClient):
    def fetch_data(self):
        req = urllib.request.Request(
            self.uri,
            headers={"User-Agent": "Mozilla/5.0"}  # Prevent 403 from WAFs
        )
        with urllib.request.urlopen(req) as response:
            raw = response.read()
            try:
                return json.loads(raw)  # ✅ parse JSON here
            except json.JSONDecodeError as e:
                raise ValueError(
                    f"Failed to decode JSON from JWKS endpoint. Raw response: {raw[:300]}"
                ) from e

class KeycloakOfflineDecoder:
    def __init__(self):
        print("ctor")


    def can_execute(self) -> bool:
        """
        Check if execution is permitted.
        """
        return VERIFY_MODE == "OFFLINE"

    def execute(self, token):
        header = get_jwt_header(token)
        alg = header.get("alg")
        decoded_token = {}
        if alg == "HS512":
            SHARED_SECRET = os.getenv('SHARED_SECRET')
            decoded_token = jwt.decode(
                token,
                SHARED_SECRET,
                algorithms=[alg],
                options={"verify_aud": False}
            )
        elif alg == "RS256" or "ES256":
            jwk_client = CustomPyJWKClient(JWKS_URL)

            # jwk_client = PyJWKClient(JWKS_URL)
            signing_key = jwk_client.get_signing_key_from_jwt(token)

            decoded_token = jwt.decode(
                token,
                signing_key.key,
                algorithms=[alg],
                audience=AUDIENCE,
                issuer=ISSUER,
                options={"verify_exp": True}
            )

        return decoded_token