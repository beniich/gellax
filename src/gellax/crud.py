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


def create_warehouse(db: Session, w: schemas.WarehouseCreate) -> models.Warehouse:
    db_w = models.Warehouse(name=w.name, location=w.location)
    db.add(db_w)
    db.commit()
    db.refresh(db_w)
    return db_w


def get_warehouse(db: Session, warehouse_id: int) -> Optional[models.Warehouse]:
    return db.query(models.Warehouse).filter(models.Warehouse.id == warehouse_id).first()


def list_warehouses(db: Session, skip: int = 0, limit: int = 100) -> list[models.Warehouse]:
    return db.query(models.Warehouse).offset(skip).limit(limit).all()


def get_inventory(db: Session, product_id: int, warehouse_id: int) -> Optional[models.Inventory]:
    return (
        db.query(models.Inventory)
        .filter(models.Inventory.product_id == product_id, models.Inventory.warehouse_id == warehouse_id)
        .first()
    )


def create_or_adjust_inventory(db: Session, product_id: int, warehouse_id: int, quantity: int) -> models.Inventory:
    inv = get_inventory(db, product_id, warehouse_id)
    if inv:
        inv.quantity = inv.quantity + quantity
        db.add(inv)
        db.commit()
        db.refresh(inv)
        return inv
    inv = models.Inventory(product_id=product_id, warehouse_id=warehouse_id, quantity=quantity)
    db.add(inv)
    db.commit()
    db.refresh(inv)
    return inv


def create_movement(db: Session, m: schemas.MovementCreate) -> models.InventoryMovement:
    mv = models.InventoryMovement(
        product_id=m.product_id,
        from_warehouse_id=m.from_warehouse_id,
        to_warehouse_id=m.to_warehouse_id,
        quantity=m.quantity,
        note=m.note,
    )
    db.add(mv)
    # apply inventory changes
    if m.from_warehouse_id:
        create_or_adjust_inventory(db, m.product_id, m.from_warehouse_id, -m.quantity)
    if m.to_warehouse_id:
        create_or_adjust_inventory(db, m.product_id, m.to_warehouse_id, m.quantity)
    db.commit()
    db.refresh(mv)
    return mv


def list_movements(db: Session, product_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> list[models.InventoryMovement]:
    q = db.query(models.InventoryMovement)
    if product_id:
        q = q.filter(models.InventoryMovement.product_id == product_id)
    return q.offset(skip).limit(limit).all()

