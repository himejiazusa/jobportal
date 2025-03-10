from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    """カスタムユーザーモデル"""
    SEEKER = 'seeker'
    EMPLOYER = 'employer'
    ADMIN = 'admin'
    
    ROLE_CHOICES = [
        (SEEKER, '求職者'),
        (EMPLOYER, '企業'),
        (ADMIN, '管理者'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=SEEKER)
    points = models.IntegerField(default=0)
    profile_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username

class SeekerProfile(models.Model):
    """求職者プロフィールモデル"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seeker_profile')
    skills = models.ManyToManyField('jobs.Skill', blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    desired_salary = models.IntegerField(blank=True, null=True)
    preferred_location = models.CharField(max_length=100, blank=True)
    years_experience = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username}のプロフィール"

class CompanyProfile(models.Model):
    """企業プロフィールモデル"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company_profile')
    company_name = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    description = models.TextField()
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    founded_year = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.company_name