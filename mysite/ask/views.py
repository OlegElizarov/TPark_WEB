from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from ask import models
from ask.models import Question, Answer,Tag

questions = {}
for i in range(20):
    questions[i] = {'id': i, 'title': f'question#{i}'}

def tag(request, tag_name):
    q=Question.objects.filter(tags__name__contains=tag_name)
    t=Tag.objects.all()
    paginator = Paginator(q, 2)  # Show 1 contacts per page
    page = request.GET.get('page')
    question_list = paginator.get_page(page)
    return render(
        request,
        'ask/tag.html',{
            'tag_name': tag_name,
            'tags':t,
            'question_list': question_list,
        }
    )


def index(request):
    q=Question.objects.all()
    t=Tag.objects.all()
    paginator = Paginator(q, 2)  # Show 2 contacts per page
    page = request.GET.get('page')
    question_list = paginator.get_page(page)
    return render(
        request,
        'ask/index.html',{
            'question_list': question_list,
            'tags':t,
        }
    )

def question(request,question_id):
    q = get_object_or_404(Question, pk=question_id)
    a = q.answer_set.all()
    t=Tag.objects.all()
    return render(
        request,
        'ask/question.html',{
            'question': q,
            'answer_list': a,
            'tags':t,
        }
    )

def base(request):
    t=Tag.objects.all()
    return render(
        request,
        'ask/base.html',{
            'tags':t,
        }
    )

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