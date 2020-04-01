import scrapy


class CategorySpider(scrapy.Spider):
    name = "category"

    def start_requests(self):
        urls = []
        product_url_filename = 'product_urls.txt'
        main_url_filename = 'main_urls.txt'

        with open(product_url_filename, 'w') as f:
            print('Cleared existing data in product url file=%s', product_url_filename)

        with open(main_url_filename, 'r') as f:
            [urls.append(line) for line in f.readlines()]

        for url in urls:
            print('Trying to scrape %s', url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = 'product_urls.txt'
        product_urls = response.xpath(
            '//*[@id="mc_mainWrapper"]/div[3]/div[1]/div[10]/div[2]/div/table/tr/td/a/@href').getall()

        with open(filename, 'a') as f:
            [f.write('https://www.moneycontrol.com%s\n' % product_url) for product_url in product_urls]

        [print('https://www.moneycontrol.com%s' % product_url) for product_url in product_urls]
