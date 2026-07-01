from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, UTC

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    hashed_password = Column(String, nullable=False)

    is_admin = Column(Boolean, default=False)

    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

    reviews = relationship(
        "Review",
        back_populates="user",
        cascade="all, delete"
    )

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)

    description = Column(Text)

    image_url = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

    reviews = relationship(
        "Review",
        back_populates="product",
        cascade="all, delete"
    )


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(
        Integer,
        ForeignKey("products.id", ondelete="CASCADE")
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE")
    )

    rating = Column(Integer, nullable=False)

    comment = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship(
        "User",
        back_populates="reviews"
    )

    product = relationship(
        "Product",
        back_populates="reviews"
    )