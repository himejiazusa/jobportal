from django.contrib import admin
from .models import Skill, JobPost, JobApplication, SavedJob

class JobPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'job_type', 'posted_date', 'is_active')
    list_filter = ('job_type', 'is_active', 'posted_date')
    search_fields = ('title', 'description', 'company__company_name')
    date_hierarchy = 'posted_date'

class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'status', 'applied_date')
    list_filter = ('status', 'applied_date')
    search_fields = ('job__title', 'applicant__username')
    date_hierarchy = 'applied_date'

admin.site.register(Skill)
admin.site.register(JobPost, JobPostAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
admin.site.register(SavedJob)