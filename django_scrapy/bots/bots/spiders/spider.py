# -*- coding:utf-8 -*-

import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from bots.items import DoubanBookItem


class DoubanBookSpider(CrawlSpider):
    name = 'douban_book'

    allowed_domains = ['douban.com']

    start_urls = [
        'https://book.douban.com/tag/?icn=index-nav'
    ]

    # 爬虫规则
    rules = (
        Rule(LinkExtractor(allow='/tag/', restrict_xpaths='//div[@class="article"]'), follow=True),
        Rule(LinkExtractor(allow='\?start=\d+\&type=', restrict_xpaths='//div[@class="paginator"]'), follow=True),
        Rule(LinkExtractor(allow='/subject/\d+/$', restrict_xpaths='//ul[@class="subject-list"]'),
             callback='parse_item')
    )

    def parse_item(self, response):
        def value(list):
            return list[0] if len(list) else ' '

        item = DoubanBookItem()
        sel = Selector(response)

        item['book_id'] = response.url.split('/')[-2]
        item['book_name'] = value(sel.xpath('//div[@id="wrapper"]/h1/span/text()').extract())
        item['image_urls'] = value(sel.xpath('//div[@id="mainpic"]/a/@href').extract())
        item['author_info'] = ''
        author_info = sel.xpath('//div[@id="info"]/a[1]/text()').extract()
        if author_info:
            item['author_info'] = ''.join(author_info).strip().replace(' ', '').replace('\n', ' ')

        book_info = sel.xpath('//div[@id="info"]').extract()[0].replace('\n', '')
        m = re.search(r'出版社:</span>\s*(.*?)\s*<br>', book_info)
        item['book_publish'] = m.group(1) if m else ''
        m = re.search(r'出版年:</span>\s*(.*?)\s*<br>', book_info)
        item['book_publish_time'] = m.group(1) if m else ''

        item['book_star'] = value(sel.xpath('//div[@class="rating_self clearfix"]/strong/text()').extract())
        item['people_num'] = value(sel.xpath('//div[@class="rating_sum"]/span/a/span/text()').extract())
        item['book_quote'] = ''
        book_quote = sel.xpath('//div[@class="intro"]//p/text()').extract()
        if book_quote:
            for line in book_quote:
                item['book_quote'] = item['book_quote'] + line

        item['author_quote'] = ''
        author_quote = sel.xpath('//div[@class="indent "]/div/div[@class="intro"]//p/text()').extract()
        if author_quote:
            for l in author_quote:
                item['author_quote'] = item['author_quote'] + l

        yield item
