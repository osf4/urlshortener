from fastapi import FastAPI

from app.routes import user, url, redirect

app = FastAPI()

app.include_router(user.router)
app.include_router(url.router)
app.include_router(redirect.router)