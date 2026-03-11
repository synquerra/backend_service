from fastapi import APIRouter, Body
from app.services.TataSubscriptionService import *

router = APIRouter()


@router.get("/subscription/{iccid}")
async def get_subscription(iccid: str):
    return await fetch_subscription(iccid)


@router.get("/device/{iccid}")
async def get_device(iccid: str):
    return await fetch_device_info(iccid)


@router.get("/data-session/{iccid}")
async def get_data_session(iccid: str):
    return await fetch_data_session(iccid)


@router.get("/plans")
async def get_plans():
    return await fetch_plans()


@router.get("/whitelist/{iccid}")
async def get_whitelist(iccid: str):
    return await fetch_whitelist(iccid)


@router.post("/whitelist")
async def add_whitelist(payload: dict = Body(...)):
    return await create_whitelist(payload)


@router.post("/sms")
async def send_sms(payload: dict = Body(...)):
    return await send_bulk_sms(payload)


@router.get("/sms/status/{transaction_id}")
async def get_sms_status(transaction_id: str):
    return await fetch_sms_status(transaction_id)


@router.put("/plan/change")
async def change_subscription_plan(payload: dict = Body(...)):
    return await change_plan(payload)


@router.put("/sim/state")
async def update_state(payload: dict = Body(...)):
    return await update_sim_state(payload)


@router.get("/subscription/id/{subscription_id}")
async def get_subscription_by_id(subscription_id: str):
    return await fetch_subscription_by_id(subscription_id)


@router.get("/subscription/{subscription_id}/balance")
async def get_subscription_balance(subscription_id: str):
    return await fetch_subscription_balance(subscription_id)


@router.get("/accounts/{name}")
async def get_accounts(name: str):
    return await search_accounts(name)


@router.get("/static-ip/{iccid}")
async def get_static_ip(iccid: str):
    return await fetch_static_ip(iccid)


@router.post("/plan-renew")
async def plan_renew(payload: dict = Body(...)):
    return await renew_plan(payload)


@router.post("/bootstrap")
async def bootstrap(payload: dict = Body(...)):
    return await bootstrap_extension(payload)


@router.post("/product")
async def create_new_product(payload: dict = Body(...)):
    return await create_product(payload)


@router.post("/product/bulk-status")
async def bulk_status(payload: dict = Body(...)):
    return await bulk_product_status(payload)