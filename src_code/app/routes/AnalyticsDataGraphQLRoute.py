from fastapi import APIRouter, Request, Body
from fastapi.responses import JSONResponse
from app.graphql.AnalyticsDataSchema import schema
from app.controllers.APIResponse import APIResponse

router = APIRouter()

@router.post("/analytics-query")
async def analytics_graph_query(payload: dict = Body(...)):
    query = payload.get("query")
    if not query:
        return JSONResponse(APIResponse.error("Missing GraphQL query", 400), 400)

    result = await schema.execute(query)

    if result.errors:
        return JSONResponse(APIResponse.error(str(result.errors[0]), 500), 500)

    return JSONResponse(APIResponse.success("OK", result.data))
