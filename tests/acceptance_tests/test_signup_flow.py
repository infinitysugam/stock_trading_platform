import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def browser():
    # Setup: Start a Chrome browser instance
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("http://localhost:8000/register")  # Use the correct URL for signup
    yield driver
    # Teardown: Quit the browser after each test
    driver.quit()

def test_signup_valid_user(browser):
    # Wait for the username input field to be clickable
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.NAME, "username")))

    # Find the form elements
    username = browser.find_element(By.NAME, "username")
    password1 = browser.find_element(By.NAME, "password1")
    password2 = browser.find_element(By.NAME, "password2")

    # Fill out the form with valid credentials
    username.send_keys("validuser")
    password1.send_keys("StrongPassword123")
    password2.send_keys("StrongPassword123")
    password2.send_keys(Keys.RETURN)

    # Wait for the success message to appear
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, "messages")))

    # Check that the success message appears
    assert "Signup Successful" in browser.page_source

def test_signup_invalid_password(browser):
    # Wait for the username input field to be clickable
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.NAME, "username")))

    # Find the form elements
    username = browser.find_element(By.NAME, "username")
    password1 = browser.find_element(By.NAME, "password1")
    password2 = browser.find_element(By.NAME, "password2")

    # Fill out the form with a password that's too short
    username.send_keys("validuser")
    password1.send_keys("123")  # Too short password
    password2.send_keys("123")
    password2.send_keys(Keys.RETURN)

    # Wait for the error message to appear
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, "messages")))

    # Check that the proper error message appears
    assert "There was an error with your submission." in browser.page_source
