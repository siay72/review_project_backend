from fastapi import FastAPI

from app.database import Base
from app.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Review Platform API",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Review Platform API Running"
    }