from app.routes.SigninGraphQLRoute import router as signin_graphql_route
from app.routes.SignupGraphQLRoute import router as signup_graphql_route
from app.routes.DeviceMasterGraphQLRoute import router as device_graphql_route


router_registry = []

router_registry += [
    {"router": signin_graphql_route, "prefix": "/auth", "tags": ["Signin GraphQL"], "include_in_schema": True},
    {"router": signup_graphql_route, "prefix": "/auth", "tags": ["Signup GraphQL"], "include_in_schema": True},
    {"router": device_graphql_route, "prefix": "/device", "tags": ["Device Master GraphQL"], "include_in_schema": True}
]
