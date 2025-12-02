"""FastAPI application and routes for Gellax."""
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import db, crud, schemas
from . import security
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI(title="Gellax Merchandise API")


def get_db():
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


@app.on_event("startup")
def on_startup():
    db.init_db()


@app.post("/auth/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = security.create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users/", response_model=schemas.UserRead)
def create_user_endpoint(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # For simplicity allow creation; in production restrict to admins or setup flow
    return crud.create_user(db, user)


@app.post("/products/", response_model=schemas.ProductRead)
def create_product_endpoint(product: schemas.ProductCreate, db: Session = Depends(get_db), _=Depends(security.require_role("admin","manager"))):
    return crud.create_product(db, product)


@app.get("/products/", response_model=list[schemas.ProductRead])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_products(db, skip=skip, limit=limit)


@app.get("/products/{product_id}", response_model=schemas.ProductRead)
def get_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    prod = crud.get_product(db, product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return prod


@app.put("/products/{product_id}", response_model=schemas.ProductRead)
def update_product_endpoint(product_id: int, updates: schemas.ProductCreate, db: Session = Depends(get_db), _=Depends(security.require_role("admin","manager"))):
    prod = crud.get_product(db, product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud.update_product(db, prod, updates)


@app.delete("/products/{product_id}")
def delete_product_endpoint(product_id: int, db: Session = Depends(get_db), _=Depends(security.require_role("admin","manager"))):
    prod = crud.get_product(db, product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    crud.delete_product(db, prod)
    return {"ok": True}
