# image scraping from PINTREST
# requirements install
#!pip install requests selenium

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as chromeservice
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import requests

search = input('Search Images : ')     #search image names what you need
images_count = int(input('Number of Images Downloaded : '))   #search images how many you need
driver = webdriver.Chrome(service=chromeservice("E:\\chromedriver-win64\\chromedriver.exe"))
#if you doesnot have chrome driver installed you can use below commented code , it might need high speed internet
#driver = webdriver.Chrome(service=chromeservice(ChromeDriverManager().install()))
URL = f'https://in.pinterest.com/search/pins/?q={search}&rs=autocomplete_bubble&b_id=BF8EaZQQ6XHOAAAAAAAAAAALis344AohI_ad3R-r068A-Gh6ML70ygUq9g_rAAO0lNVTL8nwo6lPncrZ4UTdeIznbfO4Nw7g_nfiLrSKq0myEv3MCJr6TV8&source_id=Q7iDh4c0&top_pin_id=2533343532482543'


driver.get(URL)
image_urls = []
#scroll page for 3 times with time 1 second delay
while len(image_urls) <= images_count:
    driver.execute_script("window.scrollBy(0,1000);")
    time.sleep(10)

    #get image urls

    image_tags = driver.find_elements(By.XPATH,"//img[@class='hCL kVc L4E MIw']")
    image_url_duplicate = [img.get_attribute('src') for img in image_tags]
    image_urls = list(set(image_urls))+list(set(image_url_duplicate))
    print(len(image_urls))
print(len(image_urls))
#Downloading images

for index,img in enumerate(image_urls):
    response = requests.get(img,stream=True)
    with open(f'{search}-{index+1}.jpg','wb') as f:
        for chunk in response.iter_content(chunk_size=128):
            f.write(chunk) 
print(f'{len(image_urls)} Images Downloaded')
driver.close()


