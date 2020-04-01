import scrapy


class MainSpider(scrapy.Spider):
    name = "main"

    def start_requests(self):
        filename = 'main_urls.txt'
        with open(filename, 'w') as f:
            print('Refreshing the main url file=%s', filename)

        urls = [
            'https://www.moneycontrol.com/stocks/marketinfo/marketcap/bse/index.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = 'main_urls.txt'
        base_urls = response.xpath('//div[@class="lftmenu"]/ul/li/a/@href').getall()
        with open(filename, 'a') as f:
            [f.write('https://www.moneycontrol.com%s\n' % base_url) for base_url in base_urls]
        [print('https://www.moneycontrol.com%s' % base_url) for base_url in base_urls]
