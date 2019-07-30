# -*- coding: utf-8 -*-
import os

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from mzitu.items import MzituItem




#爬取http://www.mzitu.com/上的所有图片

# 存储每个分类的路径
all_page_link = []
# 存储每张图片的路径
final_page_link = []


class MzituSpider(CrawlSpider):
    name = 'mzitu'
    allowed_domains = ['www.mzitu.com']
    start_urls = ['http://www.mzitu.com/']

    def parse(self, response):
        print('==========开始==============')
        root_path = 'd:/mzitu'
        # 这是针对WINDOWS下创建文件名可能存在的非法字符进行替换
        trantab = str.maketrans('\/:*?"<>|','abcdefghi')
        if response.url not in all_page_link:
            # 做记录
            all_page_link.append(response.url)
            # 当前页下所有分类url
            detail_page = scrapy.Selector(response).xpath('//ul[@id="pins"]/li/a/@href').extract()
            # 当前页下所有分类名称
            detail_name = scrapy.Selector(response).xpath('//ul[@id="pins"]/li/span/a/text()').extract()
            # 进行遍历
            for page, name in zip(detail_page, detail_name):
                # 替换非法字符
                name = name.translate(trantab)
                dir_path = '%s/%s' % (root_path, name)
                dir_path = dir_path.replace(' ', '-')
                if not os.path.exists(dir_path):
                    # 找到每一分类的时候先创建目录，后续就不用创建了.os.mkdir()只能创建一级目录;os.makedirs()可以创建多级目录
                    os.makedirs(dir_path)
                # 每一页的每一分类转入下一函数进行处理
                yield scrapy.Request(page, callback=self.pic_download)
        # 下一页的地址
        next_url = scrapy.Selector(response).xpath('//a[@class="next page-numbers"]/@href').extract()[0]
        # 爬完当前页的所有分类，就进入下一页回调函数
        yield scrapy.Request(next_url, callback=self.parse())

    def pic_download(self, response):
        item = MzituItem()
        pic_name = scrapy.Selector(response).xpath('//div[@class="main-image"]/p/a/img/@alt').extract()[0]
        trantab = str.maketrans('\/:*?"<>|', 'abcdefghi')
        # 依然是替换非法字符，之前是为了创建目录，这里是为了把图片应存储的本地分类路劲写入到item中
        item['pic_name'] = pic_name.translate(trantab)
        # 找到该分类的页数
        item['pic_url'] = scrapy.Selector(response).xpath('//div[@class="main-image"]/p/a/img/@src').extract()[0]
        # 进入管道处理
        yield item
        # 找到该分类的页数
        url_num = scrapy.Selector(response).xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()').extract()[0]
        # 从第二页开始遍历
        for i in range(2, int(url_num) + 1):
            link = '{}/{}'.format(response.url, i)
            if link not in final_page_link:
                # 记录
                final_page_link.append(link)
                # 调用后续函数，这里不能回调该函数,原因看readme
                yield scrapy.Request(link, callback=self.pic_download_next)

    def pic_download_next(self, response):
        item = MzituItem()
        pic_name = scrapy.Selector(response).xpath('//div[@class="main-image"]/p/a/img/@alt').extract()[0]
        # 同上
        trantab = str.maketrans('\/:*?"<>|', 'abcdefghi')
        item['pic_name'] = pic_name.translate(trantab)
        item['pic_url'] = scrapy.Selector(response).xpath('//div[@class="main-image"]/p/a/img/@src').extract()[0]
        # 进入管道处理
        yield item