from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from ask.models import Question, Answer, Tag, QuestionManager, TagManager, Author, LikeDislike
from .forms import questionform
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse


def paginator(request, obj, per_pages):
    pag = Paginator(obj, per_pages)
    page = request.GET.get('page')
    return pag.get_page(page)


def tag(request, tag_name):
    q = Question.objects.filter(tags__name__contains=tag_name)
    question_list = paginator(request, q, 2)
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
    question_list = paginator(request, q, 2)
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
    answer_list = paginator(request, a, 2)
    return render(
        request,
        'ask/question.html', {
            'question': q,
            'answer_list': answer_list,
            'tags': Tag.object1.besters(),
            'question_list': answer_list,
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
            q = Question(title=form.cleaned_data['title'], text=form.cleaned_data['text'],
                         author=get_object_or_404(Author, user=request.user), pub_date=timezone.now(), rating=0)
            q.save()
            for tg in form.cleaned_data['tag']:
                q.tags.add(Tag.objects.get(id=tg))
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


def like(request, object_id, like_val, typ_obj):
    if typ_obj != '0':
        q = get_object_or_404(Question, pk=object_id)
        if (LikeDislike.objects.filter(author=get_object_or_404(Author, user=request.user), question=q,
                                       like_type=int(like_val)).count() == 0):
            if (LikeDislike.objects.filter(author=get_object_or_404(Author, user=request.user), question=q,
                                           like_type=(int(like_val)) ^ 1).count() != 0):
                LikeDislike.objects.filter(author=get_object_or_404(Author, user=request.user), question=q,
                                           like_type=(int(like_val)) ^ 1).delete()
                q.rating = q.rating - 1 + 2 * int(like_val)
            LikeDislike.objects.create(author=get_object_or_404(Author, user=request.user), question=q,
                                       like_type=int(like_val))
            q.rating = q.rating - 1 + 2 * int(like_val)
            q.save()
        return HttpResponseRedirect(reverse('ask:index'))
    else:
        a = get_object_or_404(Answer, pk=object_id)
        if (LikeDislike.objects.filter(author=get_object_or_404(Author, user=request.user), answer=a,
                                       like_type=int(like_val)).count() == 0):
            if (LikeDislike.objects.filter(author=get_object_or_404(Author, user=request.user), answer=a,
                                           like_type=(int(like_val)) ^ 1).count() != 0):
                LikeDislike.objects.filter(author=get_object_or_404(Author, user=request.user), answer=a,
                                           like_type=(int(like_val)) ^ 1).delete()
                a.rating = a.rating - 1 + 2 * int(like_val)
            LikeDislike.objects.create(author=get_object_or_404(Author, user=request.user), answer=a,
                                       like_type=int(like_val))
            a.rating = a.rating - 1 + 2 * int(like_val)
            a.save()
        q = a.question
        q = q.id
        return HttpResponseRedirect(reverse('ask:question', kwargs={'question_id': q}))
