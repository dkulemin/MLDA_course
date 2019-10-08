# -*- coding: utf-8 -*-
import scrapy


class IspytanogetreviewsSpider(scrapy.Spider):
    name = 'ispytanogetreviews'
    allowed_domains = ['ispytano.ru']

    def parse(self, response):
        print(f'Парсим: {response.url}')
        labels = response.xpath('//body/div[1]/div[4]/table/tr/td[4]/b/font/@color').extract()
        reviews = []
        for res in response.xpath('//body/div[1]/div[4]/table/tr[position()>1]/td[5]'):
            pros_n_cons = ' '.join(res.xpath('./div/text()').extract())
            pros_n_cons = pros_n_cons.replace('Недостатки: ', '')
            pros_n_cons = pros_n_cons.replace('Преимущества: ', '')
            review = ' '.join(res.xpath('./text()').extract())
            reviews.append(pros_n_cons + ' ' + review)
        for item in zip(labels, reviews):
            scraped_info = {'labels': item[0], 'reviews': item[1]}

            yield scraped_info
