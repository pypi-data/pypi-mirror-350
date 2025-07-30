from functools import wraps

def pre_authorize(required_roles):
    required_roles = set(required_roles) if isinstance(required_roles, (list, tuple, set)) else {required_roles}

    def decorator(func):
        @wraps(func)
        def wrapper(event, context, *args, **kwargs):
            roles_string = event.get("requestContext", {}).get("authorizer", {}).get("roles", "")
            user_roles = set(roles_string.split(",")) if roles_string else set()

            if not user_roles & required_roles:
                return {
                    "statusCode": 403,
                    "body": f"Forbidden: Requires any of roles {required_roles}"
                }

            return func(event, context, *args, **kwargs)
        return wrapper
    return decorator

def post_authorize(check_func):

    def decorator(func):
        @wraps(func)
        def wrapper(event, context, *args, **kwargs):
            result = func(event, context, *args, **kwargs)

            # Extract user info
            authorizer = event.get("requestContext", {}).get("authorizer", {})
            user_name = authorizer.get("userName", "unknown")
            user_roles = authorizer.get("roles", "")

            # Call the check function with result and user info
            authorized = check_func(result, user_name, user_roles)

            if not authorized:
                return {
                    "statusCode": 403,
                    "body": "Forbidden: Post-authorization check failed"
                }

            return result
        return wrapper
    return decorator





context = {}

# Case 1: Authorized user with 'admin' role
event_admin = {
    "requestContext": {
        "authorizer": {
            "userName": "admin",
            "roles": "admin,offline_access"
        }
    }
}

# Case 2: Unauthorized user without 'admin' role
event_user = {
    "requestContext": {
        "authorizer": {
            "userName": "user",
            "roles": "viewer"
        }
    }
}

# Case 3: Missing roles entirely
event_no_roles = {
    "requestContext": {
        "authorizer": {
            "userName": "guest"
            # No userRoles key
        }
    }
}

@pre_authorize("admin")
def pre_lambda_handler(event, context):
    user = event["requestContext"]["authorizer"]["userName"]
    return {
        "statusCode": 200,
        "body": f"Hello {user}, you have admin access."
    }

@post_authorize(lambda result, user_name, roles: result.get("owner") == user_name)
def post_lambda_handler(event, context):
    return {
        "statusCode": 200,
        "owner": "user",
        "data": "confidential"
    }


if __name__ == "__main__":
    print(pre_lambda_handler(event_admin, context))

    print("\nUnauthorized:")
    print(pre_lambda_handler(event_user, context))

    print("\nMissing roles:")
    print(pre_lambda_handler(event_no_roles, context))

    print(post_lambda_handler(event_user, context))
