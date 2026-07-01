from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine

from app.routes.users import router as user_router
from app.routes.products import router as product_router
from app.routes.reviews import router as review_router
from app.routes.auth import router as auth_router
from app.routes.dashboard import router as dashboard_router
from app.routes.upload import router as upload_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Review Platform API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://review-client-two.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





@app.get("/")
def home():
    return {"message": "Review Platform API Running"}

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(product_router)
app.include_router(review_router)
app.include_router(dashboard_router)
app.include_router(upload_router)
