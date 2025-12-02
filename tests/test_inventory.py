from fastapi.testclient import TestClient
from gellax import api, db, models
from gellax.security import get_password_hash

client = TestClient(api.app)


def setup_module(module):
    db.Base.metadata.drop_all(bind=db.engine)
    db.Base.metadata.create_all(bind=db.engine)


def test_warehouse_and_movement_flow():
    # create manager
    db_session = db.SessionLocal()
    try:
        hashed = get_password_hash("pass")
        u = models.User(username="mgr2", hashed_password=hashed, role="manager")
        db_session.add(u)
        db_session.commit()
    finally:
        db_session.close()

    # get token
    r_token = client.post("/auth/token", data={"username": "mgr2", "password": "pass"})
    assert r_token.status_code == 200
    token = r_token.json()["access_token"]

    # create product
    prod = client.post("/products/", json={"name": "ProdA"}, headers={"Authorization": f"Bearer {token}"})
    assert prod.status_code == 200
    pid = prod.json()["id"]

    # create warehouses
    w1 = client.post("/warehouses/", json={"name": "W1"}, headers={"Authorization": f"Bearer {token}"})
    w2 = client.post("/warehouses/", json={"name": "W2"}, headers={"Authorization": f"Bearer {token}"})
    assert w1.status_code == 200 and w2.status_code == 200
    w1_id = w1.json()["id"]
    w2_id = w2.json()["id"]

    # add stock to W1
    mv_in = client.post("/movements/", json={"product_id": pid, "to_warehouse_id": w1_id, "quantity": 10}, headers={"Authorization": f"Bearer {token}"})
    assert mv_in.status_code == 200

    # transfer 3 from W1 to W2
    mv_trans = client.post("/movements/", json={"product_id": pid, "from_warehouse_id": w1_id, "to_warehouse_id": w2_id, "quantity": 3}, headers={"Authorization": f"Bearer {token}"})
    assert mv_trans.status_code == 200

    # check inventories via direct DB (simpler for test)
    s = db.SessionLocal()
    try:
        inv_w1 = s.query(models.Inventory).filter(models.Inventory.product_id == pid, models.Inventory.warehouse_id == w1_id).first()
        inv_w2 = s.query(models.Inventory).filter(models.Inventory.product_id == pid, models.Inventory.warehouse_id == w2_id).first()
        assert inv_w1 is not None and inv_w1.quantity == 7
        assert inv_w2 is not None and inv_w2.quantity == 3
    finally:
        s.close()
