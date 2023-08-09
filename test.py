from bs4 import BeautifulSoup
import requests

def get_prices():

        # Save soup to new file
        with open('soup.html', 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')

        # Find the html cards
        card_tags = soup.find_all('div', class_='result-card')

        if card_tags:
            for card in card_tags:
                link_tag = card.find('a', class_=['result-card', 'result-card__highlight'])
                price_tag = card.find('div', class_='listing-price')
                location_tag = card.find('section', class_='card__location')
                title_tag = card.find('h2', class_='l-text l-u-color-neutral-28 l-text--variant-heading-small l-text--weight-medium card__address')
                description_tag = card.find('p', class_='l-text l-u-color-neutral-44 l-text--variant-body-small l-text--weight-regular card__description')
                
                if link_tag and price_tag and location_tag and title_tag and description_tag:
                    link = link_tag['href']
                    price = price_tag.text.strip()
                    location = location_tag.find('h2', class_='l-text l-u-color-neutral-28 l-text--variant-heading-small l-text--weight-medium card__address').text.strip()
                    street = location_tag.find('p', class_='l-text l-u-color-neutral-28 l-text--variant-body-small l-text--weight-regular card__street').text.strip()
                    title = title_tag.text.strip()
                    description = description_tag.text.strip().replace('\n', ' ')[:1000]  # Get the first 1000 characters of the description and replace line breaks with spaces
                    
                    # Create a dictionary that represents the document to insert
                    print
                    doc = {
                        "link": link,
                        "price": price,
                        "location": location,
                        "street": street,
                        "title": title,
                        "description": description,
                     }
                    # Insert the document into the 'listings' collection
                    
                    print(doc)
                else:
                    print("Some data not found.")
        else:
            print("No data found.")
get_prices()