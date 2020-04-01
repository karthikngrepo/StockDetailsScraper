import scrapy
import os


class MainSpider(scrapy.Spider):
    name = "main"
    relative_path = os.path.realpath(os.path.dirname(__file__))
    filename = stock_analysis_file_path = os.path.join(relative_path, '../samples/main_urls.txt')

    def start_requests(self):
        spider = MainSpider()
        with open(spider.filename, 'w') as f:
            print('Refreshing the main url file=%s', spider.filename)

        urls = [
            'https://www.moneycontrol.com/stocks/marketinfo/marketcap/bse/index.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url,
                                 callback=self.parse_main_page,
                                 cb_kwargs=dict(spider=spider))

    def parse_main_page(self, response, spider):
        base_urls = response.xpath('//div[@class="lftmenu"]/ul/li/a/@href').getall()
        with open(spider.filename, 'a') as f:
            [f.write('https://www.moneycontrol.com%s\n' % base_url) for base_url in base_urls]
        [print('https://www.moneycontrol.com%s' % base_url) for base_url in base_urls]
