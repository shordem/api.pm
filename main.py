from fastapi import FastAPI

from routes import (
    authentication,
    user as user_route,
    organization as organization_route,
)
from config.database import Base
from config.database import engine


Base.metadata.create_all(bind=engine)

app = FastAPI(
    version="0.1.0",
    title="Todo App",
    description="A simple todo app",
    root_path="/v1",
)

app.include_router(authentication.router)
app.include_router(user_route.router)
app.include_router(organization_route.router)


@app.get("/")
def root():
    return {"author": "horlakz", "about": "Todo App"}
