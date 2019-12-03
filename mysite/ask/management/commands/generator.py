from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from faker import Faker
from random import choice
from django.utils import timezone

from ask.models import  Question, Answer, Tag

f = Faker()


class Command(BaseCommand):
    USERS_COUNT = 3
    TAGS_COUNT = 3
    QUESTIONS_COUNT_FOR_ONE_USER = 3
    ANSWERS_COUNT_FOR_ONE_QUESTION = 3

    def question_generator(self):
        authors = Author.objects.all()
        for a in authors:
            for _ in range(0, self.QUESTIONS_COUNT_FOR_ONE_USER):
                q = Question.objects.create(author=a,
                                            title=f.text(16),
                                            #f.sentence()
                                            text=f.text(256),
                                            pub_date=timezone.now())
                q.save()

    def answers_generator(self):
        authors = Author.objects.all()
        questions = Question.objects.all()
        for q in questions:
            for _ in range(0, self.ANSWERS_COUNT_FOR_ONE_QUESTION):
                a = Answer.objects.create(author=choice(authors),
                                          question=q,
                                          title=f.text(256),
                                          text=f.text(256),
                                          pub_date=timezone.now(),
                                          correct=False, )
                a.save()

    def tags_generator(self):
        questions = Question.objects.all()
        for _ in range(0, self.TAGS_COUNT):
            t = Tag.objects.create(name=f.color_name(), color=f.color_name())
            for _ in range(0, self.QUESTIONS_COUNT_FOR_ONE_USER):
                t.question_set.add(choice(questions))
            t.save()

    def generator(self):
        #self.authors_generator()
        self.question_generator()
        self.answers_generator()
        self.tags_generator()

    def handle(self, *args, **options):
        self.generator()
