from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from ask import models
from ask.models import Question, Answer, Tag,QuestionManager,TagManager
from django.contrib.auth.models import User
from .forms import questionform
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse

def tag(request, tag_name):
    q = Question.objects.filter(tags__name__contains=tag_name)
    t = Tag.object1.besters()
    paginator = Paginator(q, 2)  # Show 1 contacts per page
    page = request.GET.get('page')
    question_list = paginator.get_page(page)
    return render(
        request,
        'ask/tag.html', {
            'tag_name': tag_name,
            'tags': t,
            'question_list': question_list,
            'users': User.objects.all(),
        }
    )


def index(request):
    q = Question.object1.besters()
    t = Tag.object1.besters()
    paginator = Paginator(q, 2)  # Show 2 contacts per page
    page = request.GET.get('page')
    question_list = paginator.get_page(page)
    return render(
        request,
        'ask/index.html', {
            'question_list': question_list,
            'tags': t,
            'users':User.objects.all()
        }
    )


def question(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    a = q.answer_set.all()
    t = Tag.object1.besters()
    return render(
        request,
        'ask/question.html', {
            'question': q,
            'answer_list': a,
            'tags': t,
            'users': User.objects.all(),
        }
    )


def base(request):
    t = Tag.object1.besters()
    return render(
        request,
        'ask/base.html', {
            'tags': t,
            'users':User.objects.all(),
        }
    )


def ask(request):
    t=Tag.objects.all()
    form = questionform()
    if request.method == "POST":
        form = questionform(request.POST)
        if form.is_valid():
            title1= form.cleaned_data['title']
            text1= form.cleaned_data['text']
            tag1= form.cleaned_data['tag']
            print(title1,text1,tag1)
            q=Question(title=title1,text=text1,author=request.user,pub_date=timezone.now(),rating=0)
            print(q)
            q.save()
            for tg in tag1:
                q.tags.add(Tag.objects.get(id=tg))
            print(q)
            return HttpResponseRedirect(reverse('ask:index'))
        else:
            form = questionform()
    return render(
        request,
        'ask/question_create.html',
        {
            'form':form,
            'users':User.objects.all(),
            'tags':Tag.objects.all(),
        }
    )


class SView(generic.ListView):
    template_name = 'ask/settings.html'

    def get_queryset(self):
        pass


def settings(request):
    t = Tag.object1.besters()
    return render(
        request,
        'ask/settings.html', {
            'tags': t,
            'users':User.objects.all(),
        }
    )


class RView(generic.ListView):
    template_name = 'ask/registration.html'

    def get_queryset(self):
        pass
