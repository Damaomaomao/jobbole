# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import datetime
import scrapy
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose,Join,TakeFirst
#MapCompose可以传入函数对于该字段进行处理，而且可以传入多个

def return_value(value):
    return value

def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()

    return create_date

def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums


def remove_comment_tags(value):
    #去掉tag中提取的评论
    if "评论" in value:
        return ""
    else:
        return value

def remove_time(value):
    if "·" in value:
        return value.replace("·","").strip()
    else:
        return value


class ArticleItemLoader(ItemLoader):
    # 自定义itemloader实现默认提取第一个
    default_output_processor = TakeFirst()

class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(remove_time),
        output_processor=TakeFirst()

    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(",")
    )
    #content = scrapy.Field()


    def get_insert_sql(self):
        insert_sql='''
        insert into jobbole(title,create_date,url,url_object_id,front_image_url,praise_nums,comment_nums,fav_nums,tags)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON  DUPLICATE KEY UPDATE fav_nums=VALUES(fav_nums)
        '''
        create_date = date_convert(self['create_date'])
        params = (
            self['title'],create_date,self['url'],self['url_object_id'],self['front_image_url'],
            self['praise_nums'],self['comment_nums'],self['fav_nums'],self['tags']
        )
        return insert_sql,params