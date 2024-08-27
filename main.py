import requests
from bs4 import BeautifulSoup

# Global variables
url = "https://www.dfimoveis.com.br/aluguel/df/brasilia/asa-norte/apartamento?palavrachave=cln&ordenamento=mais-recente"

# Function to scrape apartments
def scrape_apartments():
    global response, soup, listings

    # Send a GET request to fetch the content of the page
    response = requests.get(url)
    
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the apartment listings in the page (new-text phrase contains the main description)
        listings = soup.find_all('div', class_='new-text phrase')
        
        for listing in listings:
            # Extract the description of the apartment
            description = listing.get_text(strip=True)
            
            # Find the media content (link to the desired page and image)
            parent_listing = listing.find_next_sibling('div', class_='new-anounce')
            if parent_listing:
                # Extract the image URL
                image_source = parent_listing.find('source')['srcset']
                
                # Extract the CRECI (primary key or unique identifier for the apartment)
                creci = parent_listing.find('p').get_text(strip=True)
                
                # If there's a link to the page of the apartment, we can extract it
                link_tag = listing.find_previous('a', href=True)
                if link_tag:
                    link = link_tag['href']
                else:
                    link = "No link available"
                
                # Print the details
                print(f"Description: {description}")
                print(f"Image URL: {image_source}")
                print(f"Apartment Link: {link}")
                print(f"Cresci (PK): {creci}")
                print('-' * 40)
    
    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)

# Scrape apartments
scrape_apartments()

# Now response, soup, and listings are globally accessible

