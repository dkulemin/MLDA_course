# -*- coding: utf-8 -*-
import scrapy


class IspytanogetlinksSpider(scrapy.Spider):
    name = 'ispytanogetlinks'
    allowed_domains = ['ispytano.ru']

    def parse(self, response):
        links = response.css('table.table_light td:nth-child(1) a::attr(href)').extract()
        for link in links:
            scraped_info = {'link': 'https://ispytano.ru' + link}

            yield scraped_info
