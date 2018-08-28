# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class JobbolePipeline(object):
    def process_item(self, item, spider):
        return item

#---------------<<图片保存改写>>------------------------------
#定制改写图片保存的pipeline使其下载图片后能保存下它的本地路径
# from scrapy.pipelines.images import ImagesPipeline
# class ArticleImagePipeline(ImagesPipeline):
#     def item_completed(self, results, item, info):
#         if "front_image_url" in item:
#             for ok,value in results:
#                 image_file_path = value['path']
#             item['front_image_url'] =image_file_path
#
#         return item

#----------------<<json>>-----------------------
#自定义json文件导出，避免编码问题
import codecs
import json
class JsonWithEncodingPipeline(object):
    #自定义json文件的导出
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding="utf-8")
    def process_item(self, item, spider):
        #将item转换为dict，然后生成json对象，false避免中文出错
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item
    #当spider关闭的时候
    def spider_closed(self, spider):
        self.file.close()


#--------------<<MySQL>>-------------------------
#方法1：采用同步的机制写入mysql
import pymysql
from  scrapy.conf import settings
class MysqlPipeline(object):

    def __init__(self):
        #配置基本的sql信息
        host = settings["MYSQL_HOST"]
        user= settings["MYSQL_USER"]
        psd = settings['MYSQL_PASSWD']
        db = settings['MYSQL_DBNAME']
        try:
            #连接到数据库
            self.connect = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset="utf8", use_unicode=True)

           #通过cursor执行增删查改
            self.curse = self.connect.cursor()
        except pymysql.MySQLError as e:
            print(e.args)


    def process_item(self,item,spider):
        # 查重处理
        self.curse.execute(
            """ select * from jobbole where url_object_id = %s """,
            item['url_object_id'])
        #是否有重复值
        repetition = self.curse.fetchone()

        if repetition:
            pass
        else:
            try:
                insert_sql,params = item.get_insert_sql()
                self.curse.execute(insert_sql,params)
                self.connect.commit()
            except pymysql.MySQLError as e:
                print(e.args)
                self.connect.rollback()


#方法2：采用异步的机制写入mysql
import pymysql.cursors
from twisted.enterprise import adbapi

#连接池ConnectionPool
#    def __init__(self, dbapiName, *connargs, **connkw):
class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWD"],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        #**dbparms-->("MySQLdb",host=settings['MYSQL_HOST']
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)#无需直接导入 dbmodule. 只需要告诉 adbapi.ConnectionPool 构造器你用的数据库模块的名称比如pymysql.

        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) #处理异常

    def handle_error(self, failure, item, spider):
        #处理异步插入的异常
        print (failure)

    def do_insert(self, cursor, item):
        #执行具体的插入
        #根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)

#--------------<<MongoDB>>-------------------------
import pymongo
class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self,item,spider):
        self.db["jobbole"].insert(dict(item))
        return item

    def close_spider(self,spider):
        self.client.close()

