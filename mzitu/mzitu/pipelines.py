# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import time
import requests


class MzituPipeline(object):

    def process_item(self, item, spider):
        pic_url = item['pic_url']
        # 从url取图片名称
        name = pic_url.rsplit('/', 1)[-1]
        root_path = 'd:/mzitu'
        # 取出该图片应属于哪个分类
        dir_path = item['pic_name']
        # 拼接名称确认图片路径
        file_path = '%s/%s/%s' % (root_path, dir_path, name)
        file_path = file_path.replace(' ', '-')
        # 判断是否下载过
        if not os.path.exists(file_path):
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(f'{t} downloading: ', file_path)
            with open(file_path, 'wb') as jpg:
                jpg.write(requests.get(pic_url, timeout=15, headers=self.getheader(pic_url)).content)
        return item

    def getheader(self, refers):
        # 要使用Referer指向，不然会被防盗链
        headers = DEFAULT_REQUEST_HEADERS = {
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Referer': '{}'.format(refers),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        return headers

    def close_spider(self, spider):
        print('任务结束了！')