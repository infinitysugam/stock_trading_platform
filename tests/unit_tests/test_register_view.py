import pytest
import os
import sys
from django.urls import reverse
from django.test import Client
import django
import re


# Add project root to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_trading.settings')  # Update with your project's settings file

django.setup()

@pytest.mark.django_db
def test_register_valid_user():
    client = Client()
    url = reverse('register')  # Replace with your actual register URL name
    response = client.post(url, {
        'username': 'validuser',
        'password1': 'StrongPassword123',
        'password2': 'StrongPassword123'
    })
    
    # Print the response content to inspect it
    print(response.content.decode())  # Decode response content to see the actual HTML.

    # Check if the register was successful (Assuming redirect after successful register)
    assert response.status_code == 302
    assert '/login/' in response.url  # Replace '/success/' if the redirect URL differs.


@pytest.mark.django_db
def test_register_invalid_password():
    client = Client()
    url = reverse('register')  #  URL name
    response = client.post(url, {
        'username': 'validuser',
        'password1': '123',  # Too short password
        'password2': '123'
    })
    
    # Print the response content to inspect it
    print(response.content.decode())  # Decode response content to see the actual HTML.

    # Check for the error message in the form
    assert response.status_code == 200
    assert 'This password is too short' in str(response.content)


@pytest.mark.django_db
def test_register_mismatched_passwords():
    client = Client()
    url = reverse('register')  # Replace with your actual URL name
    response = client.post(url, {
        'username': 'validuser',
        'password1': 'StrongPassword123',
        'password2': 'DifferentPassword'
    })

    # Print the response content to inspect it
    print(response.content.decode())  # Decode response content to see the actual HTML.

    # Check if the correct error is raised for mismatched passwords
    assert response.status_code == 200
    # assert "The two password fields didn't match." in str(response.content)
    assert re.search(r"The two password fields didn[’']t match\.", response.content.decode())






