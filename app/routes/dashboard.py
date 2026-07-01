from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import Product, Review, User
from app.dependencies import get_current_admin

router = APIRouter(
    prefix="/api/admin",
    tags=["Admin Dashboard"],
)


@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    total_products = db.query(Product).count()

    total_reviews = db.query(Review).count()

    total_users = db.query(User).count()

    average_rating = (
        db.query(func.avg(Review.rating)).scalar() or 0
    )

    recent_reviews = (
        db.query(Review)
        .order_by(Review.created_at.desc())
        .limit(5)
        .all()
    )

    reviews = []

    for review in recent_reviews:
        reviews.append(
            {
                "id": review.id,
                "user": review.user.name,
                "product": review.product.title,
                "rating": review.rating,
                "comment": review.comment,
                "created_at": review.created_at,
            }
        )

    return {
        "totalProducts": total_products,
        "totalReviews": total_reviews,
        "totalUsers": total_users,
        "averageRating": round(average_rating, 1),
        "recentReviews": reviews,
    }