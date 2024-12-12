import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_trading.settings')

import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from portfolio_management.models import AmountDetails, Portfolio

django.setup()

@pytest.mark.django_db
def test_deposit_amount(client):
    # Create a test user
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')
    
    # Make a POST request to deposit amount
    response = client.post(reverse('portfolio_management'), {'deposit_amount': 100})
    
    # Fetch the updated cash amount
    deposit = AmountDetails.objects.get(user=user)
    
    # Assertions
    assert response.status_code == 302  # Redirect after successful deposit
    assert deposit.cash_amount == 100

@pytest.mark.django_db
def test_invalid_deposit_amount(client):
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')
    
    # Attempt to deposit an invalid amount
    response = client.post(reverse('portfolio_management'), {'deposit_amount': -100})
    
    # Assertions
    assert response.status_code == 200  # Page reloads with an error
    assert b"Deposit amount must be greater than zero." in response.content

@pytest.mark.django_db
def test_portfolio_display(client):
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')
    
    # Create portfolio data
    Portfolio.objects.create(user=user, instrument="EUR_USD", quantity=100, average_price=1.1)
    
    # Access the portfolio page
    response = client.get(reverse('portfolio_management'))
    
    # Assertions
    assert response.status_code == 200
    assert b"EUR_USD" in response.content
    assert b"100" in response.content

@pytest.mark.django_db
def test_notifications(client):
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')
    
    # Perform an action that triggers a notification
    client.post(reverse('portfolio_management'), {'deposit_amount': 50})
    
    # Check for notifications
    response = client.get(reverse('portfolio_management'))
    assert b"$50 Amount Deposited in the platform." in response.content

@pytest.mark.django_db
def test_cash_allocation_graph(client):
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')
    
    # Create data
    AmountDetails.objects.create(user=user, cash_amount=500, used_amount=300)
    Portfolio.objects.create(user=user, instrument="EUR_USD", quantity=100, average_price=1.2)
    
    # Access the graph endpoint
    response = client.get(reverse('cash_allocation_graph'))
    
    # Assertions
    assert response.status_code == 200
    assert b'"name": "EUR_USD"' in response.content
    assert b'"name": "Cash"' in response.content
