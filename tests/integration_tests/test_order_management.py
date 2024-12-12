import pytest
import os
import django
from django.urls import reverse
from django.test import Client

# Set up Django environment for testing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_trading.settings')
django.setup()

@pytest.mark.django_db
def test_load_order_management_page():
    client = Client()
    url = reverse('order_management')  # Update with correct URL name if needed
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_select_instrument():
    client = Client()
    url = reverse('order_management')
    response = client.get(url, {'instrument': 'EUR_USD'})
    assert response.status_code == 200
    assert b'EUR/USD' in response.content

@pytest.mark.django_db
def test_place_buy_order():
    client = Client()
    url = reverse('order_management')
    response = client.post(url, {
        'instrument': 'EUR_USD',
        'order_type': 'buy',
        'price': '1.12345',
        'quantity': '100'
    })
    assert response.status_code == 302  # Assuming redirect on successful order

@pytest.mark.django_db
def test_place_sell_order():
    client = Client()
    url = reverse('order_management')
    response = client.post(url, {
        'instrument': 'EUR_USD',
        'order_type': 'sell',
        'price': '1.12345',
        'quantity': '100'
    })
    assert response.status_code == 302  # Assuming redirect on successful order

@pytest.mark.django_db
def test_transaction_history():
    client = Client()
    url = reverse('order_management')
    response = client.get(url)
    assert response.status_code == 200
    assert b'Transaction History' in response.content
