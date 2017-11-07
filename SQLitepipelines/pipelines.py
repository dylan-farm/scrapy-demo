# pipelines.py
# -*- coding:utf-8 -*-
from .sql import Sql

from ddxiaoshuo.items import DdxiaoshuoItem, DcontentItem


class BingdingPipeline(object):
    print("数据处理")
    values = []
    chapters = []

    def process_item(self, item, spider):
        if isinstance(item, DdxiaoshuoItem):
            name_id = item['name_id']
            ret = Sql.select_name(name_id)
            if ret[0] == 1:
                print('已经存在了')
                pass
            else:
                xs_name = item['name']
                xs_author = item['author']
                category = item['category']
                category_id = item['category_ids']
                value = (xs_name, xs_author, category, category_id, name_id)
                if len(self.values) < 1000:
                    self.values.append(value)
                else:
                    Sql.insert_dd_name(self.values)
                    self.values.clear()
                    self.values.append(value)

            print(u'开始存小说标题')
        if isinstance(item, DcontentItem):
            url = item['chapterurl']
            name_id = item['id_name']
            num_id = item['num']
            xs_chaptername = item['chaptername']
            xs_content = item['chaptercontent']
            chapter = (xs_chaptername, xs_content, name_id, num_id, url)
            if len(self.chapters) < 1000:
                self.chapters.append(chapter)
            else:
                Sql.insert_dd_chaptername(self.chapters)
                self.chapters.clear()
                self.chapters.append(chapter)
            # Sql.insert_dd_chaptername()
            print(u'%s 存储完毕' % xs_chaptername)
            return item
