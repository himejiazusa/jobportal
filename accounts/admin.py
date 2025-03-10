from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, SeekerProfile, CompanyProfile

class CustomUserAdmin(UserAdmin):
    """カスタムユーザー管理画面"""
    list_display = ('username', 'email', 'role', 'points', 'profile_completed', 'is_staff')
    list_filter = ('role', 'profile_completed', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('追加情報', {'fields': ('role', 'points', 'profile_completed')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(SeekerProfile)
admin.site.register(CompanyProfile)