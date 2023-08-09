import requests
import time
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime
from urllib.parse import unquote
import time
import random
import math

class RealEstateScraper:
    def __init__(self, db_name, collection_name):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def get_prices(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Save soup to new file
        with open('soup.html', 'w') as f:
            f.write(str(soup))
        # with open('soup.html', 'r') as f:
        #     soup = BeautifulSoup(f, 'html.parser')

        # Find the html cards
       

         # Find the html cards
        allCards = soup.find_all('div', class_='result-card')

        tags = {
            "link": {
                "selector": ('a', {'class':['result-card','result-card__highlight']}),
                "action": lambda tag: tag['href'],
            },
            "price": {
                "selector": ('div', {'class': 'listing-price'}),
                "action": lambda tag: tag.text.strip(),
            },
            "location": {
                "selector": ('section', {'class': 'card__location'}),
                "action": lambda tag: tag.find('h2', {'class': 'l-text l-u-color-neutral-28 l-text--variant-heading-small l-text--weight-medium card__address'}).text.strip(),
            },
            "title": {
                "selector": ('h2', {'class': 'l-text l-u-color-neutral-28 l-text--variant-heading-small l-text--weight-medium card__address'}),
                "action": lambda tag: tag.text.strip(),
            },
            "description": {
                "selector": ('p', {'class': 'l-text l-u-color-neutral-44 l-text--variant-body-small l-text--weight-regular card__description'}),
                "action": lambda tag: tag.text.strip().replace('\n', ' ')[:1000],
            },
        }
    
            
        for card in allCards:
            for tag_name, tag_index in tags.items():
                tag = card.find(*tag_index['selector'])
                if tag:
                    print(f'{tag_name}: {tag_index["action"](tag)}')
                else:
                    print(f'{tag_name} tag not found.')
       

    def print_documents(self):
        docs = self.collection.find()

        for doc in docs:
            print(doc)

# Create a new scraper

scraper = RealEstateScraper('real_estate', 'listings')

# List of places in Rio de Janeiro
places_rio = [
    {"name": "Laranjeiras", "zone": "Zona Sul", "coordinates": "-22.933207,-43.18473"},
    {"name": "Barra da Tijuca", "zone": "Zona Oeste", "coordinates": "-23.000371,-43.365895"},
    {"name": "Ipanema", "zone": "Zona Sul", "coordinates": "-22.984667,-43.198593"},
    {"name": "Copacabana", "zone": "Zona Sul", "coordinates": "-22.969442,-43.186845"},
    {"name": "Botafogo", "zone": "Zona Sul", "coordinates": "-22.951193,-43.180784"},
    {"name": "Urca", "zone": "Zona Sul", "coordinates": "-22.954378,-43.167588"},
    {"name": "Recreio Dos Bandeirantes", "zone": "Zona Oeste", "coordinates": "-23.017479,-43.46259"},
    {"name": "Centro", "zone": "Zona Central", "coordinates": "-22.916266,-43.191636"}
]

# Function to construct the URLs
def construct_url_final(place, zone, coordinates):
    # Convert the place and zone names to lower case with hyphens instead of spaces
    place_lower = place.lower().replace(" ", "-")
    zone_lower = zone.lower().replace(" ", "-")

    # List of prepositions that should not be capitalized
    prepositions = ["da", "de", "do", "dos"]

    # Capitalize each word in the place name, with spaces instead of hyphens, unless the word is a preposition
    place_capitalized = " ".join(word if word in prepositions else word.capitalize() for word in place.split("-"))

    # Exceptions
    if place_lower == 'barra-da-tijuca':
        place_capitalized = 'Barra da Tijuca'
    if place_lower == 'recreio-dos-bandeirantes':
        place_capitalized = 'Recreio Dos Bandeirantes'

    # Construct the URL
    url = f"https://www.zapimoveis.com.br/venda/imoveis/rj+rio-de-janeiro+{zone_lower}+{place_lower}/?transacao=venda&onde=,Rio%20de%20Janeiro,Rio%20de%20Janeiro,{zone},{place_capitalized},,,neighborhood,BR%3ERio%20de%20Janeiro%3ENULL%3ERio%20de%20Janeiro%3E{zone}%3E{place_capitalized},{coordinates},&pagina=1&precoMinimo=450000&precoMaximo=750000"

    return url

# URL of the webpage you want to access
def check_places(places_rio, min_interval, max_interval):
    for place in places_rio:
        url = construct_url_final(place["name"], place["zone"], place["coordinates"])
        print(url)  # This will print the URL
        scraper.get_prices(url)

        # generate a random number between 0 and 1
        random_number = random.random()

        # get a number from a logarithmic distribution
        # math.log1p function returns the natural logarithm of 1+x (base e)
        # The distribution will be skewed towards the minimum
        skewed_number = math.log1p(random_number)

        # scale this number so that it lies within our desired interval
        interval = min_interval + (max_interval - min_interval) * skewed_number
        print(f"wainting for {interval} seconds")
        # pause for the desired interval
        time.sleep(interval)

# Call the function with minimum and maximum intervals (converted to seconds)
check_places(places_rio, 5, 60)

scraper.print_documents()

