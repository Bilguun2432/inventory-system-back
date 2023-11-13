from fastapi import FastAPI
from dotenv import load_dotenv
from .router import auth

load_dotenv()
app = FastAPI()
app.include_router(auth.router)