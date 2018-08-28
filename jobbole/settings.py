# -*- coding: utf-8 -*-

# Scrapy settings for jobbole project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'jobbole'

SPIDER_MODULES = ['jobbole.spiders']
NEWSPIDER_MODULE = 'jobbole.spiders'

#------<<MySql数据库信息>>-------
MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'article'
MYSQL_USER = 'root'
MYSQL_PASSWD = '123456'

SQL_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
SQL_DATE_FORMAT = "%Y-%m-%d"

#------<<MongoDB数据库信息>>-------
MONGO_URI = 'localhost'
MONGO_DB = 'article'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'jobbole (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'jobbole.middlewares.JobboleSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'jobbole.middlewares.JobboleDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}


# pipeline中自带三种管道
# 1.图片下载（scrapy.pipelines.images.ImagesPipeline）
# 2.文件下载：json,csv,xml等
# 3.媒体下载


# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    #'jobbole.pipelines.JobbolePipeline': 300,
    #'jobbole.pipelines.JsonWithEncodingPipeline': 2,
    #'jobbole.pipelines.MysqlTwistedPipline': 2,
    #'jobbole.pipelines.MongoPipeline': 2,
    #'jobbole.pipelines.MysqlPipeline': 2,
    #'jobbole.pipelines.ArticleImagePipeline': 300,
    #'scrapy.pipelines.images.ImagesPipeline': 1,
}


# #设置下载图片的最下宽度等
# IMAGES_MIN_HEIGHT = 100
# IMAGES_MIN_WIDTH = 100
# #设置图片下载的地址
# #新建文件夹images
# project_dir = os.path.abspath(os.path.dirname(__file__))
# IMAGES_URLS_FIELD = "front_image_url"
# IMAGES_STORE = os.path.join(project_dir, 'images')



# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
