import requests
from bs4 import BeautifulSoup
import json

brand = ('Ampere',
'Aprilia',
'Ather',
'Avan Motors',
'Avanturaa Choppers',
'Bajaj',
'Benelli',
'Benling',
'BGauss',
'BMW',
'Bounce',
'Brixton Motorcycles',
'BSA',
'CFMoto',
'Cleveland CycleWerks',
'Ducati',
'Evolet',
'FB Mondial',
'Ferrato',
'Gemopai',
'Harley-Davidson',
'Hero',
'Hero Electric',
'Hero Honda',
'Honda',
'Hop Electric',
'Husqvarna',
'Hyosung',
'Indian',
'iVOOMi',
'Jawa',
'Joy e-bike',
'Kawasaki',
'Keeway',
'Kinetic Green',
'KTM',
'Lambretta',
'Lectrix',
'LML',
'Mahindra',
'Matter',
'Moto Guzzi',
'Moto Morini',
'MV Agusta',
'Norton',
'Numeros Motors',
'Oben',
'Odysse',
'Okaya',
'Okinawa',
'OLA',
'PURE EV',
'QJ Motor',
'Quantum Energy',
'Revolt',
'River',
'Royal Enfield',
'Simple Energy,'
'Suzuki',
'SWM',
'Techo Electra',
'Tork',
'Triumph',
'TVS',
'Ultraviolette',
'UM',
'Vespa',
'VIDA',
'Yamaha',
'Yezdi',
'Yo',
'Zontes')
city = ('Mumbai',
'Bangalore',
'Delhi'
'Pune',
'Navi Mumbai',
'Hyderabad',
'Ahmedabad',
'Chennai',
'Kolkata',
'Chandigarh')
data = []
posts = 0       
def scrap(URL,brand,city):
    response = requests.get(URL)

    soup = BeautifulSoup(response.content,"html.parser")
    content = soup.find_all('div',class_='lSq7kt')


    for i in content:
        title = i.find('h3')
        address = i.find('p',class_='o-j1 o-jJ o-ei o-jz o-f5')
        mobile_number = i.find('p',class_='o-j1 o-js o-os o-jK')
        
        if title != None:
            title = title.get_text()
        if address != None:
            address = address.get_text()
        if not mobile_number:
            mobile_number = i.find('p',class_='o-j1 o-js o-os o-jK o-c6')
        mobile_number =mobile_number.get_text() if mobile_number else None
        print(title)
        print(address)
        print(mobile_number)
        entry = ({
        "Brand":brand,
        "City":city,
        "Title": title,
        "Address": address,
        "Mobile Number": mobile_number
    })
        if entry not in data and title!=None:
            data.append(entry)
        
for i in brand:
    for j in city:
        URL = f'https://www.bikewale.com/dealer-showrooms/{i}/{j}/'
        scrap(URL,i,j) 
        posts += 1
    print(posts)
with open("bikewale brands.json","w",encoding='utf-8') as f:
    json.dump(data,f,ensure_ascii = False,indent =4)

print(posts,"saved in json file ")