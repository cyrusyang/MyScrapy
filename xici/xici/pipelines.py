# -*- coding: utf-8 -*-
import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class XiciPipeline(object):
    def process_item(self, item, spider):
        self.saveItem(item)
        return item

    def saveItem(self, item):
        # 打开数据库连接
        print(item)
        db = pymysql.connect(
            host='localhost',  # 连接的是本地数据库
            user='root',  # 自己的mysql用户名
            passwd='123456',  # 自己的密码
            db='test',  # 数据库的名字
            )

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        # SQL 插入语句
        sql = "INSERT INTO t_proxy(ip, \
               port, protocol) \
               VALUES ('%s', '%s', '%s' )" % \
              (item['ip'], item['port'], item['protocol'],)
        print(sql)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 执行sql语句
            db.commit()
        except Exception as e:
            # 发生错误时回滚
            print(e)
            db.rollback()

        # 关闭数据库连接
        db.close()