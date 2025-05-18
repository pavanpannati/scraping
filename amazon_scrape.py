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
def post_url_scraping():
    search = input('Search Post Name : ')     #search image names what you need
    post_count = int(input('Number of URLs stored : '))   #search images how many you need
    driver = webdriver.Chrome(service=chromeservice("E:\\chromedriver-win64\\chromedriver.exe"))
    #if you doesnot have chrome driver installed you can use below commented code , it might need high speed internet
    #driver = webdriver.Chrome(service=chromeservice(ChromeDriverManager().install()))
    URL = f'https://www.amazon.in/s?k={search}&sprefix={search}%2Caps%2C304&ref=noss_2'
    #https://www.amazon.in/s?k=headphones&crid=222LL1B7AEJAB&sprefix=headphone%2Caps%2C426&ref=nbnoss_2

    driver.get(URL)
    while True:
        driver.get(URL)
        time.sleep(5)

        if "503" in driver.title or "Service Unavailable" in driver.title:
            print("503 error, Page Unavailable ")
            print("Page Refreshing .....")
            driver.refresh()
            time.sleep(3)
            continue
        else:
            print("Page Loaded successfully")
            break
    post_urls = []
    #scroll page for 3 times with time 1 second delay
    while len(post_urls) <= post_count:
        driver.execute_script("window.scrollBy(0,1000);")
        time.sleep(10)

        #get post urls

        post_tags = driver.find_elements(By.XPATH,"//a[@class='a-link-normal s-no-outline']")
        # print(post_tags)
        post_url_duplicate = [post.get_attribute('href') for post in post_tags]
        post_urls = list(set(post_urls))+list(set(post_url_duplicate))
        print(len(post_urls))
    driver.close()
    if post_urls:
        for url in post_urls:
            post_scraping(url)
    
    
            
def post_scraping(url):
    
    title_list = []
    price_list = []
    image_tag_list = []
    discount_tag_list = []
    # Use headers to avoid getting blocked
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/125.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }


    # Send the request
    response = requests.get(url, headers=headers)
    # Parse the HTML
    soup = BeautifulSoup(response.content, "html.parser")
    # Extract product title
    title = soup.find(id="productTitle")
    image_tag = soup.find("img", {"id": "landingImage"})
    discount_tag = soup.find("span", class_="savingsPercentage")
    price = soup.find("span", class_="a-price-whole")
    # if discount_tag:
    #     discount_tag = discount_tag.get_text(strip=True) if discount_tag else None
    # else:
    #     discount_tag = None

    # # --- Amazon Price (Deal Price) ---
    # deal_price_tag = soup.find("span", class_="a-price aok-align-center reinventPricePriceToPayMargin priceToPay")
    # if deal_price_tag:
    #     deal_price = deal_price_tag.find("span", class_="a-offscreen")
    #     deal_price = deal_price.get_text(strip=True) if deal_price else None
    # else:
    #     deal_price = None

    # # --- Convert prices to float for discount calculation ---
    # def parse_price(price_str):
    #     if price_str:
    #         return float(price_str.replace("₹", "").replace(",", "").strip())
    #     return None

    # original = parse_price(original_price)

    # # --- Discount Calculation ---
    # if original and deal:
    #     discount_percentage = round((original - deal) / original * 100, 2)
    # else:
    #     discount_percentage = None



    if title:
        title_list.append(title.get_text(strip=True))
        print("Title:", title.get_text(strip=True))
    if image_tag:
        image_url = image_tag.get("src")
        image_tag_list.append(image_url)
        print("Image URL:", image_url)
    else:
        print("Image not found.")
    # Extract price
    # --- Print Results ---
    price_list.append(price.get_text(strip=True).replace(",",""))
    print("Price:",price.get_text(strip=True).replace(",","") or "Not found")
    # print("Amazon Price:", price or "Not found")
    discount_tag_list.append(discount_tag.get_text(strip=True).replace("-",""))
    print("Discount %:", discount_tag.get_text(strip=True).replace("-",""))

    #save data to excel
    data = {
        "Title":title_list,
        "Price": price_list,
        "Image URL":image_tag_list,
        "Discount":discount_tag_list,
    }
    df = pd.DataFrame(data)
    df.to_csv("amazon posts.csv",index = True)
if __name__ == "__main__":
    post_url_scraping()