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


print(f"KEYCLOAK_URL: {KEYCLOAK_URL}")
print(f"REALM: {REALM}")
print(f"ISSUER: {ISSUER}")
print(f"AUDIENCE: {AUDIENCE}")
print(f"JWKS_URL: {JWKS_URL}")
print(f"VERIFY_MODE: {VERIFY_MODE}")

from datum_authorization.keycloak.decoder.offline_decoder import KeycloakOfflineDecoder
from datum_authorization.keycloak.decoder.online_decoder import KeycloakOnlineDecoder

handlers = [KeycloakOfflineDecoder(), KeycloakOnlineDecoder()]
def get_jwt_header(token: str) -> dict:
    header_b64 = token.split('.')[0]
    header_b64 += '=' * (-len(header_b64) % 4)  # pad base64 if needed
    decoded = base64.urlsafe_b64decode(header_b64)
    return json.loads(decoded)

def keycloak_lambda_auth_handler(issuer, audience):

    def decorator(func):
        @wraps(func)
        def wrapper(event, context, *args, **kwargs):
            try:
                auth_header = event["headers"].get("Authorization", "")
                if not auth_header.startswith("Bearer "):
                    raise Exception("Missing or invalid Authorization header")

                token = auth_header.split(" ")[1]
                print("token: ")
                print(token)
                handler = next(filter(lambda x: x.can_execute(), handlers), None)
                if handler == None:
                    raise Exception("Authentication type not supported")
                decoded_token = handler.execute(token)
                event["decoded_token"] = decoded_token  # Pass it along
                print(decoded_token)
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
                # response["context"]["extra_info"] = extra_info
                # response["context"]["extra_info"] = "extra_info"
                return response

            except Exception as e:
                print('unauthorized')
                print(e)
                response = generateDeny('me', event['methodArn'])
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

    # authResponse['context'] = {
    #     "username": username,
    #     "roles": roles
    # }
    # authResponse['context'] = {
    #     "userName": username,
    #     "userRoles": "role"
    # }

    authResponse['context'] = {
        "stringKey": "stringval",
        "numberKey": 123,
        "booleanKey": "true"
    }
    print(authResponse)

    return authResponse


def generateAllow(principalId, resource, decoded_token):
    return generatePolicy(principalId, 'Allow', resource, decoded_token)


def generateDeny(principalId, resource):
    return generatePolicy(principalId, 'Deny', resource)

event = {
    "headers": {
        "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIzNEpOakhmaTd5ZGpadnhUVHA0QzkxZVV0OXV1RDBIV25RQmVZQnlSSW1vIn0.eyJleHAiOjE3NDgxMjY3NjEsImlhdCI6MTc0ODEwODc2MSwiYXV0aF90aW1lIjoxNzQ4MTA4NzM5LCJqdGkiOiJvbnJ0YWM6Njc0MzYzYzMtYjgxOC00NjU3LWI5YTgtMzk0YzgwNTFjYTU5IiwiaXNzIjoiaHR0cHM6Ly9rZXljbG9hay5zdGcuYXV0b3NoaXAudm4vcmVhbG1zL2F1dGhvcml6YXRpb24tZGV2IiwiYXVkIjoiYWNjb3VudCIsInN1YiI6ImRkYzk5NDI2LTYwMmItNDdmZS1hNjIwLTcwZjEwMzI4MTE5ZiIsInR5cCI6IkJlYXJlciIsImF6cCI6ImhvYW5nIiwic2lkIjoiNTc2MGYzNTgtYWJlNC00MzBhLTgyMzEtODY4YjE5ZDdmMGFlIiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyIqIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJkZWZhdWx0LXJvbGVzLWF1dGhvcml6YXRpb24tZGV2Iiwib2ZmbGluZV9hY2Nlc3MiLCJhZG1pbiIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwibmFtZSI6ImhvYW5nIGhvYW5nIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiaG9hbmciLCJnaXZlbl9uYW1lIjoiaG9hbmciLCJmYW1pbHlfbmFtZSI6ImhvYW5nIiwiZW1haWwiOiJob2FuZ0BnbWFpbC5jb20ifQ.T2FFZMrl89Xzcjt6ax2Y6Nj701kbKe4-tQZOuV2tT-6caGkds8-FiUxmgOogdkYIHd3xB0PtKeDtKtfLnhIWhztkEQ_6XD0xRboCLcNFMEuJG5r7kp8jswW5-V0ssNo991HpCtYojpLcEbP0vPFheXpSYx7-HT8LstBAtvgEFFVGxtWO9Y3bSYabIim5CfeWAMx3KjyRxcsDFl1Yg2oNksDuFS_li7PFaMlMQPgSfnO-BwhKKZjm_DIQEdALzKH4dm-r2J4HqUtLP4HLndwrZoe9eataLuthUqI9cMXYwBCsgnKLSNdy5Z1rkXxL1MoBzXH1dDN9-g0XHz-e6GIiOA"
    },
    "methodArn": "arn:aws:execute-api:us-east-1:123456789012:example123/test/GET/resource"
}

class DummyContext:
    function_name = "test_function"
    memory_limit_in_mb = 128
    invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:test"
    aws_request_id = "test-id"

context = DummyContext()

@keycloak_lambda_auth_handler("test","test")
def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": "Authorized access"
    }

if __name__ == "__main__":
    response = lambda_handler(event, context)
    print(response)