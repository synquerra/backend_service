# app/routes/DeviceMasterGraphQLRoute.py
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request, Body
from app.graphql.DeviceMasterGraphQLSchema import schema
from app.controllers.APIResponse import APIResponse
from app.helpers.ErrorCodes import ErrorCodes
from app.helpers.ErrorMessages import ErrorMessages

router = APIRouter()

@router.post("/device-master-query")
async def graphql_device_master_query(request: Request, payload: dict = Body(...)):
    query = payload.get("query")

    if not query:
        return JSONResponse(
            APIResponse.error(
                msg=ErrorMessages.MISSING_GRAPHQL_QUERY,
                code=ErrorCodes.BAD_REQUEST
            ),
            status_code=ErrorCodes.BAD_REQUEST
        )

    result = await schema.execute(query, context_value={"request": request})

    if result.errors:
        return JSONResponse(
            APIResponse.error(
                msg=str(result.errors[0]),
                code=ErrorCodes.INTERNAL_SERVER_ERROR,
            ),
            status_code=ErrorCodes.INTERNAL_SERVER_ERROR
        )

    return JSONResponse(
        APIResponse.success(msg="Success", data=result.data),
        status_code=ErrorCodes.SUCCESS
    )
