from fastapi import Request, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

class HostHeaderValidatorMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, allowed_hosts: list[str]):
        super().__init__(app)
        self.allowed_hosts = set(allowed_hosts)

    async def dispatch(self, request: Request, call_next):
        host_header = request.headers.get("host", "")
        host = host_header.split(":")[0]

        if host not in self.allowed_hosts:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "code": 400,
                    "request_id": getattr(request.state, "request_id", None),
                    "error_description": f"Invalid Host header: {host}",
                },
            )
        return await call_next(request)
