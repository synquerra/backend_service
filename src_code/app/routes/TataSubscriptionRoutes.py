# app/routes/TataSubscriptionRoutes.py

from fastapi import APIRouter
from app.services.TataSubscriptionService import fetch_subscription

router = APIRouter()

@router.get("/tata/subscription/{iccid}")
async def get_subscription(iccid: str):
    return await fetch_subscription(iccid)