import time
from typing import Union, Annotated

from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from apps.auth.app import app as app_auth
from apps.admn.app import app as app_admn
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def timeLogger(request: Request, callNext):
    # timeStart = time.time()
    response = await callNext(request)
    # timeEnd = time.time()
    # print({"start": timeStart, "end": timeEnd})
    return response

app.mount("/_admn", app_admn)
app.mount("/_auth", app_auth)