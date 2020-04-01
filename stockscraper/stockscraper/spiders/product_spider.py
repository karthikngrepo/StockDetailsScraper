import scrapy
import statistics
import pandas as pa
import os


class ProductSpider(scrapy.Spider):
    name = "product"

    def __init__(self, *args, **kwargs):
        super(ProductSpider, self).__init__(*args, **kwargs)
        self.stock_id = 'stock_id'
        self.stock_name = 'stock_name'
        self.price_nse = 'price_nse'
        self.price_bse = 'price_bse'
        self.eps = 'eps'
        self.roe = 'RoE'
        self.dividend_yield = 'dividend_yield'
        self.face_value = 'face_value'
        self.dividend = 'dividend'
        self.dividend_avg = 'dividend_avg'
        self.p_to_e = 'p_to_e'
        self.industry_p_to_e = 'industry_p_to_e'
        self.book_value = 'book_value'
        self.p_to_b = 'p_to_b'
        self.twenty_nineteen_net = '2019 Net'
        self.twenty_eighteen_net = '2018 Net'
        self.twenty_seventeen_net = '2017 Net'
        self.twenty_sixteen_net = '2016 Net'
        self.twenty_fifteen_net = '2015 Net'
        self.twenty_nineteen_yoy = 'YoY 2019'
        self.twenty_eighteen_yoy = 'YoY 2018'
        self.twenty_seventeen_yoy = 'YoY 2017'
        self.twenty_sixteen_yoy = 'YoY 2016'
        self.twenty_fifteen_yoy = 'YoY 2015'
        self.twenty_nineteen_esc = '2019 ESC'
        self.twenty_eighteen_esc = '2018 ESC'
        self.twenty_seventeen_esc = '2017 ESC'
        self.twenty_sixteen_esc = '2016 ESC'
        self.twenty_fifteen_esc = '2015 ESC'
        self.twenty_nineteen_profit = '2019 Profit'
        self.twenty_eighteen_profit = '2018 Profit'
        self.twenty_seventeen_profit = '2017 Profit'
        self.twenty_sixteen_profit = '2016 Profit'
        self.twenty_fifteen_profit = '2015 Profit'
        self.twenty_nineteen_eps = '2019 EPS'
        self.twenty_eighteen_eps = '2018 EPS'
        self.twenty_seventeen_eps = '2017 EPS'
        self.twenty_sixteen_eps = '2016 EPS'
        self.twenty_fifteen_eps = '2015 EPS'

    def start_requests(self):
        urls = []
        product_url_filename = 'product_urls.txt'

        with open(product_url_filename, 'r') as f:
            [urls.append(line.replace('\n', '')) for line in f.readlines()]

        for url in urls:
            url_elements = url.split('/')
            stock_id = url_elements[len(url_elements)-1]
            stock_short_name = url_elements[len(url_elements) - 2]
            yield scrapy.Request(url=url,
                                 callback=self.parse_summary,
                                 cb_kwargs=dict(stock_id=stock_id, stock_short_name=stock_short_name))

    def parse_summary(self, response, stock_id, stock_short_name):
        summary_stats = {
            self.stock_name:
                response.xpath('//*[@id="sec_quotes"]/div[2]/div/h1/text()').get(),
            self.price_nse:
                response.xpath('//*[@id="div_bse_livebox_wrap"]/div[1]/div[1]/div/div[2]/span[1]/text()').get(),
            self.price_bse:
                response.xpath('//*[@id="div_nse_livebox_wrap"]/div[1]/div[1]/div/div[2]/span[1]/text()').get(),
            self.eps:
                response.xpath('//*[@id="standalone_valuation"]/ul/li[2]/ul/li[3]/div[2]/text()').get(),
            self.dividend_yield:
                response.xpath('//*[@id="standalone_valuation"]/ul/li[3]/ul/li[2]/div[2]/text()').get(),
            self.face_value:
                response.xpath('//*[@id="standalone_valuation"]/ul/li[3]/ul/li[3]/div[2]/text()').get(),
            self.dividend:
                response.xpath('//*[@id="standalone_valuation"]/ul/li[1]/ul/li[4]/div[2]/text()').get(),
            self.p_to_e:
                response.xpath('//*[@id="standalone_valuation"]/ul/li[1]/ul/li[2]/div[2]/text()').get(),
            self.industry_p_to_e:
                response.xpath('//*[@id="standalone_valuation"]/ul/li[2]/ul/li[2]/div[2]/text()').get(),
            self.book_value:
                response.xpath('//*[@id="standalone_valuation"]/ul/li[1]/ul/li[3]/div[2]/text()').get(),
            self.p_to_b:
                response.xpath('//*[@id="standalone_valuation"]/ul/li[3]/ul/li[1]/div[2]/text()').get()
        }
        dataframe = pa.DataFrame(summary_stats, index=[stock_id])

        yearly_url = 'https://www.moneycontrol.com/financials/%s/results/yearly/%s#%s' \
                     % (stock_short_name, stock_id, stock_id)
        yield scrapy.Request(url=yearly_url,
                             callback=self.parse_yearly_stats,
                             cb_kwargs=dict(stock_id=stock_id, dataframe=dataframe))

    def parse_yearly_stats(self, response, stock_id, dataframe):
        yearly_stats = dict()
        yearly_results_table = response.xpath('//*[@id="standalone-new"]/div[1]/table/tr')
        _get_avg_dividend(yearly_results_table, 'Equity Dividend Rate (%)', yearly_stats)
        _get_column_data(yearly_results_table, 'Other Income', yearly_stats,
                         [self.twenty_nineteen_net, self.twenty_eighteen_net, self.twenty_seventeen_net,
                          self.twenty_sixteen_net, self.twenty_fifteen_net])
        _get_column_data(yearly_results_table, 'Basic EPS', yearly_stats,
                         [self.twenty_nineteen_eps, self.twenty_eighteen_eps, self.twenty_seventeen_eps,
                          self.twenty_sixteen_eps, self.twenty_fifteen_eps])
        _get_column_data(yearly_results_table, 'Equity Share Capital', yearly_stats,
                         [self.twenty_nineteen_esc, self.twenty_eighteen_esc, self.twenty_seventeen_esc,
                          self.twenty_sixteen_esc, self.twenty_fifteen_esc])
        _get_column_data(yearly_results_table, 'Net Profit/(Loss) For the Period', yearly_stats,
                         [self.twenty_nineteen_profit, self.twenty_eighteen_profit, self.twenty_seventeen_profit,
                          self.twenty_sixteen_profit, self.twenty_fifteen_profit])

        yearly_stats_dataframe = pa.DataFrame(yearly_stats, index=[stock_id])
        dataframe = dataframe.merge(yearly_stats_dataframe, left_index=True, right_index=True)
        _write_data_to_csv(dataframe)


def _write_data_to_csv(dataframe):
    dataframe.reset_index()
    relative_path = os.path.realpath(os.path.dirname(__file__))
    stock_analysis_file_path = os.path.join(relative_path, '../StockMarketData.csv')
    print(stock_analysis_file_path)
    dataframe.to_csv(stock_analysis_file_path, encoding='utf-8', index=False, mode='a', header=False)


def _get_column_data(rows, column_identifier, data_as_dict, column_names):
    data = []
    for row in rows:
        if row.xpath('.//td/text()')[0].get() == column_identifier:
            data = row.xpath('.//td/text()')[1:6].getall()

    data = [float(item.replace(',', '')) for item in data]

    for index in range(len(data)):
        key = column_names[index]
        value = data[index]
        data_as_dict[key] = value


def _get_avg_dividend(rows, column_identifier, data_as_dict):
    data = []
    for row in rows:
        if row.xpath('.//td/text()')[0].get() == column_identifier:
            data = row.xpath('.//td/text()')[1:6].getall()

    for item in data:
        five_years_dividend = 0 if item == '--' else float(item.replace(',', ''))
        data_as_dict['avg_dividend'] = statistics.mean(five_years_dividend)
