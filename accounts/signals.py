# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, SeekerProfile, CompanyProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """ユーザー作成時にプロフィールを自動作成"""
    if created:
        if instance.role == User.SEEKER:
            SeekerProfile.objects.create(user=instance)
        elif instance.role == User.EMPLOYER:
            CompanyProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """ユーザープロフィールの保存"""
    if instance.role == User.SEEKER:
        if hasattr(instance, 'seeker_profile'):
            instance.seeker_profile.save()
    elif instance.role == User.EMPLOYER:
        if hasattr(instance, 'company_profile'):
            instance.company_profile.save()