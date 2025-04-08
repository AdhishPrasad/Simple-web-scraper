from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    products = []
    if request.method == 'POST':
        query = request.form['query']
        site = request.form['site']

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9"
        }

        if site == 'snapdeal':
            url = f"https://www.snapdeal.com/search?keyword={query.replace(' ', '%20')}"
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.select('div.product-tuple-listing')

            for item in items[:5]:
                title = item.select_one('.product-title')
                price = item.select_one('.product-price')
                image = item.select_one('img.product-image')

                if title and price and image:
                    products.append({
                        'title': title.text.strip(),
                        'price': price.text.strip(),
                        'image': image['src'] if image.has_attr('src') else 'https://via.placeholder.com/100',
                        'rating': 'N/A (Snapdeal)'
                    })

        elif site == 'indiamart':
            url = f"https://dir.indiamart.com/search.mp?ss={query.replace(' ', '+')}"
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.select('div.lst')

            for item in items[:5]:
                title = item.select_one('.prd-name')
                price = item.select_one('.prc')
                image = item.select_one('img')

                if title and image:
                    products.append({
                        'title': title.text.strip(),
                        'price': price.text.strip() if price else 'Price on request',
                        'image': image.get('data-original', 'https://via.placeholder.com/100'),
                        'rating': 'N/A (IndiaMART)'
                    })

    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
