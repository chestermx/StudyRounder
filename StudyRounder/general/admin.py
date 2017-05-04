from django.contrib import admin
from .models import SRUser, Question


class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        ("username", {"fields": ["username"]}),
        ('password', {'fields': ['password']}),
        ('is_active', {'fields': ['is_active']}),
        ('is_staff', {'fields': ['is_staff']}),
    ]


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("title", {"fields": ["title"]}),
        ("text", {"fields": ["text"]}),
        ("clear_user", {"fields": ["clear_user"]}),
    ]

admin.site.register(SRUser, UserAdmin)
admin.site.register(Question, QuestionAdmin)
