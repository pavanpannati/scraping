import json
import requests
from bs4 import BeautifulSoup
import threading
import pandas as pd
# image scraping from PINTREST
# requirements install
#!pip install requests selenium

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as chromeservice
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import requests
data = []

def bike_post_scrap():
    search = input('Search Post Name : ')     #search image names what you need
    driver = webdriver.Chrome(service=chromeservice("E:\\chromedriver-win64\\chromedriver.exe"))
    #if you doesnot have chrome driver installed you can use below commented code , it might need high speed internet
    #driver = webdriver.Chrome(service=chromeservice(ChromeDriverManager().install()))
    URL = f'https://www.bikewale.com/{search}-bikes/'
    driver.get(URL)
    while True:
        driver.get(URL)
        time.sleep(5)

        if "Page Not Found" in driver.title:
            print(" Page Unavailable ")
            search = input('Search Post Name : ')
            URL = f'https://www.bikewale.com/{search}-bikes/'
            driver.get(URL)
            time.sleep(3)
            continue
        else:
            print("Page Loaded successfully")
        break
    #height of the page at the starting
    last_height = driver.execute_script("return document.body.scrollHeight")
    bike_urls = []
    i=0
    while True:
        #scroll down to bottom
        driver.execute_script(f"window.scrollTo(0,1000+{i});")
        time.sleep(5)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        i+=10
    bike_tags = driver.find_elements(By.XPATH,"//a[@class='o-f o-aF o-jJ o-eQ']")
    # print(post_tags)
    bike_url_duplicate = [post.get_attribute('href') for post in bike_tags]
    bike_urls = list(set(bike_url_duplicate))
    print(len(bike_urls))
    for url in bike_urls:
        bike_scraping(url)
    with open("data.json","w",encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii = False,indent =4)
    print('file saved')
    
def bike_scraping(url):
    
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    
}
    # Send the request
    response = requests.get(url)
    # Parse the HTML
    
    soup = BeautifulSoup(response.content, "html.parser")
    name = soup.find("h1",class_='o-j6 o-jm o-jJ').get_text(strip=True)
    is_available = soup.find("h1",class_='o-j6 o-jm o-jJ').get_text(strip=True)
    color_options = soup.find("div",class_='o-j6 o-jm o-jJ')
    special_features =soup.find("div",class_='o-kY o-mf o-lS o-lX o-mO')
    if special_features !=None:
        special_features=special_features.get_text()
    showroom_price = soup.find("h1",class_='o-j6 o-jm o-jJ').get_text(strip=True)
    rto_charges = soup.find("h1",class_='o-j6 o-jm o-jJ').get_text(strip=True)
    insurance_price = soup.find("h1",class_='o-j6 o-jm o-jJ').get_text(strip=True)
    other_charges = soup.find("h1",class_='o-j6 o-jm o-jJ').get_text(strip=True) 
    on_road_price = soup.find("span",class_='o-j5 o-jl o-js')
    if on_road_price != None:    
        on_road_price=on_road_price.get_text(strip=True)
    min_emi = soup.find("div",class_ = 'o-jJ o-j0 b2q6xz')
    
    loan_interest_rate =soup.find("h1",class_='o-j6 o-jm o-jJ').get_text(strip=True)
    #extract all variants
    # for bike in soup.select('.body-content'):
        # name = bike.select_one('.o-j6 o-jm o-jJ').get_text(strip = True)
        # is_available = bike.select_one().get_text(strip = True)
        # color_options = bike.select_one('.o-jC o-jK    Ahg0iS o-j1 o-jh o-cA o-kY  o-k   o-gI o-cA o-c4 o-bS o-co').get_text(strip = True)
        # special_features =bike.select_one('.o-mO o-m3 o-lZ o-mf o-lS').get_text(strip = True)
        # showroom_price = bike.select_one('.o-j5 o-jl o-js').get_text(strip = True)
        # rto_charges = bike.select_one().get_text(strip = True) or None
        # insurance_price = bike.select_one().get_text(strip = True) or None
        # other_charges = bike.select_one().get_text(strip = True) or None 
        # on_road_price = bike.select_one().get_text(strip = True) or None
        # min_emi = bike.select_one('.o-jJ o-j0 b2q6xz').get_text(strip = True)
        # loan_interest_rate = bike.select_one().get_text(strip = True) or None
    data.append({
        "Name":name,
        "Availability":is_available,
        "Colors":color_options,
        "Features":special_features,
        "Showroom_Price":showroom_price,
        "Rto Charges":rto_charges,
        "Insurance":insurance_price,
        "Other Charges":other_charges,
        "On Road Price":on_road_price,
        "Minimum EMI":min_emi,
        "Loan Rate":loan_interest_rate
    })

    #saving data into json file
    
if __name__ == "__main__":
    bike_post_scrap()
    # url = 'https://www.bikewale.com/ktm-bikes/duke-200/'
    # bike_scraping(url)