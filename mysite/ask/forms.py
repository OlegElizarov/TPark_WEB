from django import forms
from django.core.exceptions import ValidationError
from .models import Question, Tag, Author
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.forms import ModelForm

import re  # import regular expressions

t = Tag.objects.values()
idlist = []
namelist = []
for i in range(Tag.objects.count()):
    idlist.append(t[i]['id'])
    namelist.append(t[i]['name'])
    tags = list(zip(idlist, namelist))


class answerform(forms.Form):
    title = forms.CharField(widget=forms.Textarea(attrs={'class': 'col-3 control-label', 'required': True, 'style':'height:40px'}))
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'col-3 control-label', 'required': True, 'style':'height:40px'}))

    def clean_text(self):
        data = self.cleaned_data['text']
        return data

    def clean_title(self):
        data = self.cleaned_data['title']
        return data

    def clean(self):
        cleaned_data = super(answerform, self).clean()
        return cleaned_data


class questionform(forms.Form):
    title = forms.CharField()
    text = forms.CharField(widget=forms.Textarea)
    # tag = forms.MultipleChoiceField(choices=tags)
    tag = forms.CharField(widget=forms.Textarea)

    def clean(self):
        cleaned_data = super(questionform, self).clean()
        return cleaned_data

    def clean_tag(self):
        data = self.cleaned_data['tag']
        rgx = re.compile('^[a-zA-Z]+$')
        # rgx = re.compile('^\w+$')
        # [t.strip() for t in data.split(',') if rgx.match(t.strip())]
        data = re.findall(r'\w+', data)
        return data


class RegistrationForm(forms.Form):
    nickname = forms.CharField()
    email = forms.EmailField(initial='email',
                             widget=forms.EmailInput(attrs={'class': 'col-5 control-label', 'required': True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'col-3 control-label', 'required': True}))
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'col-3 control-label', 'required': True}))
    avatar = forms.ImageField()

    def clean(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        password = self.cleaned_data.get('password')

        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')

        cleaned_data = super(RegistrationForm, self).clean()
        return cleaned_data

    def clean_nickname(self):
        data = self.cleaned_data['nickname']
        return data

    def save(self, commit=True):
        u = User(username=self.cleaned_data.get('nickname'))
        u.set_password(self.cleaned_data.get('password'))
        u.save()
        return u


class SettingForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['avatar', 'nickname']
        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'col-5 control-label', 'required': True})}

    email = forms.EmailField(initial='email',
                             widget=forms.EmailInput(attrs={'class': 'col-4 control-label', 'required': True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'col-4 control-label', 'required': True}))

    def __init__(self, author, *args, **kwargs):
        self.author = author
        super(SettingForm, self).__init__(*args, **kwargs)

    def save(self):
        a = self.author
        u = a.user
        a.nickname = self.cleaned_data['nickname']
        u.email = self.cleaned_data['email']
        a.avatar = self.cleaned_data['avatar']
        u.save()
        a.save()
        return a
