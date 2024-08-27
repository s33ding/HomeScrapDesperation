import requests
import boto3
from bs4 import BeautifulSoup
import pandas as pd
import re

# Global variables
url = "https://www.dfimoveis.com.br/aluguel/df/brasilia/asa-norte/apartamento?palavrachave=cln&ordenamento=mais-recente"
response = None
soup = None
listings = None

# Function to scrape apartments and return data as a DataFrame
def scrape_apartments():
    global response, soup, listings
    data = []

    # Send a GET request to fetch the content of the page
    response = requests.get(url)
    
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the apartment listings on the page (new-text phrase contains the main description)
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
                
                # Append data to the list
                data.append({
                    'Description': description,
                    'Apartment Link': link,
                    'Cresci (PK)': creci
                })
    
    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)
    
    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(data)
    
    # Use regex to extract numbers starting with 1, 2, 3, 4, 5, or 7 followed by two digits (e.g., 405)
    df['Address'] = df['Description'].apply(lambda x: re.search(r'\b[1-57]\d{2}\b', x).group() if re.search(r'\b[1-57]\d{2}\b', x) else 'Unknown')
    
    return df


def insert_dataframe_to_dynamodb(df: pd.DataFrame, df_pk_column: str, dynamo_pk_column: str, dynamo_table_name: str):
    """
    Insert data from a pandas DataFrame into a DynamoDB table.

    :param df: The pandas DataFrame containing the data to insert.
    :param df_pk_column: The name of the column in the DataFrame that corresponds to the primary key in DynamoDB.
    :param dynamo_pk_column: The name of the primary key in the DynamoDB table.
    :param dynamo_table_name: The name of the DynamoDB table.
    """
    # Initialize the DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(dynamo_table_name)

    # Iterate through the DataFrame rows and insert each row into DynamoDB
    for index, row in df.iterrows():
        # Ensure the primary key column exists in the DataFrame row
        if df_pk_column not in row or pd.isna(row[df_pk_column]):
            print(f"Skipping row {index}: Missing primary key {df_pk_column}.")
            continue

        # Create an item to insert (ensure to map the correct columns as needed)
        item = {dynamo_pk_column: row[df_pk_column]}

        # Add other columns from the DataFrame to the DynamoDB item
        for col in df.columns:
            if col != df_pk_column:  # Skip the PK column, already added
                item[col] = row[col]

        try:
            # Insert item into DynamoDB table
            response = table.put_item(Item=item)
            print(f"Successfully inserted item {item}")
        except Exception as e:
            print(f"Error inserting item {item}: {e}")

    print(f"Processed {len(df)} items for table {dynamo_table_name}.")



# Scrape apartments and create a DataFrame
df = scrape_apartments()

insert_dataframe_to_dynamodb(df=df, df_pk_column="Cresci (PK)", dynamo_pk_column="pk", dynamo_table_name="apt-scrap")
# Display the DataFrame with the new 'Address' column
print(df)

