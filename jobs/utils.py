# jobs/utils.py
from django.db import models
from accounts.models import SeekerProfile
from .models import JobPost

def get_matching_jobs(user, limit=10):
    """ユーザープロフィールに基づいて求人をマッチングする"""
    try:
        profile = user.seeker_profile
    except SeekerProfile.DoesNotExist:
        return JobPost.objects.filter(is_active=True)[:limit]
    
    # ユーザーのスキルに基づくマッチング
    user_skills = profile.skills.all()
    
    matching_jobs = JobPost.objects.filter(
        is_active=True,
        skills_required__in=user_skills
    ).distinct()
    
    # スキルの一致数でソート
    from django.db.models import Count
    matching_jobs = matching_jobs.annotate(
        matching_skills_count=Count('skills_required', filter=models.Q(skills_required__in=user_skills))
    ).order_by('-matching_skills_count')
    
    # その他の条件でフィルタリング（必要に応じて）
    
    return matching_jobs[:limit]