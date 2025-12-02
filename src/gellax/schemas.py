from pydantic import BaseModel
from typing import Optional


class CategoryCreate(BaseModel):
    name: str


class CategoryRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class ProductCreate(BaseModel):
    name: str
    sku: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = 0.0
    quantity: Optional[int] = 0
    category_id: Optional[int] = None


class ProductRead(BaseModel):
    id: int
    name: str
    sku: Optional[str]
    description: Optional[str]
    price: Optional[float]
    quantity: int
    category_id: Optional[int]

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    password: str
    role: Optional[str] = "viewer"


class UserRead(BaseModel):
    id: int
    username: str
    is_active: bool
    role: str

    class Config:
        orm_mode = True
