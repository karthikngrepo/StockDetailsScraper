import scrapy
import os


class CategorySpider(scrapy.Spider):
    name = "category"
    relative_path = os.path.realpath(os.path.dirname(__file__))
    product_url_filename = os.path.join(relative_path, '../samples/product_urls.txt')
    main_url_filename = os.path.join(relative_path, '../samples/main_urls.txt')

    def start_requests(self):
        spider = CategorySpider()
        urls = []

        with open(spider.product_url_filename, 'w') as f:
            print('Cleared existing data in product url file=%s', spider.product_url_filename)

        with open(spider.main_url_filename, 'r') as f:
            [urls.append(line) for line in f.readlines()]

        for url in urls:
            print('Trying to scrape %s', url)
            yield scrapy.Request(url=url,
                                 callback=self.parse_categories,
                                 cb_kwargs=dict(spider=spider))

    def parse_categories(self, response, spider):
        product_urls = response.xpath(
            '//*[@id="mc_mainWrapper"]/div[3]/div[1]/div[10]/div[2]/div/table/tr/td/a/@href').getall()

        with open(spider.product_url_filename, 'a') as f:
            [f.write('https://www.moneycontrol.com%s\n' % product_url) for product_url in product_urls]

        [print('https://www.moneycontrol.com%s' % product_url) for product_url in product_urls]
