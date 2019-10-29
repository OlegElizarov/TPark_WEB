from django.contrib import admin
from ask import models

admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.Tag)