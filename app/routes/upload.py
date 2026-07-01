from fastapi import APIRouter, UploadFile, File
import cloudinary.uploader

from app.cloudinary_config import *

router = APIRouter(
    prefix="/api/upload",
    tags=["Upload"]
)

@router.post("/")
async def upload_image(file: UploadFile = File(...)):
    result = cloudinary.uploader.upload(
        file.file,
        folder="review-platform/products"
    )

    return {
        "image_url": result["secure_url"]
    }