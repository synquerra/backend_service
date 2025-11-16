from fastapi import APIRouter, Request, Body
from fastapi.responses import JSONResponse
from app.graphql.SignupGraphQLSchema import schema
from app.controllers.APIResponse import APIResponse
from app.helpers.ErrorCodes import ErrorCodes

# ✅ Define router before using it
router = APIRouter()

@router.post("/signup-query")
async def graphql_signup_query(request: Request, payload: dict = Body(...)):
    query = payload.get("query")
    if not query:
        return JSONResponse(
            content=APIResponse.error(msg="Missing GraphQL query", code=ErrorCodes.BAD_REQUEST),
            status_code=ErrorCodes.BAD_REQUEST
        )

    result = await schema.execute(query, context_value={"request": request})

    if result.errors:
        error_msg = str(result.errors[0].message).strip()
        error_msg_lower = error_msg.lower()

        if "email already registered" in error_msg_lower or "mobile number already registered" in error_msg_lower:
            return JSONResponse(content=APIResponse.error(msg=error_msg, code=ErrorCodes.CONFLICT),
                status_code=ErrorCodes.CONFLICT
            )
        return JSONResponse(content=APIResponse.error(msg=error_msg, code=ErrorCodes.INTERNAL_SERVER_ERROR),
            status_code=ErrorCodes.INTERNAL_SERVER_ERROR
        )

    flattened_data = next(iter(result.data.values())) if result.data else None

    return JSONResponse(content=APIResponse.success(msg="Signup successful", data=flattened_data),
        status_code=ErrorCodes.SUCCESS
    )
