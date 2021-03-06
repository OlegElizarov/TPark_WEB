from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
import json
from ask.models import Question, Answer, Tag, QuestionManager, TagManager, Author, LikeDislike
from django.contrib.auth.models import User
from .forms import questionform, RegistrationForm, SettingForm, answerform
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login


def paginator(request, obj, per_pages):
    pag = Paginator(obj, per_pages)
    page = request.GET.get('page')
    return pag.get_page(page)


def logged_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('ask:index'))


def logged_in(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('ask:index'))
    if request.method == "GET":
        return render(
            request,
            'ask/login.html',
            {
                'tags': Tag.objects.besters(),
                'users': Author.objects.all(),
            }
        )
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                redirect_to = request.GET.get('next', 'index')
                print(redirect_to)
                return HttpResponseRedirect(redirect_to)
            else:
                return render(
                    request,
                    'ask/login.html',
                    {
                        'tags': Tag.objects.besters(),
                        'users': Author.objects.all(),
                        'error': 'error',
                    }
                )


def tag(request, tag_name):
    q = Question.objects.filter(tags__name__contains=tag_name)
    question_list = paginator(request, q, 2)
    return render(
        request,
        'ask/tag.html', {
            'tag_name': tag_name,
            'tags': Tag.objects.besters(),
            'question_list': question_list,
            'users': Author.objects.all(),
        }
    )


def index(request):
    q = Question.objects.besters()
    question_list = paginator(request, q, 2)
    return render(
        request,
        'ask/index.html', {
            'question_list': question_list,
            'tags': Tag.objects.besters(),
            'users': Author.objects.all()
        }
    )


def question(request, question_id):
    if request.method == "GET":
        q = get_object_or_404(Question, pk=question_id)
        a = q.answer_set.all()
        answer_list = paginator(request, a, 2)
        form = answerform()
        return render(
            request,
            'ask/question.html', {
                'question': q,
                'answer_list': answer_list,
                'tags': Tag.objects.besters(),
                'question_list': answer_list,
                'users': Author.objects.all(),
                'form': form,
            }
        )
    if request.method == "POST":
        q = get_object_or_404(Question, pk=question_id)
        form = answerform(request.POST)
        if form.is_valid():
            a = Answer(question=q, text=form.cleaned_data['text'], title=form.cleaned_data['title'],
                       author=request.user.author, correct=False, pub_date=timezone.now())
            a.save()
            return HttpResponseRedirect(reverse('ask:question', kwargs={'question_id': question_id}))


def base(request):
    return render(
        request,
        'ask/base.html', {
            'tags': Tag.objects.besters(),
            'users': Author.objects.all(),
        }
    )


@login_required
def ask(request):
    form = questionform()
    if request.method == "POST":
        form = questionform(request.POST)
        if form.is_valid():
            q = Question(title=form.cleaned_data['title'], text=form.cleaned_data['text'],
                         author=get_object_or_404(Author, user=request.user), pub_date=timezone.now(), rating=0)
            q.save()
            for tg in form.cleaned_data['tag']:
                Tag.objects.get_or_create(name=tg)
                q.tags.add(Tag.objects.get(name=tg))
                qid = q.id
            return HttpResponseRedirect(reverse('ask:question', kwargs={'question_id': qid}))
    return render(
        request,
        'ask/question_create.html',
        {
            'form': form,
            'users': Author.objects.all(),
            'tags': Tag.objects.besters(),

        }
    )


@login_required
def settings(request):
    if request.method == "GET":
        form = SettingForm(request.user, initial={'nickname': request.user.author.nickname,
                                                  'email': request.user.email, 'user': request.user})
        form.user = request.user
        return render(
            request,
            'ask/settings.html', {
                'form': form,
                'tags': Tag.objects.besters(),
                'users': Author.objects.all(),
            }
        )
    if request.method == "POST":
        form = SettingForm(request.user.author, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ask:index'))
        else:
            form = SettingForm(request.user)
        return render(
            request,
            'ask/settings.html',
            {
                'form': form,
                'users': Author.objects.all(),
                'tags': Tag.objects.besters(),
            }
        )


# ВАЖНО СПРОСИТЬ из тегов не верный запрос на картинки идет!!!

class RView(View):

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('ask:index'))
        form = kwargs.get('form', RegistrationForm())
        return render(
            request,
            'registration.html', {
                'tags': Tag.objects.besters(),
                'users': Author.objects.all(),
                'form': form,
            }
        )

    def post(self, request):
        form = RegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            u = form.save()
            a = u.author
            a.nickname = form.cleaned_data['nickname']
            # a.avatar=request.FILES

            a.save()
            print(a)
            # print()
            # print(Author.objects.all())
            login(request, u)

            return HttpResponseRedirect(reverse('ask:index'))
        else:
            return self.get(request, form=form)


# неготовая часть
@csrf_exempt
@require_POST
def like(request):
    post = request.POST.get('post', None)
    obj = get_object_or_404(Question, id=post)
    method = request.POST.get('method', None)
    ctx = {'message': 'OK'}
    print(method)
    print(post)
    print(obj)
    if (method == 'like'):
        obj.rating += 1
    else:
        if (method == 'dislike'):
            obj.rating -= 1
        else:
            ctx = {'message': 'error_method'}
    obj.save()
    return HttpResponse(json.dumps(ctx), content_type='application/json')
    # if typ_obj != '0':
    #     q = get_object_or_404(Question, pk=object_id)
    #     if (LikeDislike.objects.filter(author=get_object_or_404(Author, user=request.user), question=q,
    #                                    like_type=int(like_val)).count() == 0):
    #         if (LikeDislike.objects.filter(author=get_object_or_404(Author, user=request.user), question=q,
    #                                        like_type=(int(like_val)) ^ 1).count() != 0):
    #             LikeDislike.objects.filter(author=get_object_or_404(Author, user=request.user), question=q,
    #                                        like_type=(int(like_val)) ^ 1).delete()
    #             q.rating = q.rating - 1 + 2 * int(like_val)
    #         LikeDislike.objects.create(author=get_object_or_404(Author, user=request.user), question=q,
    #                                    like_type=int(like_val))
    #         q.rating = q.rating - 1 + 2 * int(like_val)
    #         q.save()
    #     return HttpResponseRedirect(reverse('ask:index'))
    # else:
    #     a = get_object_or_404(Answer, pk=object_id)
    #     if (LikeDislike.objects.filter(author=get_object_or_404(Author, user=request.user), answer=a,
    #                                    like_type=int(like_val)).count() == 0):
    #         if (LikeDislike.objects.filter(author=get_object_or_404(Author, user=request.user), answer=a,
    #                                        like_type=(int(like_val)) ^ 1).count() != 0):
    #             LikeDislike.objects.filter(author=get_object_or_404(Author, user=request.user), answer=a,
    #                                        like_type=(int(like_val)) ^ 1).delete()
    #             a.rating = a.rating - 1 + 2 * int(like_val)
    #         LikeDislike.objects.create(author=get_object_or_404(Author, user=request.user), answer=a,
    #                                    like_type=int(like_val))
    #         a.rating = a.rating - 1 + 2 * int(like_val)
    #         a.save()
    #     q = a.question
    #     q = q.id
    #     return HttpResponseRedirect(reverse('ask:question', kwargs={'question_id': q}))

# request.GET.get('r')
# Response.objects.filter(pk=r).first()
# form= formname()
