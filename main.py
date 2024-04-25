from fastapi import FastAPI

from routes import authentication, user
from models.user import User
from config.database import engine


User.__base__.metadata.create_all(engine)  

app = FastAPI()

app.include_router(authentication.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"author": "horlakz", "about": "Todo App"}