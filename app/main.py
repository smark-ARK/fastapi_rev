from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from . import models
from .database import engine
from .routers import user, post, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)

app.mount("/static", StaticFiles(directory="static"), name="static")
