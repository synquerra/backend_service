import httpx
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.config.config import settings


# shared HTTP client
client = httpx.AsyncClient(timeout=20)


def tata_headers():
    return {
        "Accept": "application/json",
        "Cache-Control": "no-cache",
        "Cookie": settings.TATA_COOKIE,
        "InitiatorID": settings.TATA_INITIATOR_ID,
        "Ocp-Apim-Subscription-Key": settings.TATA_API_KEY
    }


async def make_request(method: str, endpoint: str, params=None, payload=None):

    url = f"{settings.TATA_API_URL}{endpoint}"

    try:
        response = await client.request(
            method=method,
            url=url,
            headers=tata_headers(),
            params=params,
            json=payload
        )

        try:
            data = response.json()
        except Exception:
            data = {"raw_response": response.text}

        return JSONResponse(
            status_code=response.status_code,
            content=data
        )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Tata API timeout"
        )

    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Unable to connect Tata API"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# --------------------------------------------------
# SUBSCRIPTION
# --------------------------------------------------

async def fetch_subscription(iccid: str):
    return await make_request(
        "GET",
        "/subscriptions",
        params={"iccids": iccid}
    )


async def fetch_subscription_by_id(subscription_id: str):
    return await make_request(
        "GET",
        f"/subscriptions/{subscription_id}",
        params={"includeproductvalidity": True}
    )


async def fetch_subscription_balance(subscription_id: str):
    return await make_request(
        "GET",
        f"/subscriptions/{subscription_id}/balances"
    )


# --------------------------------------------------
# DEVICE
# --------------------------------------------------

async def fetch_device_info(iccid: str):
    return await make_request(
        "GET",
        "/deviceInfo",
        params={"iccid": iccid}
    )


# --------------------------------------------------
# DATA SESSION
# --------------------------------------------------

async def fetch_data_session(iccid: str):
    return await make_request(
        "GET",
        "/dataSessionInfo",
        params={"iccid": iccid}
    )


# --------------------------------------------------
# PLAN
# --------------------------------------------------

async def fetch_plans():
    return await make_request(
        "GET",
        "/plans"
    )


async def renew_plan(payload: dict):
    return await make_request(
        "POST",
        "/planRenewal",
        payload=payload
    )


async def change_plan(payload: dict):
    return await make_request(
        "PUT",
        "/subscriptions/changePlan",
        payload=payload
    )


# --------------------------------------------------
# SIM STATE
# --------------------------------------------------

async def update_sim_state(payload: dict):
    return await make_request(
        "PUT",
        "/subscriptions/state",
        payload=payload
    )


# --------------------------------------------------
# SMS
# --------------------------------------------------

async def send_bulk_sms(payload: dict):
    return await make_request(
        "POST",
        "/subscriptions/sms",
        payload=payload
    )


async def fetch_sms_status(transaction_id: str):
    return await make_request(
        "GET",
        "/subscriptions/sms/status",
        params={"transactionId": transaction_id}
    )


# --------------------------------------------------
# WHITELIST
# --------------------------------------------------

async def fetch_whitelist(iccid: str):
    return await make_request(
        "GET",
        "/whitelist",
        params={"iccid": iccid}
    )


async def create_whitelist(payload: dict):
    return await make_request(
        "POST",
        "/whitelist",
        payload=payload
    )


# --------------------------------------------------
# ACCOUNT
# --------------------------------------------------

async def search_accounts(name: str):
    return await make_request(
        "GET",
        "/accounts/search",
        params={"name": name}
    )


# --------------------------------------------------
# STATIC IP
# --------------------------------------------------

async def fetch_static_ip(iccid: str):
    return await make_request(
        "GET",
        f"/subscriptions/{iccid}/staticip"
    )


# --------------------------------------------------
# PRODUCT
# --------------------------------------------------

async def create_product(payload: dict):
    return await make_request(
        "POST",
        "/products",
        payload=payload
    )


async def bootstrap_extension(payload: dict):
    return await make_request(
        "POST",
        "/bootstrap-extension",
        payload=payload
    )


async def bulk_product_status(payload: dict):
    return await make_request(
        "POST",
        "/Products/bulk/changestatus",
        payload=payload
    )