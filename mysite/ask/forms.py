from django import forms
from django.core.exceptions import ValidationError
from .models import Question, Tag

t = Tag.objects.values()
idlist = []
namelist = []
for i in range(Tag.objects.count()):
    # tags = (tags) + list((t[i]['id'] , t[i]['name']))
    idlist.append(t[i]['id'])
    namelist.append(t[i]['name'])
    tags = list(zip(idlist, namelist))

OPTIONS = (
    ("a", "A"),
    ("b", "B"),
)

print(tuple(tags))
print((OPTIONS))


class questionform(forms.Form):
    title = forms.CharField()
    text = forms.CharField()
    tag = forms.MultipleChoiceField(choices=tags)

    def clean(self):
        cleaned_data = super(questionform, self).clean()
        return cleaned_data
