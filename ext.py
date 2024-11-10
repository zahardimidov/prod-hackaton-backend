import ssl
from datetime import datetime, timedelta, timezone

import aiohttp
import jwt
from config import FNS_TOKEN
from passlib.context import CryptContext
from yookassa import Configuration, Payment
import json

Configuration.account_id = '986380'
Configuration.secret_key = 'test_-eujruQjhy1Ifg259CiC4osm25gIhbnvah88hZWeGuA'

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
EXPIRATION_TIME = timedelta(minutes=30)


def create_payment_url(rubles, metadata):
    payment = Payment.create({
        "amount": {
            "value": str(rubles),
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://playcloud.pro"
        },
        "capture": True,
        "metadata": {
            "data": json.dumps(metadata)
        }
    })
    return payment.confirmation.confirmation_url


def create_jwt_token(data: dict):
    expiration = datetime.now(timezone.utc) + EXPIRATION_TIME
    data.update({"exp": expiration})
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token 


def verify_jwt_token(token: str):
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_data
    except jwt.PyJWTError as e:
        print(e)
        return None


async def scanqrcode(file: bytes):
    url = "https://proverkacheka.com/api/v1/check/get"
    data = {"token": FNS_TOKEN}

    form_data = aiohttp.FormData()
    form_data.add_field("token", data["token"])
    form_data.add_field("qrfile", file, filename="test.jpg")

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=form_data, ssl=ssl_context) as response:
            response_data = await response.json()
            result = response_data.get("data", {}).get(
                "json", {}).get("items", [])
            for item in result:
                item['price'] = round(item['price'] / 100, 2)
                item['sum'] = round(item['sum'] / 100, 2)
    return result
