# app/graphql/AnalyticsDataSchema.py
import json
import strawberry
from fastapi import Request
from strawberry.exceptions import GraphQLError

def to_camel(d):
    return {
        "id": d["id"],
        "topic": d["topic"],
        "imei": d["imei"],
        "interval": d["interval"],
        "geoid": d["geoid"],
        "packet": d["packet"],
        "latitude": d["latitude"],
        "longitude": d["longitude"],
        "speed": d["speed"],
        "battery": d["battery"],
        "signal": d["signal"],
        "alert": d["alert"],
        "rawText": d["raw_text"],
        "timestampNormalized": d["timestamp_normalized"],
        "timestampIso": d["timestamp_iso"],
        "timestamp": d["timestamp"],
        "receivedAtIst": d["received_at_ist"],
        "processedAt": d["processed_at"],
        "type": d["type"],
        "createdAt": d["created_at"],
    }

@strawberry.type
class AnalyticsDataType:
    id: str | None
    topic: str | None
    imei: str | None
    interval: int | None
    geoid: str | None
    packet: str | None
    latitude: str | None
    longitude: str | None
    speed: str | None
    battery: str | None
    signal: str | None
    alert: str | None
    rawText: str | None
    timestampNormalized: str | None
    timestampIso: str | None
    timestamp: str | None
    receivedAtIst: str | None
    processedAt: str | None
    type: str | None
    createdAt: str | None

@strawberry.type
class Query:

    @strawberry.field
    async def analyticsData(self, info) -> list[AnalyticsDataType]:
        from app.routes.AnalyticsDataRoutes import all_handler
        req: Request = info.context["request"]
        resp = await all_handler(req)
        raw = json.loads(resp.body)["data"]
        return [AnalyticsDataType(**to_camel(r)) for r in raw]

    @strawberry.field
    async def analyticsDataById(self, id: str, info) -> AnalyticsDataType:
        from app.routes.AnalyticsDataRoutes import by_id_handler
        req: Request = info.context["request"]
        resp = await by_id_handler(id, req)
        raw = json.loads(resp.body)["data"]
        return AnalyticsDataType(**to_camel(raw))

    @strawberry.field
    async def analyticsDataByTopic(self, topic: str, info) -> list[AnalyticsDataType]:
        from app.routes.AnalyticsDataRoutes import by_topic_handler
        req: Request = info.context["request"]
        resp = await by_topic_handler(topic, req)
        raw = json.loads(resp.body)["data"]
        return [AnalyticsDataType(**to_camel(r)) for r in raw]

    @strawberry.field
    async def analyticsDataByImei(self, imei: str, info) -> list[AnalyticsDataType]:
        from app.routes.AnalyticsDataRoutes import by_imei_handler
        req: Request = info.context["request"]
        resp = await by_imei_handler(imei, req)
        raw = json.loads(resp.body)["data"]
        return [AnalyticsDataType(**to_camel(r)) for r in raw]

    @strawberry.field
    async def analyticsDataPaginated(self, skip: int, limit: int, info) -> list[AnalyticsDataType]:
        from app.routes.AnalyticsDataRoutes import paginated_handler
        req: Request = info.context["request"]
        resp = await paginated_handler(skip, limit, req)
        raw = json.loads(resp.body)["data"]
        return [AnalyticsDataType(**to_camel(r)) for r in raw]

    @strawberry.field
    async def analyticsDataCount(self, info) -> int:
        from app.routes.AnalyticsDataRoutes import count_handler
        req: Request = info.context["request"]
        resp = await count_handler(req)
        raw = json.loads(resp.body)["data"]
        return raw["count"]

schema = strawberry.Schema(query=Query)
