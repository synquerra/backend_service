from app.routes.JwtAuthRoutes import router as jwt_router
from app.routes.SignupRoutes import router as signup_router
from app.routes.SigninRoutes import router as signin_router

router_registry = [
    {"router": jwt_router, "prefix": "/auth", "tags": ["Authentication"], "include_in_schema": True},
    {"router": signup_router, "prefix": "/auth", "tags": ["Authentication"], "include_in_schema": True},
    {"router": signin_router, "prefix": "/auth", "tags": ["Authentication"], "include_in_schema": True}
]