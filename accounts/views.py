from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import User, SeekerProfile, CompanyProfile
from .forms import UserRegistrationForm, SeekerProfileForm, CompanyProfileForm
from missions.models import Mission, UserMission

def register(request):
    """ユーザー登録ビュー"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # ユーザー登録ミッションの処理
            try:
                register_mission = Mission.objects.get(name="ユーザー登録")
                user_mission, created = UserMission.objects.get_or_create(
                    user=user,
                    mission=register_mission
                )
                if not user_mission.completed:
                    user_mission.completed = True
                    user_mission.completed_date = timezone.now()
                    user_mission.save()
                    
                    # ポイント付与
                    user.points += register_mission.points
                    user.save()
            except Mission.DoesNotExist:
                # ミッションが存在しない場合は何もしない
                pass
            
            login(request, user)
            messages.success(request, '登録が完了しました。プロフィールを設定してください。')
            return redirect('accounts:profile_setup')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {
        'form': form
    })

@login_required
def profile_setup(request):
    """プロフィール初期設定ビュー"""
    user = request.user
    
    # プロフィールが既に設定されている場合はリダイレクト
    if user.profile_completed:
        messages.info(request, 'プロフィールは既に設定されています。')
        return redirect('accounts:dashboard')
    
    if user.role == User.SEEKER:
        if request.method == 'POST':
            form = SeekerProfileForm(request.POST, request.FILES, instance=getattr(user, 'seeker_profile', None))
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = user
                profile.save()
                
                # 多対多リレーションシップを保存
                form.save_m2m()
                
                # プロフィール設定ミッションの処理
                try:
                    profile_mission = Mission.objects.get(name="プロフィール作成")
                    user_mission, created = UserMission.objects.get_or_create(
                        user=user,
                        mission=profile_mission
                    )
                    if not user_mission.completed:
                        user_mission.completed = True
                        user_mission.completed_date = timezone.now()
                        user_mission.save()
                        
                        # ポイント付与
                        user.points += profile_mission.points
                        user.save()
                except Mission.DoesNotExist:
                    pass
                
                # プロフィール完了フラグを設定
                user.profile_completed = True
                user.save()
                
                messages.success(request, 'プロフィールが設定されました。')
                return redirect('accounts:dashboard')
        else:
            form = SeekerProfileForm(instance=getattr(user, 'seeker_profile', None))
        
        return render(request, 'accounts/seeker_profile_setup.html', {
            'form': form
        })
    
    elif user.role == User.EMPLOYER:
        if request.method == 'POST':
            form = CompanyProfileForm(request.POST, request.FILES, instance=getattr(user, 'company_profile', None))
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = user
                profile.save()
                
                # プロフィール完了フラグを設定
                user.profile_completed = True
                user.save()
                
                messages.success(request, '企業プロフィールが設定されました。')
                return redirect('accounts:dashboard')
        else:
            form = CompanyProfileForm(instance=getattr(user, 'company_profile', None))
        
        return render(request, 'accounts/company_profile_setup.html', {
            'form': form
        })
    
    # その他のロールの場合
    messages.warning(request, '無効なユーザータイプです。')
    return redirect('core:home')

@login_required
def edit_profile(request):
    """プロフィール編集ビュー"""
    user = request.user
    
    if user.role == User.SEEKER:
        if request.method == 'POST':
            form = SeekerProfileForm(request.POST, request.FILES, instance=user.seeker_profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'プロフィールが更新されました。')
                return redirect('accounts:dashboard')
        else:
            form = SeekerProfileForm(instance=user.seeker_profile)
        
        return render(request, 'accounts/seeker_profile_edit.html', {
            'form': form
        })
    
    elif user.role == User.EMPLOYER:
        if request.method == 'POST':
            form = CompanyProfileForm(request.POST, request.FILES, instance=user.company_profile)
            if form.is_valid():
                form.save()
                messages.success(request, '企業プロフィールが更新されました。')
                return redirect('accounts:dashboard')
        else:
            form = CompanyProfileForm(instance=user.company_profile)
        
        return render(request, 'accounts/company_profile_edit.html', {
            'form': form
        })
    
    # その他のロールの場合
    messages.warning(request, '無効なユーザータイプです。')
    return redirect('core:home')

@login_required
def dashboard(request):
    """ユーザーダッシュボードビュー"""
    user = request.user
    
    # プロフィールが設定されていない場合はプロフィール設定ページにリダイレクト
    if not user.profile_completed:
        messages.info(request, 'まずプロフィールを設定してください。')
        return redirect('accounts:profile_setup')
    
    context = {
        'user': user
    }
    
    if user.role == User.SEEKER:
        # 求職者向けダッシュボード情報
        from jobs.models import JobApplication, SavedJob
        
        # 応募した求人
        applications = JobApplication.objects.filter(applicant=user).select_related('job')
        context['applications'] = applications
        
        # お気に入り求人
        saved_jobs = SavedJob.objects.filter(user=user).select_related('job')
        context['saved_jobs'] = saved_jobs
        
        # ミッション達成状況
        missions = UserMission.objects.filter(user=user, completed=True).select_related('mission')
        context['completed_missions'] = missions
        
        return render(request, 'accounts/seeker_dashboard.html', context)
    
    elif user.role == User.EMPLOYER:
        # 企業向けダッシュボード情報
        from jobs.models import JobPost
        
        # 掲載中の求人
        jobs = JobPost.objects.filter(company=user.company_profile)
        context['jobs'] = jobs
        
        # 応募者数の集計
        from django.db.models import Count
        jobs_with_application_count = jobs.annotate(application_count=Count('jobapplication'))
        context['jobs_with_application_count'] = jobs_with_application_count
        
        return render(request, 'accounts/company_dashboard.html', context)
    
    # その他のロールの場合
    return render(request, 'accounts/dashboard.html', context)