from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Start a new instance of Chrome WebDriver
driver = webdriver.Chrome()

# Open the website with the form
driver.get("https://fill.dev/form/registration-username")

xpath_username = '//*[@id="username"]'
xpath_password = '//*[@id="password"]'
xpath_confirm = '//*[@id="password-confirm"]'

xpath_submit = '//*[@id="app"]/main/div/div/div/div/div[2]/form/div[4]/div/button'
xpath_back = '//*[@id="app"]/main/div/div/div/div/div[2]/a'

# Infinite loop to fill and submit the form
while True:
    try:
        # Find the username input field and fill it
        driver.find_element(By.XPATH, xpath_username).send_keys("dedi")
        driver.find_element(By.XPATH, xpath_password).send_keys("abc")
        driver.find_element(By.XPATH, xpath_confirm).send_keys("abc")

        # Click on the submit button
        driver.find_element(By.XPATH, xpath_submit).click()

        # Wait for some time before repeating the loop (you can adjust the delay as needed)
        time.sleep(2)  # Sleep for 5 seconds

        # Go back to form filling page
        driver.find_element(By.XPATH, xpath_back).click()
    except Exception as e:
        print("An error occurred:", e)
