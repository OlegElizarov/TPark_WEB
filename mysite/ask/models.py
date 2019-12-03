# coding=utf-8
import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Question.objects.annotate(num_tags=Count('tags',distinct=True)).order_by('-num_tags')
# Tag.objects.annotate(num_tags=Count('question')).order_by('-num_tags')

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    nickname = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nickname

    @receiver(post_save, sender=User)
    def create_user_author(sender, instance, created, **kwargs):
        if created:
            Author.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_author(sender, instance, **kwargs):
        instance.author.save()

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class TagManager(models.Manager):
    def besters(self):
        return self.annotate(num_tags=Count('question')).order_by('-num_tags')


class Tag(models.Model):
    name = models.CharField(max_length=15,unique=True)
    color = models.CharField(max_length=15)
    objects = TagManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class QuestionManager(models.Manager):
    def fresh(self):
        return self.order_by('-pub_date')

    def besters(self):
        return self.order_by('-rating')


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey(
        Author, on_delete=models.SET_NULL, null=True, blank=True)
    pub_date = models.DateTimeField('date published')
    rating = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag)
    objects = QuestionManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    author = models.ForeignKey(
        Author, on_delete=models.SET_NULL, null=True, blank=True)
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


class LikeDislike(models.Model):
    author = models.ForeignKey(
        Author, on_delete=models.SET_NULL, null=True, blank=True)

    #question = models.ForeignKey(
    #    Question, on_delete=models.SET_NULL, null=True, blank=True)
    #answer = models.ForeignKey(
    #    Answer, on_delete=models.SET_NULL, null=True, blank=True)
    like_type = models.BooleanField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
