from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional
from sqlalchemy.exc import IntegrityError


def get_product(db: Session, product_id: int) -> Optional[models.Product]:
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[models.Product]:
    return db.query(models.Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: schemas.ProductCreate) -> models.Product:
    db_prod = models.Product(
        name=product.name,
        sku=product.sku,
        description=product.description,
        price=product.price,
        quantity=product.quantity,
        category_id=product.category_id,
    )
    db.add(db_prod)
    db.commit()
    db.refresh(db_prod)
    return db_prod


def update_product(db: Session, db_obj: models.Product, updates: schemas.ProductCreate) -> models.Product:
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_product(db: Session, db_obj: models.Product) -> None:
    db.delete(db_obj)
    db.commit()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed = user.password
    try:
        from .security import get_password_hash

        hashed = get_password_hash(user.password)
    except Exception:
        pass
    db_user = models.User(username=user.username, hashed_password=hashed, role=user.role)
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(db_user)
    return db_user


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()

