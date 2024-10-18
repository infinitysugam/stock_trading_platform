import pytest

@pytest.fixture

#1 Test case for setting up a database
def setup_order_database():
    #simulate a database setup
    db = {"orders": []}
    yield db                #give access to the "database" during the test
    db["orders"].clear()    #Clear order after the test (teardown)

#2 Test case for adding an order
def test_add_order(setup_order_database):

    order = {"order_id": 1, "stock" : "APPL", "quantity": 10}
    setup_order_database["orders"].append(order)

    assert len(setup_order_database["orders"]) == 1
    assert setup_order_database["orders"][0]["stock"] == "APPL"

#3 Test case for removing and order
def test_remove_order(setup_order_database):

    order = {"order_id": 1, "stock" : "APPL", "quantity": 10}
    setup_order_database["orders"].append(order)

    assert len(setup_order_database["orders"]) == 1

    setup_order_database["orders"].remove(order)
    assert len(setup_order_database["orders"]) == 0

#4 Test case for multiple orders
def test_multiple_orders(setup_order_database):
    order = [
        {"order_id": 1, "stock" : "APPL", "quantity": 10},
        {"order_id": 2, "stock" : "NVDA", "quantity": 15},
        {"order_id": 3, "stock" : "TSLA", "quantity": 100}
    ]

    setup_order_database["orders"].extend(order)

    assert len(setup_order_database["orders"]) == 3
    assert setup_order_database["orders"][1]["stock"] == "NVDA"
    assert setup_order_database["orders"][2]["quantity"] == 100

#5 Test case for updating an order
def test_update_order(setup_order_database):
    order = {"order_id": 1, "stock" : "APPL", "quantity": 10}
    setup_order_database["orders"].append(order)

    setup_order_database["orders"][0]["quantity"] = 50

    assert setup_order_database["orders"][0]["quantity"] == 50


    

#6 Test case for finding an order by order id
def test_find_order_by_id(setup_order_database):
    order = [
        {"order_id": 1, "stock" : "APPL", "quantity": 10},
        {"order_id": 2, "stock" : "NVDA", "quantity": 15},
        {"order_id": 3, "stock" : "TSLA", "quantity": 100},
        {"order_id": 4, "stock" : "GOOGL", "quantity": 40}
    ]

    setup_order_database["orders"].extend(order)
    order_to_find = next(id for id in setup_order_database["orders"] if id["order_id"] == 4)

    assert order_to_find["quantity"] == 40
    assert order_to_find["order_id"] == 4

#7 Test case for empty order list
def test_empty_order_list(setup_order_database):
    assert len(setup_order_database["orders"]) == 0 

#8 Test case for invalid order handling
def test_invalid_order(setup_order_database):
    # Create an invalid order (missing 'order_id')

    invalid_order = {"stock": "APPL", "quantity" : 40}

    # Ensure adding an invalid order raises an error
    with pytest.raises(KeyError):
        if "order_id" not in invalid_order:
            raise KeyError("Order must have a valid id")
        
        setup_order_database["orders"].append(invalid_order)
    

