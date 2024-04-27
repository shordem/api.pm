from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.database import Base, engine
from routes import authentication
from routes import organization as organization_route
from routes import user as user_route

origins = ["*"]

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
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authentication.router)
app.include_router(user_route.router)
app.include_router(organization_route.router)


@app.get("/")
def root():
    return {"author": "horlakz", "about": "Todo App"}
