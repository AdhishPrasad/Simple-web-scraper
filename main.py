import requests
from bs4 import BeautifulSoup

def scrape_texts(url, tag, class_name=None, label="Items"):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    elements = soup.find_all(tag, class_=class_name) if class_name else soup.find_all(tag)
    
    print(f"\n{label}:")
    for idx, element in enumerate(elements[:10], 1):
        print(f"{idx}. {element.text.strip()}")

scrape_texts('https://www.bbc.com/news', 'h3', label="Headlines")
scrape_texts('http://quotes.toscrape.com/', 'span', class_name='text', label="Quotes")
