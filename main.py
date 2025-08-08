# scrape_books.py

# Install required libraries (optional for Colab)
!pip install beautifulsoup4 pandas requests

import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL for pagination
base_url = "https://books.toscrape.com/catalogue/page-{}.html"
all_books = []

# Loop through all 50 pages
for page in range(1, 51):
    print(f"Scraping page {page}")
    res = requests.get(base_url.format(page))
    soup = BeautifulSoup(res.text, 'html.parser')
    
    books = soup.select(".product_pod")
    
    for book in books:
        title = book.h3.a["title"]
        price = book.select_one(".price_color").text.strip()
        rating = book.p["class"][1]
        in_stock = "In stock" in book.select_one(".availability").text.strip()
        book_link = "https://books.toscrape.com/catalogue/" + book.h3.a["href"]
        image_url = "https://books.toscrape.com/" + book.img["src"].replace("../", "")
        
        all_books.append({
            "Title": title,
            "Price": price,
            "Rating": rating,
            "In Stock": in_stock,
            "Product Link": book_link,
            "Image URL": image_url
        })

# Convert to DataFrame and export
df = pd.DataFrame(all_books)
df.to_csv("books.csv", index=False)
df.to_json("books.json", orient='records', indent=2)

# Optional: download files in Colab
from google.colab import files
files.download("books.csv")
files.download("books.json")
