from django.contrib import admin

from .models import (
    Chapter,
    Course,
    CustomType,
    Member,
    Paper,
    PaperQuestionContact,
    Question,
    StudentAnswer,
    StudentPaperContact,
    UserCourseContact,
)


# Register your models here.
class Admin(admin.ModelAdmin):
    pass


class MemberAdmin(admin.ModelAdmin):
    list_filter = ("id", "username", "class_number", "name")
    list_display = ("id", "username", "openid", "class_number", "name", "identity")


class CourseAdmin(admin.ModelAdmin):
    list_filter = ("id", "course_name", "teacher", "create_people")
    list_display = ("id", "course_name", "teacher", "create_people")


class UserCourseContactAdmin(admin.ModelAdmin):
    list_filter = (
        "id",
        "user_id",
        "course_id",
    )
    list_display = ("id", "user_id", "course_id")


class ChapterAdmin(admin.ModelAdmin):
    list_filter = (
        "id",
        "course_id",
        "chapter_name",
    )
    list_display = ("id", "course_id", "chapter_name")


class QuestionAdmin(admin.ModelAdmin):
    list_filter = ("id", "course_id", "chapter_id", "types")
    list_display = ("id", "course_id", "chapter_id", "types", "question", "answer")


class CustomTypeAdmin(admin.ModelAdmin):
    list_filter = ("id", "course_id", "custom_type_name")
    list_display = ("id", "course_id", "custom_type_name")


class PaperAdmin(admin.ModelAdmin):
    list_filter = ("id", "types", "course_id", "paper_name", "teacher")
    list_display = (
        "id",
        "types",
        "course_id",
        "chapter_id",
        "paper_name",
        "teacher",
        "status",
    )


class PaperQuestionContactAdmin(admin.ModelAdmin):
    list_filter = ("id", "paper_id", "types", "question_id")
    list_display = ("id", "paper_id", "types", "score", "question_id", "question")


class StudentAnswerAdmin(admin.ModelAdmin):
    list_filter = ("id", "student_id", "PQContact_id")
    list_display = ("id", "student_id", "PQContact_id", "answer", "score")


class StudentPaperContactAdmin(admin.ModelAdmin):
    list_filter = ("id", "course_id", "paper_id", "student_id")
    list_display = ("id", "course_id", "paper_id", "student_id", "status", "score")


admin.site.register(Course, CourseAdmin)
admin.site.register(UserCourseContact, UserCourseContactAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Paper, PaperAdmin)
admin.site.register(CustomType, CustomTypeAdmin)
admin.site.register(PaperQuestionContact, PaperQuestionContactAdmin)
admin.site.register(StudentAnswer, StudentAnswerAdmin)
admin.site.register(StudentPaperContact, StudentPaperContactAdmin)
