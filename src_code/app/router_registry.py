from app.routes.JwtAuthRoutes import router as jwt_router

router_registry = [
    {"router": jwt_router, "prefix": "/auth", "tags": ["Authentication"], "include_in_schema": True}
]