from django import forms
from django.core.exceptions import ValidationError
from .models import Question, Tag
import re  # import regular expressions

t = Tag.objects.values()
idlist = []
namelist = []
for i in range(Tag.objects.count()):
    idlist.append(t[i]['id'])
    namelist.append(t[i]['name'])
    tags = list(zip(idlist, namelist))


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
        #[t.strip() for t in data.split(',') if rgx.match(t.strip())]
        data=re.findall(r'\w+', data)
        return data
