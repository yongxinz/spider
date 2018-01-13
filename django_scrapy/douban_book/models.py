# coding=utf-8

from django.db import models


class DoubanBook(models.Model):
    """
    豆瓣图书
    """
    book_id = models.CharField(u"书本序号", max_length=10)
    book_name = models.CharField(u"书名", max_length=20)
    book_star = models.CharField(u"评分", max_length=5)
    people_num = models.CharField(u"评价人数", max_length=10)
    author_info = models.CharField(u"作者", max_length=30)
    book_publish = models.CharField(u"出版社", max_length=20)
    book_publish_time = models.CharField(u"出版年", max_length=10)

    book_quote = models.CharField(u"内容简介", max_length=2000)
    author_quote = models.CharField(u"作者介绍", max_length=2000)
    image_urls = models.CharField(u"书本封面", max_length=100)

    class Meta:
        ordering = ['book_id']

    def __unicode__(self):
        return self.book_name
