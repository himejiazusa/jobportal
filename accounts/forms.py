from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, SeekerProfile, CompanyProfile

class UserRegistrationForm(UserCreationForm):
    """ユーザー登録フォーム"""
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, label='アカウントタイプ')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password1', 'password2')

class SeekerProfileForm(forms.ModelForm):
    """求職者プロフィールフォーム"""
    class Meta:
        model = SeekerProfile
        fields = ('skills', 'resume', 'desired_salary', 'preferred_location', 'years_experience')
        widgets = {
            'skills': forms.CheckboxSelectMultiple(),
        }

class CompanyProfileForm(forms.ModelForm):
    """企業プロフィールフォーム"""
    class Meta:
        model = CompanyProfile
        fields = ('company_name', 'industry', 'description', 'website', 'logo', 'founded_year')