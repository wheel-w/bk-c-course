from django.contrib import admin

from .models import User, UserTag, UserTagContact


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_filter = ("u_id", "name", "gender", "phone_number")


class UserTagAdmin(admin.ModelAdmin):
    list_filter = ("tag_value", "tag_color", "is_built_in", "sub_project")


class UserTagContactAdmin(admin.ModelAdmin):
    list_filter = ("id", "user_id", "tag_id")


admin.site.register(User, UserAdmin)
admin.site.register(UserTag, UserTagAdmin)
admin.site.register(UserTagContact, UserTagContactAdmin)
