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


class WarehouseCreate(BaseModel):
    name: str
    location: Optional[str] = None


class WarehouseRead(BaseModel):
    id: int
    name: str
    location: Optional[str]

    class Config:
        orm_mode = True


class InventoryCreate(BaseModel):
    product_id: int
    warehouse_id: int
    quantity: int


class InventoryRead(BaseModel):
    id: int
    product_id: int
    warehouse_id: int
    quantity: int

    class Config:
        orm_mode = True


class MovementCreate(BaseModel):
    product_id: int
    from_warehouse_id: Optional[int] = None
    to_warehouse_id: Optional[int] = None
    quantity: int
    note: Optional[str] = None


class MovementRead(BaseModel):
    id: int
    product_id: int
    from_warehouse_id: Optional[int]
    to_warehouse_id: Optional[int]
    quantity: int
    note: Optional[str]

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
