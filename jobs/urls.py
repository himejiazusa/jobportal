# jobs/urls.py
from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    # 既存のURLパターン
    path('', views.job_list, name='job_list'),
    path('<int:job_id>/', views.job_detail, name='job_detail'),
    path('<int:job_id>/save/', views.save_job, name='save_job'),
    # 以下を追加
    path('<int:job_id>/unsave/', views.unsave_job, name='unsave_job'),
    # 既存の他のURLパターン
    path('<int:job_id>/apply/', views.apply_job, name='apply_job'),
    # 以下は既存のものと思われます
    path('recommended/', views.recommended_jobs, name='recommended_jobs'),
    path('saved/', views.saved_jobs, name='saved_jobs'),
    path('applications/', views.user_applications, name='user_applications'),
    path('company/', views.company_jobs, name='company_jobs'),
    path('company/create/', views.create_job, name='create_job'),
    path('company/<int:job_id>/edit/', views.edit_job, name='edit_job'),
    path('company/<int:job_id>/applicants/', views.view_applicants, name='view_applicants'),
    path('application/<int:application_id>/status/<str:new_status>/', 
         views.update_application_status, name='update_application_status'),
]