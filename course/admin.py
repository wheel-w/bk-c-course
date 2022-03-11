from django.contrib import admin
from course.models import *


# Register your models here.
class Admin(admin.ModelAdmin):
    pass


admin.site.register(Course, Admin)
admin.site.register(UserCourseContact, Admin)
admin.site.register(Member, Admin)
admin.site.register(Chapter, Admin)
admin.site.register(Question, Admin)
admin.site.register(Paper, Admin)
admin.site.register(CustomType, Admin)
admin.site.register(PaperQuestionContact, Admin)
admin.site.register(StudentAnswer, Admin)
admin.site.register(StudentPaperContact, Admin)
