from fastapi.responses import JSONResponse
from fastapi import APIRouter, Body, Request
from app.helpers.ErrorCodes import ErrorCodes
from app.graphql.DeviceMasterSchema import schema
from app.controllers.APIResponse import APIResponse
from app.helpers.ErrorMessages import ErrorMessages

router = APIRouter()

@router.post("/device-query")
async def graphql_device_query(request: Request, payload: dict = Body(...)):
    query = payload.get("query")
    if not query:
        return JSONResponse(content=APIResponse.error(msg=ErrorMessages.MISSING_GRAPHQL_QUERY, code=ErrorCodes.BAD_REQUEST), status_code=ErrorCodes.BAD_REQUEST)

    result = await schema.execute(query)

    if result.errors:
        return JSONResponse(content=APIResponse.error(msg=str(result.errors[0]), code=ErrorCodes.INTERNAL_SERVER_ERROR), status_code=ErrorCodes.INTERNAL_SERVER_ERROR)

    if result.data and result.data.get("get_device") is None and result.data.get("list_devices") is None:
        return JSONResponse(content=APIResponse.error(msg=ErrorMessages.DEVICE_NOT_FOUND, code=ErrorCodes.NOT_FOUND), status_code=ErrorCodes.NOT_FOUND)

    return JSONResponse(content=APIResponse.success(msg=ErrorMessages.DEVICE_FETCHED, data=result.data), status_code=ErrorCodes.SUCCESS)

