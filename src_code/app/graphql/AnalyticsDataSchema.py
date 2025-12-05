import strawberry
from bson import ObjectId

from app.models import get_db
from app.models.AnalyticsData import AnalyticsData
from app.controllers.AnalyticsDataController import serialize


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
    speed: int | None

    battery: int | None
    signal: int | None
    alert: str | None

    # PRIMARY field used by frontend for sorting/display
    timestamp: str | None

    deviceTimestamp: str | None
    receivedAtUtc: str | None
    rawTimestamp: str | None

    rawPacket: str | None
    rawImei: str | None
    rawAlert: str | None
    rawTemperature: str | None
    rawSpeed: str | None
    rawSignal: str | None
    rawBattery: str | None
    rawGeoid: str | None
    rawLatitude: str | None
    rawLongitude: str | None
    rawInterval: str | None

    type: str | None


@strawberry.type
class Query:

    @strawberry.field
    async def analyticsData(self) -> list[AnalyticsDataType]:
        recs = await get_db().find(AnalyticsData)
        return [AnalyticsDataType(**serialize(r)) for r in recs]

    @strawberry.field
    async def analyticsDataById(self, id: str) -> AnalyticsDataType | None:
        try:
            rec = await get_db().find_one(AnalyticsData, {"_id": ObjectId(id)})
        except:
            return None
        return AnalyticsDataType(**serialize(rec)) if rec else None

    @strawberry.field
    async def analyticsDataByTopic(self, topic: str) -> list[AnalyticsDataType]:
        recs = await get_db().find(AnalyticsData, {"topic": topic})
        return [AnalyticsDataType(**serialize(r)) for r in recs]

    @strawberry.field
    async def analyticsDataByImei(self, imei: str) -> list[AnalyticsDataType]:
        recs = await get_db().find(AnalyticsData, {"imei": imei})
        return [AnalyticsDataType(**serialize(r)) for r in recs]

    @strawberry.field
    async def analyticsDataPaginated(self, skip: int, limit: int) -> list[AnalyticsDataType]:
        recs = await get_db().find(AnalyticsData)
        sliced = recs[skip:skip + limit]
        return [AnalyticsDataType(**serialize(r)) for r in sliced]

    @strawberry.field
    async def analyticsDataCount(self) -> int:
        return await get_db().count(AnalyticsData)


schema = strawberry.Schema(query=Query)
