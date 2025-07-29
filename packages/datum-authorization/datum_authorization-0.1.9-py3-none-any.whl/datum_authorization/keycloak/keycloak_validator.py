from functools import wraps
import os
import base64
import json
KEYCLOAK_URL = os.getenv("KEYCLOAK_URL")
REALM = os.getenv('REALM')
ISSUER = f"{KEYCLOAK_URL}/realms/{REALM}"
AUDIENCE = os.getenv('AUDIENCE','account')  # as per your token
JWKS_URL = f"{ISSUER}/protocol/openid-connect/certs"
VERIFY_MODE = os.getenv("VERIFY_MODE", "OFFLINE")
from decoder.offline_decoder import KeycloakOfflineDecoder
from decoder.online_decoder import KeycloakOnlineDecoder

handlers = [KeycloakOfflineDecoder(), KeycloakOnlineDecoder()]
def get_jwt_header(token: str) -> dict:
    header_b64 = token.split('.')[0]
    header_b64 += '=' * (-len(header_b64) % 4)  # pad base64 if needed
    decoded = base64.urlsafe_b64decode(header_b64)
    return json.loads(decoded)

def keycloak_token_required(issuer, audience):

    def decorator(func):
        @wraps(func)
        def wrapper(event, context, *args, **kwargs):
            try:
                auth_header = event["headers"].get("Authorization", "")
                if not auth_header.startswith("Bearer "):
                    raise Exception("Missing or invalid Authorization header")

                token = auth_header.split(" ")[1]
                handler = next(filter(lambda x: x.can_execute(), handlers), None)
                if handler == None:
                    raise Exception("Authentication type not supported")
                decoded_token = handler.execute(token)
                event["decoded_token"] = decoded_token  # Pass it along

                queryStringParameters = event.get('queryStringParameters', {})
                pathParameters = event.get('pathParameters',{})
                stageVariables = event.get('stageVariables', {})

                # Parse the input for the parameter values
                tmp = event['methodArn'].split(':')
                apiGatewayArnTmp = tmp[5].split('/')
                awsAccountId = tmp[4]
                region = tmp[3]
                restApiId = apiGatewayArnTmp[0]
                stage = apiGatewayArnTmp[1]
                method = apiGatewayArnTmp[2]
                resource = '/'

                if (apiGatewayArnTmp[3]):
                    resource += apiGatewayArnTmp[3]

                    # Perform authorization to return the Allow policy for correct parameters
                    # and the 'Unauthorized' error, otherwise.
                response = generateAllow('me', event['methodArn'], decoded_token)
                extra_info = func(event, context)
                response["extra_info"] = extra_info
                return response

            except Exception as e:
                print('unauthorized')
                response = generateDeny('me', event['methodArn'])
                func()
                return response

        return wrapper
    return decorator

def generatePolicy(principalId, effect, resource, decoded_token):
    username = decoded_token.get("preferred_username") or decoded_token.get("username") or decoded_token.get("sub")
    roles = decoded_token.get("roles") or decoded_token.get("realm_access", {}).get("roles", [])

    authResponse = {}
    authResponse['principalId'] = principalId
    if (effect and resource):
        policyDocument = {}
        policyDocument['Version'] = '2012-10-17'
        policyDocument['Statement'] = []
        statementOne = {}
        statementOne['Action'] = 'execute-api:Invoke'
        statementOne['Effect'] = effect
        statementOne['Resource'] = resource
        policyDocument['Statement'] = [statementOne]
        authResponse['policyDocument'] = policyDocument

    authResponse['authentication_context'] = {
        "username": username,
        "roles": roles
    }

    return authResponse


def generateAllow(principalId, resource, decoded_token):
    return generatePolicy(principalId, 'Allow', resource, decoded_token)


def generateDeny(principalId, resource):
    return generatePolicy(principalId, 'Deny', resource)

event = {
    "headers": {
        "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIzNEpOakhmaTd5ZGpadnhUVHA0QzkxZVV0OXV1RDBIV25RQmVZQnlSSW1vIn0.eyJleHAiOjE3NDgwOTU1MDAsImlhdCI6MTc0ODA3NzUwMCwiYXV0aF90aW1lIjoxNzQ4MDc3NDc5LCJqdGkiOiJvbnJ0YWM6MjUzZTE3OWItMTRjMi00MmQ4LWEwNTItMGY4MDM1MjYyNGM2IiwiaXNzIjoiaHR0cHM6Ly9rZXljbG9hay5zdGcuYXV0b3NoaXAudm4vcmVhbG1zL2F1dGhvcml6YXRpb24tZGV2IiwiYXVkIjoiYWNjb3VudCIsInN1YiI6ImRkYzk5NDI2LTYwMmItNDdmZS1hNjIwLTcwZjEwMzI4MTE5ZiIsInR5cCI6IkJlYXJlciIsImF6cCI6ImhvYW5nIiwic2lkIjoiZWNhZjk1ZWMtNDVhNC00ZjQ3LWJmNTItNDNhMzIwYTBkZjQyIiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyIqIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJkZWZhdWx0LXJvbGVzLWF1dGhvcml6YXRpb24tZGV2Iiwib2ZmbGluZV9hY2Nlc3MiLCJhZG1pbiIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwibmFtZSI6ImhvYW5nIGhvYW5nIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiaG9hbmciLCJnaXZlbl9uYW1lIjoiaG9hbmciLCJmYW1pbHlfbmFtZSI6ImhvYW5nIiwiZW1haWwiOiJob2FuZ0BnbWFpbC5jb20ifQ.XREZ3sQ8UaQMyZzL_sVkKsDU4J2sE457j01GqSxIHnxaD_D0mgct63wFcy29OnTHDzcc1aFKn0VmDlrcVAgdonW_EY2bhJgDORqctGSFR0qFV8Mqr-d_5uOO5Hi5Fq_FDy5m4Y5i1PpSb9OwqnLeUx2prJFO6gx1FinfXBHuMOvfo34VQO59U9ViPQpnOAwUwyjJ91vr5l-9jLm-ULdXqM2SBOjlICFZn2J8oEz6JwngFQVWKGlkwq06aEAnh5KfQT0KBCqQdq4yImnYnJHwGHltP7PtX5w-yttNVfXmMqdG3mjCTT7bFaFXTm9ilX8yKp60rQG3tT2BHu6a8kwz6Q"
    },
    "methodArn": "arn:aws:execute-api:us-east-1:123456789012:example123/test/GET/resource"
}

class DummyContext:
    function_name = "test_function"
    memory_limit_in_mb = 128
    invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:test"
    aws_request_id = "test-id"

context = DummyContext()

@keycloak_token_required("test","test")
def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": "Authorized access"
    }

if __name__ == "__main__":
    response = lambda_handler(event, context)
    print(response)