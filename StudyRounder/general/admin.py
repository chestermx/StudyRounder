from django.contrib import admin
from .models import SRUser, Question, Category


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
        ("category", {"fields": ["category"]}),
        ("point", {"fields": ["point"]}),
        ("image", {"fields": ["image"]}),
        ("clear_user", {"fields": ["clear_user"]}),
    ]


class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        ("name", {"fields": ["name"]}),
    ]

admin.site.register(SRUser, UserAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Category, CategoryAdmin)
