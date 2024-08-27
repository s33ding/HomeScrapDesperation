import requests
from bs4 import BeautifulSoup

# Global variables
url = "https://www.dfimoveis.com.br/aluguel/df/brasilia/asa-norte/apartamento?palavrachave=cln&ordenamento=mais-recente"
response = None
soup = None
listings = None

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
            
            # Find the media content (link to the desired page)
            parent_listing = listing.find_next_sibling('div', class_='new-anounce')
            if parent_listing:
                # Extract the apartment link from the previous 'a' tag
                link_tag = listing.find_previous('a', href=True)
                if link_tag:
                    link = "https://www.dfimoveis.com.br" + link_tag['href']  # Ensure the link is complete
                else:
                    link = "No link available"
                
                # Extract the CRECI (real estate registration number)
                creci = parent_listing.find('p').get_text(strip=True)
                
                # Print the details
                print(f"Description: {description}")
                print(f"Apartment Link: {link}")
                print(f"Cresci (PK): {creci}")
                print('-' * 40)
    
    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)

# Scrape apartments
scrape_apartments()

