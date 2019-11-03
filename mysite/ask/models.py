# coding=utf-8
import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db.models import Count


#Question.objects.annotate(num_tags=Count('tags',distinct=True)).order_by('-num_tags')
#Tag.objects.annotate(num_tags=Count('question')).order_by('-num_tags')


class TagManager(models.Manager):
    def besters():
        return Tag.objects.annotate(num_tags=Count('question')).order_by('-num_tags')


class Tag(models.Model):
    name = models.CharField(max_length=15)
    color = models.CharField(max_length=15)
    object1 = TagManager

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class QuestionManager(models.Manager):
    def fresh():
        return Question.objects.order_by('-pub_date')
    def besters():
        return Question.objects.order_by('-rating')


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    pub_date = models.DateTimeField('date published')
    rating = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag)
    object1 = QuestionManager

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    correct = models.BooleanField()
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
