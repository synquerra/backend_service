import json
import strawberry
from fastapi import Request
from strawberry.exceptions import GraphQLError
from app.routes.SigninRoutes import signin_user
from app.helpers.ErrorMessages import ErrorMessages
from app.controllers.SigninController import SigninRequest

@strawberry.type
class TokenType:
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int

@strawberry.type
class SigninResponse:
    unique_id: str
    first_name: str
    middle_name: str
    last_name: str
    email: str
    imei: str
    user_type: str
    mobile: str
    tokens: TokenType
    is_email_verified: bool
    is_mobile_verified: bool
    last_login_at: str
    message: str

@strawberry.input
class SigninInput:
    email: str
    password: str

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def signin(self, input: SigninInput, info) -> SigninResponse:
        request: Request = info.context["request"]
        payload = SigninRequest(**input.__dict__)
        response = await signin_user(payload, request)

        if response.status_code != 200:
            raise GraphQLError(response.body.decode())

        parsed = json.loads(response.body.decode())["data"]

        return SigninResponse(
            unique_id=parsed["unique_id"],
            first_name=parsed["first_name"],
            middle_name=parsed["middle_name"],
            last_name=parsed["last_name"],
            email=parsed["email"],
            imei= parsed["imei"],
            user_type= parsed["user_type"],
            mobile=parsed["mobile"],
            tokens=TokenType(**parsed["tokens"]),
            is_email_verified=parsed["is_email_verified"],
            is_mobile_verified=parsed["is_mobile_verified"],
            last_login_at=parsed["last_login_at"],
            message=ErrorMessages.LOGIN_SUCCESS
        )

@strawberry.type
class Query:
    @strawberry.field
    def ping(self) -> str:
        return "pong"

schema = strawberry.Schema(query=Query, mutation=Mutation)
