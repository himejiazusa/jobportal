from django.db import models
from django.conf import settings

class Skill(models.Model):
    """スキルモデル"""
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class JobPost(models.Model):
    """求人情報モデル"""
    FULL_TIME = 'full_time'
    PART_TIME = 'part_time'
    CONTRACT = 'contract'
    INTERNSHIP = 'internship'
    
    JOB_TYPE_CHOICES = [
        (FULL_TIME, '正社員'),
        (PART_TIME, 'パート・アルバイト'),
        (CONTRACT, '契約社員'),
        (INTERNSHIP, 'インターンシップ'),
    ]
    
    title = models.CharField(max_length=100)
    company = models.ForeignKey('accounts.CompanyProfile', on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    description = models.TextField()
    requirements = models.TextField()
    salary_min = models.IntegerField(blank=True, null=True)
    salary_max = models.IntegerField(blank=True, null=True)
    skills_required = models.ManyToManyField(Skill, blank=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title

class JobApplication(models.Model):
    """求人応募モデル"""
    APPLIED = 'applied'
    SCREENING = 'screening'
    INTERVIEW = 'interview'
    OFFER = 'offer'
    REJECTED = 'rejected'
    ACCEPTED = 'accepted'
    
    STATUS_CHOICES = [
        (APPLIED, '応募済み'),
        (SCREENING, '書類選考中'),
        (INTERVIEW, '面接中'),
        (OFFER, '内定'),
        (REJECTED, '不採用'),
        (ACCEPTED, '内定承諾'),
    ]
    
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    applied_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=APPLIED)
    cover_letter = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('job', 'applicant')
        
    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"

class SavedJob(models.Model):
    """お気に入り求人モデル"""
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    saved_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('job', 'user')
        
    def __str__(self):
        return f"{self.user.username} - {self.job.title}"