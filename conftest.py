import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="session")
def driver():
    chrome_options = Options()
    
    # ASSIGNMENT REQUIREMENT: Headless Mode for Jenkins/EC2
    chrome_options.add_argument("--headless=new")
    
    # Required to prevent memory crashes on Linux servers
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Auto-download and manage the Chrome driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Give React elements up to 5 seconds to load
    driver.implicitly_wait(5)
    
    yield driver
    
    # Close the hidden browser when tests finish
    driver.quit()