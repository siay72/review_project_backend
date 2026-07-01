from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.schemas import ProductDetails
from app.database import get_db
from app import crud
from app.dependencies import get_current_admin
from app import schemas
from app import models

import os
import shutil

router = APIRouter(
    prefix="/api/products",
    tags=["Products"]
)


@router.get("/")
def get_products(
    db: Session = Depends(get_db)
):
    return crud.get_products(db)




@router.get(
    "/{product_id}",
    response_model=ProductDetails
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = crud.get_product(db, product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    image_url = product["image_url"]
    return product



@router.post("/")
def create_product(
    title: str = Form(...),
    description: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):

    os.makedirs("uploads", exist_ok=True)

    filename = image.filename
    filepath = f"uploads/{filename}"

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    image_url = f"/uploads/{filename}"

    product = schemas.ProductCreate(
        title=title,
        description=description,
        image_url=image_url,
    )

    return crud.create_product(db, product)


@router.delete("/{id}")
def delete_product(
    id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    deleted = crud.delete_product(db, id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return {"message": "Product deleted successfully"}



@router.put("/{product_id}")
def update_product(
    product_id: int,
    title: str = Form(...),
    description: str = Form(...),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):

    db_product = (
        db.query(models.Product)
        .filter(models.Product.id == product_id)
        .first()
    )

    if not db_product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    image_url = db_product.image_url

    if image:

        os.makedirs("uploads", exist_ok=True)

        filename = image.filename

        filepath = f"uploads/{filename}"

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        image_url = f"/uploads/{filename}"

    product = schemas.ProductCreate(
        title=title,
        description=description,
        image_url=image_url,
    )

    return crud.update_product(
        db,
        product_id,
        product,
    )