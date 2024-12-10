import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

@pytest.fixture
def driver():
    # Use webdriver-manager to handle the ChromeDriver installation
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()

def test_order_management(driver):
    wait = WebDriverWait(driver, 20)  # wait for a maximum of 20 seconds for elements to appear

    try:
        # Step 1: Login to the system
        driver.get('http://127.0.0.1:8000/login/')
        
        # Wait for username and password fields to be visible
        username_input = wait.until(EC.visibility_of_element_located((By.NAME, 'username')))
        password_input = wait.until(EC.visibility_of_element_located((By.NAME, 'password')))
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))

        # Fill in the login credentials (Replace with valid credentials)
        username_input.send_keys('admin')  # Replace with your actual username
        password_input.send_keys('admin')  # Replace with your actual password
        login_button.click()

        # Wait for a successful redirect to the dashboard or home page after login
        wait.until(lambda driver: driver.current_url != 'http://127.0.0.1:8000/login/')

        # Step 2: Access the order management page after logging in
        driver.get('http://127.0.0.1:8000/order_management/')

        # Verify that we are on the correct page
        assert driver.current_url == 'http://127.0.0.1:8000/order_management/', "Failed to navigate to order management page"

        # Step 3: Interact with the order management page
        # Wait for the dropdown to be present in the DOM and be visible
        instrument_dropdown = wait.until(EC.visibility_of_element_located((By.ID, 'instrument')))
        instrument_dropdown.click()

        # Select the desired instrument
        instrument_option = driver.find_element(By.XPATH, "//option[@value='GBP_USD']")
        instrument_option.click()

        # Place Buy Order
        driver.find_element(By.ID, 'buy').click()
        price_input = driver.find_element(By.ID, 'price')
        quantity_input = driver.find_element(By.ID, 'quantity')
        submit_button = driver.find_element(By.CSS_SELECTOR, '.btn-submit')

        # Fill in the price and quantity and click submit
        price_input.send_keys('1.25000')
        quantity_input.send_keys('100')
        submit_button.click()

        # Wait to ensure the server has time to process the request
        time.sleep(2)

        # Check transaction history by waiting for the transaction history container to be visible
        transaction_history_table = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.transaction-history tbody')))
        rows = transaction_history_table.find_elements(By.TAG_NAME, 'tr')

        # Validate that there is at least one transaction recorded in history
        assert len(rows) > 1, "No transactions recorded in the history"  # At least one order should be recorded
        last_row = rows[-2]  # Getting the last order row excluding the 'No orders found.' row if it exists
        cells = last_row.find_elements(By.TAG_NAME, 'td')

        # Asserting if the recorded order matches the inputs
        assert cells[0].text == 'Buy', f"Expected 'Buy', got {cells[0].text}"
        assert cells[1].text == 'GBP/USD', f"Expected 'GBP/USD', got {cells[1].text}"
        assert cells[2].text == '1.25000', f"Expected '1.25000', got {cells[2].text}"
        assert cells[3].text == '100', f"Expected '100', got {cells[3].text}"

    except Exception as e:
        print("An error occurred:", e)
        assert False, f"Test failed due to an exception: {e}"

