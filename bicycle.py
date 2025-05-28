import requests
from bs4 import BeautifulSoup
import threading
from selenium.webdriver.chrome.options import Options
# image scraping from PINTREST
# requirements install
#!pip install requests selenium

from random import uniform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as chromeservice
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import requests

url = []
data = []
cycles = 0

brands =[
        'BSA',
        'Hercules'
        'Hero',
        'Hero Lectro',
        'Ninety One',
        'Avon',
        'Firefox',
        'MACH City',
        'Montra',
            ]
base_url = f'https://www.bicyclesdekho.com/'
def post_url_scraping():
    
    # options = Options()
    # options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")


    # driver = webdriver.Chrome(service=chromeservice("E:\\chromedriver-win64\\chromedriver.exe"),options=options)
    # #if you doesnot have chrome driver installed you can use below commented code , it might need high speed internet
    # #driver = webdriver.Chrome(service=chromeservice(ChromeDriverManager().install()))
    
    for brand in brands:
        URL = f'https://www.bicyclesdekho.com/{brand}'
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "DNT": "1",  # Do Not Track
        "Referer": "https://www.google.com/",  # Optional but helps
    }
        response = requests.get(URL,headers=headers)
        time.sleep(uniform(1.5,4))
        soup = BeautifulSoup(response.text,'html.parser')
        print(soup)
        app_content= soup.find('div',class_='app-content')

        if app_content:
        
            urls = [i['href'] for i in app_content.find_all('a',class_='slink')]
            urls= [i for i in urls]
            for i in urls:
                url.append(base_url+i)
        # for i in urls:
            
        #     if type(i) != str:
        #         print(i.get_attribute('href'))
        #         if i.get_attribute('href') != None:
        #             url.append(i.get_attribute('href'))
    print(url)
    print(len(url))
    #driver.close()

def bicycle_scraping(url):
        
    URL = f'{url}'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "DNT": "1",  # Do Not Track
        "Referer": "https://www.google.com/",  # Optional but helps
    }
    
    response = requests.get(URL,headers=headers)
    time.sleep(uniform(1.5,4))
    soup = BeautifulSoup(response.content,'html.parser')
    description = soup.find('p')
    description = description.get_text() if description else None
    img_url = soup.find_all('img')
    img_url = [i['src'] for i in img_url]
    img_url = img_url[1] if len(img_url)>0 else None
    
    URL = f'{url}/specifications'
    response = requests.get(URL,headers=headers)
    time.sleep(uniform(1.5,4))
    soup = BeautifulSoup(response.content,'html.parser')
    print(soup.text)
    title = soup.find('h1')
    title = title.get_text() if title else None
    
    price = soup.find('div',class_='price')
    price = price.get_text() if price else None
    # specs = soup.find_all('td',class_='right') 
    # specs = [i.get_text() for i in specs] if specs else None
    app_content= soup.find('div',class_='app-content')
    gears=None
    key1 = None
    values = None
    
    if app_content:
        for i in app_content:
            result = i.find(id='scrollDiv')
            key1 = result.find_all('span')
            key1 = [j.get_text() for j in key1]
            gears = result.find_all('h3')
            gears = [j.get_text() for j in gears]
            key1 = [r for r in key1 if r not in gears]
            values = result.find_all('td')
            for val in values:
                if values:
                    for span in val.find_all('span'):
                        span.decompose()
            values = [j.get_text() for j in values if j.get_text() !='' ]

        
    entry = ({
        
        "Title":title,
        "Description":description,
        "Image URL":img_url,
        "Price Starts From":price,
        'Gears':dict(zip(values[:2],key1[:2])),
        'Wheels':dict(zip(values[2:6],key1[2:6])),
        'Front part of cycle':dict(zip(values[6:12],key1[6:12])) ,
        'Back part of cycle':dict(zip(values[12:20],key1[12:20])),
        'Others':dict(zip(values[20:],key1[20:])),
    })
    
    data.append(entry) 
    print(entry)
    print(len(data))     
post_url_scraping()

import re
url_pattern = re.compile(r'https?://|www\.')

filtered_list = [item for item in url if url_pattern.search(item)] 
for i in filtered_list:
    bicycle_scraping(i) 

import json
with open("bicycle dekho.json","w",encoding='utf-8') as f:
    json.dump(data,f,ensure_ascii = False,indent =4) 

print("files saved")