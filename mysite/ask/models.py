# coding=utf-8
from django.db import models

class ArticleManager(models.Manager):
    def published(self):
        return self.filter(id=2).first()


class Author(models.Model):
    name = models.CharField(max_length=255,verbose_name='Имя')
    rating = models.IntegerField(default=0)
    birthday = models.DateField()

    objects= ArticleManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Article(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    date_published = models.DateTimeField()
    is_published = models.BooleanField()
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
