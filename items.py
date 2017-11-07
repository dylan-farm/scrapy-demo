# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


#
# class DdxiaoshuoItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass


class DdxiaoshuoItem(scrapy.Item):
    name = scrapy.Field()
    # 小说名
    author = scrapy.Field()
    # 作者
    novelurl = scrapy.Field()
    # 小说地址
    serialstatus = scrapy.Field()
    # 状态
    serialnumber = scrapy.Field()
    # 连载字数
    category = scrapy.Field()
    #  文章类别
    category_ids = scrapy.Field()
    # 文章类别id
    name_id = scrapy.Field()
    # 小说编号
    pass


class DcontentItem(scrapy.Item):
    id_name = scrapy.Field()  # 小说编号
    chaptercontent = scrapy.Field()  # 章节内容
    num = scrapy.Field()  # 用于绑定章节顺序
    chapterurl = scrapy.Field()  # 章节地址
    chaptername = scrapy.Field()  # 章节名字
