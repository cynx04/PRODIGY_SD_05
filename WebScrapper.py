import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the Amazon page to scrape
URL = "https://www.amazon.in/s?k=laptops+under+70000&crid=20WQBNSLP9R3F&sprefix=%2Caps%2C374&ref=nb_sb_ss_recent_1_0_recent"

# Function to get the HTML content of the page
def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.5"
    }
    response = requests.get(url, headers=headers)
    return response.text

# Function to parse the HTML content and extract product information
def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    products = []

    for item in soup.select('.s-result-item'):
        name = item.select_one('h2 .a-link-normal.a-text-normal')
        price_whole = item.select_one('.a-price-whole')
        price_fraction = item.select_one('.a-price-fraction')
        rating = item.select_one('.a-icon-alt')

        if name and price_whole and rating:
            name = name.get_text(strip=True)
            price = "f{price_whole.get_text(strip=True)}.{price_fraction.get_text(strip=True)}"
            rating = rating.get_text(strip=True)

            products.append({
                'name': name,
                'price': price,
                'rating': rating
            })

    return products

# Function to save the extracted product information to a CSV file
def save_to_csv(products, filename='C:\\Users\\USER\\OneDrive\\Documents\\Prodigy\\WebScrapper\\products.csv'):
    df = pd.DataFrame(products)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Main script
html_content = get_html(URL)
products = parse_html(html_content)
save_to_csv(products)
