from pydantic import BaseModel, ConfigDict, Field, EmailStr
from datetime import datetime


# ==========================
# User Schemas
# ==========================

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    is_admin: bool
    created_at: datetime


# ==========================
# Review Schemas
# ==========================

class ReviewCreate(BaseModel):
    product_id: int
    user_id: int
    rating: int = Field(..., ge=1, le=5)
    comment: str


class ReviewUpdate(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: str


class ReviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    rating: int
    comment: str
    created_at: datetime

    user: UserResponse


# ==========================
# Product Schemas
# ==========================

class ProductCreate(BaseModel):
    title: str
    description: str
    image_url: str


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    image_url: str
    created_at: datetime


class ProductListResponse(BaseModel):
    id: int
    title: str
    description: str
    image_url: str
    average_rating: float
    review_count: int


class ProductDetailsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    image_url: str
    created_at: datetime

    average_rating: float

    reviews: list[ReviewResponse]



# ======================================
# Product Details Schemas
# ======================================

class ReviewItem(BaseModel):
    id: int
    user: str
    user_id: int
    rating: int
    comment: str
    created_at: datetime


class ProductDetails(BaseModel):
    id: int
    title: str
    description: str
    image_url: str
    average_rating: float
    reviews: list[ReviewItem]


class ReviewWithUserCreate(BaseModel):
    product_id: int
    name: str
    rating: int = Field(..., ge=1, le=5)
    comment: str


# ======================================
# Register & Login Schemas
# ======================================


class RegisterUser(BaseModel):
    name: str

    email: EmailStr

    password: str


class LoginUser(BaseModel):
    email: EmailStr

    password: str


class TokenResponse(BaseModel):

    access_token: str

    token_type: str

    user: UserResponse