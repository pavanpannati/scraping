from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Set up driver
driver = webdriver.Chrome()  # You can use any browser driver
driver.get("https://services.gst.gov.in/services/searchtpbypan")
excel = "C:\\Users\\Admin\\OneDrive\\Desktop\\truelancer\\1744730310-GST-Level-1.xlsx"
df = pd.read_excel(excel)
column = df.iloc[0:,0]
for i in column:
    if len(str(i))==10:
        # Enter PAN number
        pan_input = driver.find_element(By.ID, "for_gstin")
        pan_input.send_keys(i)  # Replace with actual PAN

        # # Pause to solve captcha manually
        captcha_input = input("Please solve the captcha and press Enter...")
        captcha = driver.find_element(By.ID, "fo-captcha")
        captcha.send_keys(captcha_input)
        # # Click search
        search_button = driver.find_element(By.ID, "lotsearch")
        search_button.click()


        # # Extract results (adjust selectors as needed)
        results = driver.find_elements(By.TAG_NAME, "table")
        print(results)
        for row in results:
            print(row)

        driver.quit()
