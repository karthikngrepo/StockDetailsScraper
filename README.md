# Stock Scraper

Stock scraper is a project to scrape the indian stock market information to get a single page view of basic stats around all the listed socks in BSE or if need be in NSE

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install -r requirements.txt
```

## Usage

```python
scrapy crawl main # To get the url's for all categories of stocks
scrapy crawl category # To get the url's for all the products in BSE
scrapy crawl products # To get the details of all the stocks in BSE

# Note in case if you want to scrape the NSE data, you just need to modify the URL in main_spider.py
```

## Contributing 
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)