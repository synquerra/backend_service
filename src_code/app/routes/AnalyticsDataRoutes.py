# app/routes/AnalyticsDataRoutes.py
from fastapi import Request

async def all_handler(request: Request):
    from app.controllers.AnalyticsDataController import AnalyticsDataController
    return await AnalyticsDataController().all(request)

async def by_id_handler(id: str, request: Request):
    from app.controllers.AnalyticsDataController import AnalyticsDataController
    return await AnalyticsDataController().by_id(id, request)

async def by_topic_handler(topic: str, request: Request):
    from app.controllers.AnalyticsDataController import AnalyticsDataController
    return await AnalyticsDataController().by_topic(topic, request)

async def by_imei_handler(imei: str, request: Request):
    from app.controllers.AnalyticsDataController import AnalyticsDataController
    return await AnalyticsDataController().by_imei(imei, request)

async def paginated_handler(skip: int, limit: int, request: Request):
    from app.controllers.AnalyticsDataController import AnalyticsDataController
    return await AnalyticsDataController().paginated(skip, limit, request)

async def count_handler(request: Request):
    from app.controllers.AnalyticsDataController import AnalyticsDataController
    return await AnalyticsDataController().count(request)
