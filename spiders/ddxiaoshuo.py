# bingdian.py
# -*- coding:utf-8 -*-
import scrapy
# import re
# from bs4 import BeautifulSoup
# from scrapy.http import Response
from ddxiaoshuo.items import DdxiaoshuoItem, DcontentItem
from ddxiaoshuo.SQLitepipelines.sql import Sql


class ddxiaoshuo_spider(scrapy.Spider):
    name = 'ddxiaoshuo'
    allowed_domains = ['x23us.com']
    start_urls = ['http://www.x23us.com/class/2_1.html']

    # , 'http://www.23us.com/class/2_1.html',
    #           'http://www.23us.com/class/3_1.html', 'http://www.23us.com/class/4_1.html',
    #           'http://www.23us.com/class/5_1.html', 'http://www.23us.com/class/6_1.html',
    #           'http://www.23us.com/class/7_1.html', 'http://www.23us.com/class/8_1.html',
    #           'http://www.23us.com/class/9_1.html', 'http://www.23us.com/class/10_1.html']

    def parse(self, response):
        books = response.xpath('//dd/table/tr[@bgcolor="#FFFFFF"]')  # /table/tbody/tr[@bgcolor="#FFFFFF"]
        # print(books.extract())
        for book in books:
            name = book.xpath('.//td[1]/a[2]/text()').extract()[0]
            author = book.xpath('.//td[3]/text()').extract()[0]
            novelurl = book.xpath('.//td[1]/a[2]/@href').extract()[0]
            serialstatus = book.xpath('.//td[6]/text()').extract()[0]
            serialnumber = book.xpath('.//td[4]/text()').extract()[0]
            category = book.xpath('//dl/dt/h2/text()').re(u'(.+) - 文章列表')[0]
            jianjieurl = book.xpath('.//td[1]/a[1]/@href').extract()[0]

            item = DdxiaoshuoItem()
            item['name'] = name
            item['author'] = author
            item['novelurl'] = novelurl
            item['serialstatus'] = serialstatus
            item['serialnumber'] = serialnumber
            item['category'] = category
            item['category_ids'] = response.url.split('/')[-1].split('_')[0]
            item['name_id'] = jianjieurl.split('/')[-1]
            yield item
            yield scrapy.Request(novelurl, callback=self.get_chapter, meta={'name_id': item['name_id']})
        next_page = response.xpath('//dd[@class="pages"]/div/a[12]/@href').extract()[0]  # 获取下一页地址
        if next_page:
            yield scrapy.Request(next_page)

    # 获取章节名
    def get_chapter(self, response):
        num = 0
        allures = response.xpath('//tr')
        for trurls in allures:
            tdurls = trurls.xpath('.//td[@class="L"]')
            for url in tdurls:
                num = num + 1
                chapterurl = response.url + url.xpath('.//a/@href').extract()[0]
                chaptername = url.xpath('.//a/text()').extract()[0]
                rets = Sql.select_chapter(chapterurl)
                if rets[0] == 1:
                    print(u'章节已经存在了')
                    pass
                else:
                    yield scrapy.Request(url=chapterurl, callback=self.get_chaptercontent,
                                         meta={'num': num, 'name_id': response.meta['name_id'],
                                               'chaptername': chaptername, 'chapterurl': chapterurl})

    # 获取章节内容
    def get_chaptercontent(self, response):
        item = DcontentItem()
        item['num'] = response.meta['num']
        item['id_name'] = response.meta['name_id']
        item['chaptername'] = response.meta['chaptername']
        item['chapterurl'] = response.meta['chapterurl']
        content = response.xpath('//dd[@id="contents"]/text()').extract()
        # item['chaptercontent'] = '\n   '.join(content)
        item['chaptercontent'] = '/%s/%s' % (str(item['id_name']), str(item['num']))
        return item
