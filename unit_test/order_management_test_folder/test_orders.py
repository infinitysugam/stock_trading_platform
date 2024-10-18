import pytest

@pytest.fixture

def setup_order_database():
    #simulate a database setup
    db = {"orders": []}
    yield db                #give access to the "database" during the test
    db["orders"].clear()    #Clear order after the test (teardown)

def test_add_order(setup_order_database):

    order = {"order_id": 1, "stock" : "APPL", "quantity": 10}
    setup_order_database["orders"].append(order)

    assert len(setup_order_database["orders"]) == 1
    assert setup_order_database["orders"][0]["stock"] == "APPL"


