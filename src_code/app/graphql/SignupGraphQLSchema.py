import json
import strawberry
from strawberry.exceptions import GraphQLError
from fastapi import Request
from app.routes.SignupRoutes import signup_user
from app.controllers.SignupController import SignupRequest

@strawberry.type
class UserType:
    id: str = strawberry.field(name="_id")  # ✅ Expose as `_id` in GraphQL
    name: str
    email: str

@strawberry.type
class SignupData:
    user: UserType

@strawberry.type
class SignupWrapperResponse:
    status: str
    data: SignupData

@strawberry.input
class SignupInput:
    firstName: str
    middleName: str = ""
    lastName: str
    email: str
    mobile: str
    password: str

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def signup(self, input: SignupInput, info) -> SignupWrapperResponse:
        request: Request = info.context["request"]
        payload = SignupRequest(
            first_name=input.firstName,
            middle_name=input.middleName,
            last_name=input.lastName,
            email=input.email,
            mobile=input.mobile,
            password=input.password
        )
        response = await signup_user(payload, request)

        if response.status_code != 200:
            try:
                error_json = json.loads(response.body.decode())
                raise GraphQLError(error_json.get("error_description", "Signup failed"))
            except Exception:
                raise GraphQLError("Unexpected signup error")

        parsed = json.loads(response.body.decode())["data"]

        user = UserType(
            id=parsed["unique_id"],
            name=f"{parsed['first_name']} {parsed['middle_name']} {parsed['last_name']}".strip(),
            email=parsed["email"]
        )

        return SignupWrapperResponse(
            status="success",
            data=SignupData(user=user)
        )

@strawberry.type
class Query:
    @strawberry.field
    def ping(self) -> str:
        return "pong"

schema = strawberry.Schema(query=Query, mutation=Mutation)
