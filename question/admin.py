from django.contrib import admin

from .models import Question, QuestionTag, QuestionTagContact

# Register your models here.
admin.site.register(Question)
admin.site.register(QuestionTag)
admin.site.register(QuestionTagContact)
