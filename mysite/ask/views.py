from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from ask import models

questions = {}
for i in range(20):
    questions[i] = {'id': i, 'title': f'question#{i}'}

def tag(request, tag_name):
    return render(
        request,
        'ask/tag.html',{
            'questions':questions.values(),
            'tag_name': tag_name,        }
    )


def index(request):
    paginator = Paginator(list(questions.values()), 5)  # Show 25 contacts per page
    page = request.GET.get('page')
    question_list = paginator.get_page(page)
    return render(
        request,
        'ask/index.html',{
            'questions':list(questions.values()),
            'question_list': question_list,
        }
    )



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


#def tag(request, tag_name):
#    return render(
#        request,
#        'ask/tag.html',{
#            'questions':questions.values(),
#            'tag_name':tag_name,
#        }
#    )