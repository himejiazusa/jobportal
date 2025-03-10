from django.contrib import admin
from .models import Mission, UserMission

class MissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'points', 'is_recurring')
    list_filter = ('is_recurring',)
    search_fields = ('name', 'description')

class UserMissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'mission', 'completed', 'completed_date')
    list_filter = ('completed', 'mission')
    search_fields = ('user__username', 'mission__name')
    date_hierarchy = 'completed_date'

admin.site.register(Mission, MissionAdmin)
admin.site.register(UserMission, UserMissionAdmin)