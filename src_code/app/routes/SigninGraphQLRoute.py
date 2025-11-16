from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request, Body
from app.helpers.ErrorCodes import ErrorCodes
from app.graphql.SigninGraphQLSchema import schema
from app.controllers.APIResponse import APIResponse
from app.helpers.ErrorMessages import ErrorMessages

router = APIRouter()

@router.post("/signin-query")
async def graphql_signin_query(request: Request, payload: dict = Body(...)):
    query = payload.get("query")
    if not query:
        return JSONResponse(
            content=APIResponse.error(msg=ErrorMessages.MISSING_GRAPHQL_QUERY, code=ErrorCodes.BAD_REQUEST),
            status_code=ErrorCodes.BAD_REQUEST
        )

    result = await schema.execute(query, context_value={"request": request})

    if result.errors:
        error_msg = str(result.errors[0].message)
        if "Invalid email or password" or "login failed" in error_msg.lower() or "inactive" in error_msg.lower():
            return JSONResponse(
                content=APIResponse.error(msg=error_msg, code=ErrorCodes.UNAUTHORIZED),
                status_code=ErrorCodes.UNAUTHORIZED
            )
        return JSONResponse(
            content=APIResponse.error(msg=error_msg, code=ErrorCodes.INTERNAL_SERVER_ERROR),
            status_code=ErrorCodes.INTERNAL_SERVER_ERROR
        )

    flattened_data = next(iter(result.data.values())) if result.data else None

    return JSONResponse(
        content=APIResponse.success(msg=ErrorMessages.LOGIN_SUCCESS, data=flattened_data),
        status_code=ErrorCodes.SUCCESS
    )
