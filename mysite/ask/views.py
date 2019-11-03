from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from ask.models import Question, Answer, Tag, QuestionManager, TagManager, Author
from .forms import questionform
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse


def tag(request, tag_name):
    q = Question.objects.filter(tags__name__contains=tag_name)
    paginator = Paginator(q, 2)  # Show 1 contacts per page
    page = request.GET.get('page')
    question_list = paginator.get_page(page)
    return render(
        request,
        'ask/tag.html', {
            'tag_name': tag_name,
            'tags': Tag.object1.besters(),
            'question_list': question_list,
            'users': Author.objects.all(),
        }
    )


def index(request):
    q = Question.object1.besters()
    paginator = Paginator(q, 2)  # Show 2 contacts per page
    page = request.GET.get('page')
    question_list = paginator.get_page(page)
    return render(
        request,
        'ask/index.html', {
            'question_list': question_list,
            'tags': Tag.object1.besters(),
            'users': Author.objects.all()
        }
    )


def question(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    a = q.answer_set.all()
    return render(
        request,
        'ask/question.html', {
            'question': q,
            'answer_list': a,
            'tags': Tag.object1.besters(),
            'users': Author.objects.all(),
        }
    )


def base(request):
    return render(
        request,
        'ask/base.html', {
            'tags': Tag.object1.besters(),
            'users': Author.objects.all(),
        }
    )


def ask(request):
    form = questionform()
    if request.method == "POST":
        form = questionform(request.POST)
        if form.is_valid():
            title1 = form.cleaned_data['title']
            text1 = form.cleaned_data['text']
            tag1 = form.cleaned_data['tag']
            print(title1, text1, tag1)
            q = Question(title=title1, text=text1, author=request.user, pub_date=timezone.now(), rating=0)
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
            'form': form,
            'users': Author.objects.all(),
            'tags': Tag.object1.besters(),
        }
    )

def settings(request):
    return render(
        request,
        'ask/settings.html', {
            'tags': Tag.object1.besters(),
            'users': Author.objects.all(),
        }
    )


class RView(generic.ListView):
    template_name = 'ask/registration.html'

    def get_queryset(self):
        pass

def like(request,question_id,like_val):
    q = get_object_or_404(Question, pk=question_id)
    q.rating=q.rating-1 + 2*int(like_val)
    q.save()
    return HttpResponseRedirect(reverse('ask:index'))
