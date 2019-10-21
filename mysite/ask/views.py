from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse


questions={}
for i in range(20):
    questions[i]={'id':i,'title':f'question#{i}'}

class IndexView(generic.ListView):
    template_name = 'ask/index.html'

    def get_queryset(self):
        pass

class BaseView(generic.ListView):
    template_name = 'ask/base.html'

    def get_queryset(self):
        pass

class AView(generic.ListView):
    template_name = 'ask/ask.html'

    def get_queryset(self):
        pass

class QView(generic.ListView):
    template_name = 'ask/question.html'

    def get_queryset(self):
        pass

class SView(generic.ListView):
    template_name = 'ask/settings.html'

    def get_queryset(self):
        pass

class RView(generic.ListView):
    template_name = 'ask/registration.html'

    def get_queryset(self):
        pass


def tag(request, tag_name):
    return render(
        request,
        'ask/tag.html',{
            'questions':questions.values(),
            'tag_name':tag_name,
        }
    )