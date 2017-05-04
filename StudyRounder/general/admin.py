from django.contrib import admin
from .models import SRUser


class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        ("username", {"fields": ["username"]}),
        ('password', {'fields': ['password']}),
        ('is_active', {'fields': ['is_active']}),
        ('is_staff', {'fields': ['is_staff']}),
    ]

admin.site.register(SRUser, UserAdmin)