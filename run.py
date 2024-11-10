from fastapi import FastAPI, Response, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from api import auth_router, bill_router, group_router, user_router
from config import PORT
from database.admin import init_admin
from database.session import engine, run_database
from database.requests import update_user_paid_dolg
import json


async def on_startup(app: FastAPI):
    init_admin(app=app, engine=engine)
    await run_database()

    yield

app = FastAPI(lifespan=on_startup)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(group_router)
app.include_router(bill_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        '*'
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/ping', response_class=Response)
async def ping():
    return Response(status_code=200)


@app.get('/', response_class=HTMLResponse, include_in_schema=False)
async def home():
    return f'<div style="display: flex; width: 100vw; height: 100vh; justify-content: center; background-color: #F9F9F9; color: #03527E;"> <b style="margin-top:35vh">Welcome!</b> </div>'


@app.post('/kassa', response_class=Response)
async def kassa(request: Request):
    data = await request.json()

    if not data['event'] == 'payment.succeeded':
        raise HTTPException(status_code=400, detail='Incorrect event')
    
    metadata = json.loads(data["object"]["metadata"]["data"])
    
    for bill in metadata:
        bill_id = bill["bill_id"]
        user_id = bill["user_id"]
        amount = bill["amount"]
        
        await update_user_paid_dolg(bill_id=bill_id, user_id=user_id, amount=amount)

    return Response(status_code=200)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT, forwarded_allow_ips='*')
