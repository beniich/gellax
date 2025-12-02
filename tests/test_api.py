from fastapi.testclient import TestClient
from gellax import api
from gellax import db


client = TestClient(api.app)


def setup_module(module):
    # ensure fresh database for tests
    db.Base.metadata.drop_all(bind=db.engine)
    db.Base.metadata.create_all(bind=db.engine)


def test_create_and_get_product():
    # create a user with manager role directly in db
    from gellax.crud import create_user
    from gellax.security import get_password_hash
    db_session = db.SessionLocal()
    try:
        user = create_user(db_session, type("U", (), {"username": "mgr", "password": "pass", "role": "manager"}))
    finally:
        db_session.close()

    # get token
    r_token = client.post("/auth/token", data={"username": "mgr", "password": "pass"})
    assert r_token.status_code == 200
    token = r_token.json()["access_token"]

    payload = {"name": "Test product", "sku": "TP-001", "price": 9.99, "quantity": 5}
    r = client.post("/products/", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == "Test product"
    pid = data["id"]

    r2 = client.get(f"/products/{pid}")
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2["sku"] == "TP-001"


def test_list_products():
    r = client.get("/products/")
    assert r.status_code == 200
    arr = r.json()
    assert isinstance(arr, list)
