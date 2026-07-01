from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from fastapi import HTTPException
from app import models, schemas
from sqlalchemy.orm import joinedload

# ==========================================
# USER CRUD
# ==========================================

def create_user(db: Session, user: schemas.UserCreate):
    existing_user = (
        db.query(models.User)
        .filter(models.User.email == user.email)
        .first()
    )

    if existing_user:
        return existing_user

    db_user = models.User(
        name=user.name,
        email=user.email,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_users(db: Session):
    return db.query(models.User).order_by(models.User.id.desc()).all()


def delete_user(db: Session, user_id: int):
    user = (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .first()
    )

    if not user:
        return None

    # Don't allow deleting the admin account
    if user.is_admin:
        raise HTTPException(
            status_code=400,
            detail="Admin account cannot be deleted."
        )

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}


# ==========================================
# PRODUCT CRUD
# ==========================================


def create_product(db, product: schemas.ProductCreate):
    db_product = models.Product(
        title=product.title,
        description=product.description,
        image_url=product.image_url,
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product




def get_products(db: Session):
    products = db.query(models.Product).all()

    result = []

    for product in products:
        avg_rating = (
            db.query(func.avg(models.Review.rating))
            .filter(models.Review.product_id == product.id)
            .scalar()
        )

        review_count = (
            db.query(func.count(models.Review.id))
            .filter(models.Review.product_id == product.id)
            .scalar()
        )

        result.append({
            "id": product.id,
            "title": product.title,
            "description": product.description,
            "image_url": product.image_url,
            "average_rating": round(avg_rating or 0, 1),
            "review_count": review_count
        })

    return result


def get_product(db: Session, product_id: int):
    product = (
        db.query(models.Product)
        .options(
            joinedload(models.Product.reviews)
            .joinedload(models.Review.user)
        )
        .filter(models.Product.id == product_id)
        .first()
    )

    if not product:
        return None

    avg = (
        db.query(func.avg(models.Review.rating))
        .filter(models.Review.product_id == product.id)
        .scalar()
    )

    reviews = []

    for review in product.reviews:
        reviews.append(
            {
                "id": review.id,
                "user": review.user.name,
                "user_id": review.user.id,
                "rating": review.rating,
                "comment": review.comment,
                "created_at": review.created_at,
            }
        )

    return {
        "id": product.id,
        "title": product.title,
        "description": product.description,
        "image_url": product.image_url,
        "average_rating": round(avg or 0, 1),
        "reviews": reviews
    }


def update_product(db, product_id: int, product: schemas.ProductCreate):
    db_product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if not db_product:
        return None

    db_product.title = product.title
    db_product.description = product.description
    db_product.image_url = product.image_url

    db.commit()
    db.refresh(db_product)

    return db_product

def delete_product(db, product_id: int):
    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if not product:
        return False

    db.delete(product)
    db.commit()

    return True

# ==========================================
# REVIEW CRUD
# ==========================================


def get_reviews(db: Session):
    reviews = (
        db.query(models.Review)
        .options(
            joinedload(models.Review.user),
            joinedload(models.Review.product),
        )
        .order_by(models.Review.created_at.desc())
        .all()
    )

    return [
        {
            "id": review.id,
            "user": review.user.name,
            "product": review.product.title,
            "rating": review.rating,
            "comment": review.comment,
            "created_at": review.created_at,
        }
        for review in reviews
    ]


def create_review(db, review, current_user):
    db_review = models.Review(
        product_id=review.product_id,
        user_id=current_user.id,
        rating=review.rating,
        comment=review.comment,
    )

    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    return db_review

def update_review(
    db: Session,
    review_id: int,
    review: schemas.ReviewUpdate,
    user_id: int,
):
    db_review = (
        db.query(models.Review)
        .filter(models.Review.id == review_id)
        .first()
    )

    if not db_review:
        return None

    if db_review.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You can only edit your own review."
        )

    db_review.rating = review.rating
    db_review.comment = review.comment

    db.commit()
    db.refresh(db_review)

    return db_review


def delete_review(
    db: Session,
    review_id: int,
    user_id: int,
):
    db_review = (
        db.query(models.Review)
        .filter(models.Review.id == review_id)
        .first()
    )

    if not db_review:
        return None

    if db_review.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own review."
        )

    db.delete(db_review)
    db.commit()

    return {"message": "Review deleted successfully"}