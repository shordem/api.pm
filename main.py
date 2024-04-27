from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import (
    authentication,
    user as user_route,
    organization as organization_route,
)
from config.database import Base
from config.database import engine

origins = [
    "http://localhost",
]

Base.metadata.create_all(bind=engine)

app = FastAPI(
    version="0.1.0",
    title="Todo App",
    description="A simple todo app",
    root_path="/v2",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

app.include_router(authentication.router)
app.include_router(user_route.router)
app.include_router(organization_route.router)


@app.get("/")
def root():
    return {"author": "horlakz", "about": "Todo App"}
