# -*- coding:utf-8 -*-
import json
from twisted.enterprise import adbapi
from scrapy import log
import pymysql
# import pymysql.cursors
from ddxiaoshuo import settings

connect = pymysql.connect(user=settings.MYSQL_USER, password=settings.MYSQL_PASSWD, port=settings.MYSQL_PORT,
                          host=settings.MYSQL_HOST, db="MYSQL", charset="utf8")
cursor = connect.cursor()  # 获取游标
# cursor.execute("drop database if exists ddxs_db")
# cursor.execute("create database ddxs_db")  # 创建数据库，！！！！这一条代码仅限第一次使用，有了数据库后就不用再使用了
cursor.execute("use ddxs_db")  # 使用数据库

# # 创建 dd_name 表
cursor.execute('DROP TABLE IF EXISTS dd_name')
cursor.execute(
    'CREATE TABLE dd_name(xs_name VARCHAR (255) DEFAULT NULL ,xs_author VARCHAR (255),category VARCHAR (255),category_ids VARCHAR (255),name_id VARCHAR (255))')
# # 创建 dd_chaptername 表
cursor.execute('DROP TABLE IF EXISTS dd_chaptername')
cursor.execute(
    'CREATE TABLE dd_chaptername(xs_chaptername VARCHAR(255) DEFAULT NULL ,xs_content TEXT,id_name INT(11) DEFAULT NULL,num_id INT(11) DEFAULT NULL ,url VARCHAR(255))')


class Sql:
    # 插入数据
    @classmethod
    def insert_dd_name(cls, list):
        # sql = "insert into dd_name (xs_name,xs_author,category,category_id,name_id) values (%(xs_name)s , %(xs_author)s , %(category)s , %(category_id)s , %(name_id)s)"
        # sql = "insert into dd_name (xs_name,xs_author,category,category_id,name_id) values ('%s','%s','%s','%s')" % (
        # sql = "insert into dd_name (xs_name,xs_author,category,category_id,name_id) values ('%s','%s','%s','%s')" % (
        # list[0][0], list[0][1], list[0][2], list[0][3], list[0][4])
        # cursor.execute(sql)
        sql = "insert into dd_name (xs_name,xs_author,category,category_ids,name_id) values(%s,%s,%s,%s,%s)"

        try:
            cursor.executemany(sql, list)
            connect.commit()
        except Exception as e:
            connect.rollback()
            print("执行MySQL: %s 时出错：%s" % (sql, e))

        pass

    # 查重
    @classmethod
    def select_name(cls, name_id):
        sql = "SELECT EXISTS (select 1 from dd_name where name_id = '%s')" % name_id
        cursor.execute(sql)
        return cursor.fetchall()[0]
        pass

    @classmethod
    def insert_dd_chaptername(cls, list):
        # sql = '''INSERT INTO dd_chaptername(xs_chaptername , xs_content , id_name ,num_id ,
        #             url) VALUES ('%s' ,'%s' ,%s ,%s ,'%s')''' % (xs_chaptername, xs_content, id_name, num_id, url)
        # cursor.execute(sql)
        # connect.commit()
        sql2 = "insert into dd_chaptername (xs_chaptername,xs_content,id_name,num_id,url) values(%s, %s, %s, %s, %s)"

        try:
            cursor.executemany(sql2, list)
            connect.commit()
        except Exception as e:
            connect.rollback()
            print("执行MySQL: %s 时出错：%s" % (sql2, e))
        pass

    @classmethod
    def select_chapter(cls, url):
        sql = "SELECT EXISTS (select 1 from dd_chaptername where url = '%s')" % url
        cursor.execute(sql)
        return cursor.fetchall()[0]
        pass
