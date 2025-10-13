from fastapi import APIRouter, Request, Body
from fastapi.responses import JSONResponse
from app.graphql.SignupGraphQLSchema import schema
from app.controllers.APIResponse import APIResponse
from app.helpers.ErrorCodes import ErrorCodes

router = APIRouter()

@router.post("/signup-query")
async def graphql_signup_query(request: Request, payload: dict = Body(...)):
    query = payload.get("query")
    if not query:
        return JSONResponse(content=APIResponse.error(msg="Missing GraphQL query", code=ErrorCodes.BAD_REQUEST), status_code=ErrorCodes.BAD_REQUEST)

    result = await schema.execute(query, context_value={"request": request})

    if result.errors:
        return JSONResponse(content=APIResponse.error(msg=str(result.errors[0]), code=ErrorCodes.CONFLICT), status_code=ErrorCodes.CONFLICT)

    return JSONResponse(content=APIResponse.success(msg="Query executed", data=result.data), status_code=ErrorCodes.SUCCESS)
