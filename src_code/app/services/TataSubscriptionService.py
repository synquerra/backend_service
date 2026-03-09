# app/services/TataSubscriptionService.py

import httpx
from fastapi import HTTPException
from app.helpers.ErrorCodes import ErrorCodes
from app.config.config import settings

async def fetch_subscription(iccid: str):

    headers = {"Accept": "*/*",
               "Cache-Control": "no-cache",
               "Cookie": settings.TATA_COOKIE,
               "InitiatorID": settings.TATA_INITIATOR_ID,
               "Ocp-Apim-Subscription-Key": settings.TATA_API_KEY
    }

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(settings.TATA_API_URL, headers=headers, params={"iccids": iccid})

        return response.json()

    except Exception as e:
        raise HTTPException(status_code=ErrorCodes.INTERNAL_SERVER_ERROR, detail=str(e))