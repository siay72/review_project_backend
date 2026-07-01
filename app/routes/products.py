from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import ProductDetails
from app.database import get_db
from app import crud
from app.dependencies import get_current_admin
from app import schemas
from app import models


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
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
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
    product: schemas.ProductCreate,
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

    return crud.update_product(
        db,
        product_id,
        product,
    )