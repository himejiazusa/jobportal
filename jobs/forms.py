from django import forms
from .models import JobPost, JobApplication, Skill

class JobPostForm(forms.ModelForm):
    """求人投稿フォーム"""
    skills_required = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='必要なスキル'
    )
    
    class Meta:
        model = JobPost
        fields = ('title', 'location', 'job_type', 'description', 'requirements', 
                  'salary_min', 'salary_max', 'skills_required', 'deadline', 'is_active')
        labels = {
            'title': '求人タイトル',
            'location': '勤務地',
            'job_type': '雇用形態',
            'description': '求人詳細',
            'requirements': '応募要件',
            'salary_min': '給与下限（万円）',
            'salary_max': '給与上限（万円）',
            'deadline': '応募締切日',
            'is_active': '掲載する'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'job_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'salary_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'salary_max': forms.NumberInput(attrs={'class': 'form-control'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

class JobApplicationForm(forms.ModelForm):
    """求人応募フォーム"""
    class Meta:
        model = JobApplication
        fields = ('cover_letter',)
        labels = {
            'cover_letter': '志望動機'
        }
        widgets = {
            'cover_letter': forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
        }