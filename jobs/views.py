from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone

from .models import JobPost, JobApplication, SavedJob, Skill
from .forms import JobPostForm, JobApplicationForm
from accounts.models import User
from missions.models import Mission, UserMission

def job_list(request):
    """求人一覧表示"""
    query = request.GET.get('q', '')
    location = request.GET.get('location', '')
    job_type = request.GET.get('job_type', '')
    
    jobs = JobPost.objects.filter(is_active=True)
    
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(skills_required__name__icontains=query)
        ).distinct()
    
    if location:
        jobs = jobs.filter(location__icontains=location)
    
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    
    return render(request, 'jobs/job_list.html', {
        'jobs': jobs,
        'query': query,
        'location': location,
        'job_type': job_type,
        'job_types': JobPost.JOB_TYPE_CHOICES
    })

def job_detail(request, job_id):
    """求人詳細表示"""
    job = get_object_or_404(JobPost, pk=job_id, is_active=True)
    
    is_saved = False
    is_applied = False
    
    if request.user.is_authenticated:
        is_saved = SavedJob.objects.filter(job=job, user=request.user).exists()
        is_applied = JobApplication.objects.filter(job=job, applicant=request.user).exists()
    
    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'is_saved': is_saved,
        'is_applied': is_applied
    })

@login_required
def save_job(request, job_id):
    """求人をお気に入りに追加"""
    if request.user.role != User.SEEKER:
        messages.warning(request, '求職者のみがこの機能を使用できます。')
        return redirect('jobs:job_detail', job_id=job_id)
    
    job = get_object_or_404(JobPost, pk=job_id, is_active=True)
    saved_job, created = SavedJob.objects.get_or_create(job=job, user=request.user)
    
    if created:
        messages.success(request, '求人をお気に入りに追加しました。')
        
        # 初めての求人保存ミッションがあれば達成
        try:
            save_mission = Mission.objects.get(name="初めての求人保存")
            user_mission, mission_created = UserMission.objects.get_or_create(
                user=request.user,
                mission=save_mission
            )
            if not user_mission.completed:
                user_mission.completed = True
                user_mission.completed_date = timezone.now()
                user_mission.save()
                
                # ポイント付与
                request.user.points += save_mission.points
                request.user.save()
                
                messages.success(request, f'「{save_mission.name}」ミッションを達成しました！ +{save_mission.points}ポイント')
        except Mission.DoesNotExist:
            pass
    else:
        messages.info(request, 'この求人は既にお気に入りに追加されています。')
    
    return redirect('jobs:job_detail', job_id=job_id)

@login_required
def unsave_job(request, job_id):
    """求人をお気に入りから削除"""
    if request.user.role != User.SEEKER:
        messages.warning(request, '求職者のみがこの機能を使用できます。')
        return redirect('jobs:job_detail', job_id=job_id)
    
    job = get_object_or_404(JobPost, pk=job_id)
    saved_job = SavedJob.objects.filter(job=job, user=request.user)
    
    if saved_job.exists():
        saved_job.delete()
        messages.success(request, '求人をお気に入りから削除しました。')
    else:
        messages.info(request, 'この求人はお気に入りに追加されていません。')
    
    return redirect('jobs:job_detail', job_id=job_id)

@login_required
def apply_job(request, job_id):
    """求人に応募"""
    if request.user.role != User.SEEKER:
        messages.warning(request, '求職者のみがこの機能を使用できます。')
        return redirect('jobs:job_detail', job_id=job_id)
    
    job = get_object_or_404(JobPost, pk=job_id, is_active=True)
    
    # 既に応募済みか確認
    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        messages.info(request, 'この求人には既に応募しています。')
        return redirect('jobs:job_detail', job_id=job_id)
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            
            messages.success(request, '応募が完了しました。選考状況はマイページで確認できます。')
            
            # 求人応募ミッションの達成
            try:
                apply_mission = Mission.objects.get(name="求人応募")
                user_mission, mission_created = UserMission.objects.get_or_create(
                    user=request.user,
                    mission=apply_mission
                )
                
                # 繰り返し達成可能なミッションか、まだ達成していないミッションの場合
                if apply_mission.is_recurring or not user_mission.completed:
                    if not user_mission.completed:
                        user_mission.completed = True
                        user_mission.completed_date = timezone.now()
                        user_mission.save()
                    
                    # ポイント付与
                    request.user.points += apply_mission.points
                    request.user.save()
                    
                    messages.success(request, f'「{apply_mission.name}」ミッションを達成しました！ +{apply_mission.points}ポイント')
            except Mission.DoesNotExist:
                pass
            
            # 5件の求人に応募ミッションがあれば確認
            application_count = JobApplication.objects.filter(applicant=request.user).count()
            if application_count >= 5:
                try:
                    apply_five_mission = Mission.objects.get(name="5件の求人に応募")
                    user_mission, mission_created = UserMission.objects.get_or_create(
                        user=request.user,
                        mission=apply_five_mission
                    )
                    
                    if not user_mission.completed:
                        user_mission.completed = True
                        user_mission.completed_date = timezone.now()
                        user_mission.save()
                        
                        # ポイント付与
                        request.user.points += apply_five_mission.points
                        request.user.save()
                        
                        messages.success(request, f'「{apply_five_mission.name}」ミッションを達成しました！ +{apply_five_mission.points}ポイント')
                except Mission.DoesNotExist:
                    pass
            
            return redirect('accounts:dashboard')
    else:
        form = JobApplicationForm()
    
    return render(request, 'jobs/apply_job.html', {
        'job': job,
        'form': form
    })

@login_required
def saved_jobs(request):
    """お気に入り求人一覧"""
    if request.user.role != User.SEEKER:
        messages.warning(request, '求職者のみがこの機能を使用できます。')
        return redirect('core:home')
    
    saved_jobs = SavedJob.objects.filter(user=request.user).select_related('job').order_by('-saved_date')
    
    return render(request, 'jobs/saved_jobs.html', {
        'saved_jobs': saved_jobs
    })

@login_required
def user_applications(request):
    """応募履歴一覧"""
    if request.user.role != User.SEEKER:
        messages.warning(request, '求職者のみがこの機能を使用できます。')
        return redirect('core:home')
    
    applications = JobApplication.objects.filter(applicant=request.user).select_related('job').order_by('-applied_date')
    
    return render(request, 'jobs/user_applications.html', {
        'applications': applications
    })

@login_required
def recommended_jobs(request):
    """おすすめ求人表示"""
    if request.user.role != User.SEEKER:
        messages.warning(request, '求職者のみがこの機能を使用できます。')
        return redirect('jobs:job_list')
    
    # 既に応募した求人は除外
    applied_job_ids = JobApplication.objects.filter(applicant=request.user).values_list('job_id', flat=True)
    
    # ユーザーのスキルに基づいて求人を検索
    try:
        user_skills = request.user.seeker_profile.skills.all()
        matching_jobs = JobPost.objects.filter(
            is_active=True, 
            skills_required__in=user_skills
        ).exclude(
            id__in=applied_job_ids
        ).distinct()
        
        # スキルの一致度でソート
        from django.db.models import Count
        matching_jobs = matching_jobs.annotate(
            skill_count=Count('skills_required', filter=Q(skills_required__in=user_skills))
        ).order_by('-skill_count')
        
        # 給与範囲でフィルタリング（オプション）
        if request.user.seeker_profile.desired_salary:
            matching_jobs = matching_jobs.filter(
                Q(salary_min__lte=request.user.seeker_profile.desired_salary) |
                Q(salary_min__isnull=True)
            ).filter(
                Q(salary_max__gte=request.user.seeker_profile.desired_salary) |
                Q(salary_max__isnull=True)
            )
        
        # 希望勤務地でフィルタリング（オプション）
        if request.user.seeker_profile.preferred_location:
            location_jobs = matching_jobs.filter(
                location__icontains=request.user.seeker_profile.preferred_location
            )
            # 希望勤務地に一致する求人がある場合は優先、なければ全てのマッチング求人を表示
            if location_jobs.exists():
                matching_jobs = location_jobs
        
    except:
        # プロフィールやスキルが設定されていない場合は、最新の求人を表示
        matching_jobs = JobPost.objects.filter(is_active=True).exclude(id__in=applied_job_ids)
    
    # 最大20件まで表示
    matching_jobs = matching_jobs[:20]
    
    return render(request, 'jobs/recommended_jobs.html', {
        'jobs': matching_jobs
    })

# 企業向け機能
@login_required
def company_jobs(request):
    """企業の掲載求人一覧"""
    if request.user.role != User.EMPLOYER:
        messages.warning(request, '企業アカウントのみがアクセスできます。')
        return redirect('core:home')
    
    try:
        company = request.user.company_profile
        jobs = JobPost.objects.filter(company=company).order_by('-posted_date')
    except:
        messages.warning(request, '企業プロフィールを先に設定してください。')
        return redirect('accounts:profile_setup')
    
    return render(request, 'jobs/company_jobs.html', {
        'jobs': jobs
    })

@login_required
def create_job(request):
    """求人の新規作成"""
    if request.user.role != User.EMPLOYER:
        messages.warning(request, '企業アカウントのみがアクセスできます。')
        return redirect('core:home')
    
    try:
        company = request.user.company_profile
    except:
        messages.warning(request, '企業プロフィールを先に設定してください。')
        return redirect('accounts:profile_setup')
    
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = company
            job.save()
            
            # 多対多リレーションシップを保存
            form.save_m2m()
            
            messages.success(request, '求人が正常に作成されました。')
            return redirect('jobs:company_jobs')
    else:
        form = JobPostForm()
    
    return render(request, 'jobs/create_job.html', {
        'form': form
    })

@login_required
def edit_job(request, job_id):
    """求人の編集"""
    if request.user.role != User.EMPLOYER:
        messages.warning(request, '企業アカウントのみがアクセスできます。')
        return redirect('core:home')
    
    try:
        company = request.user.company_profile
        job = get_object_or_404(JobPost, pk=job_id, company=company)
    except:
        messages.warning(request, 'この操作を行う権限がありません。')
        return redirect('core:home')
    
    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, '求人が正常に更新されました。')
            return redirect('jobs:company_jobs')
    else:
        form = JobPostForm(instance=job)
    
    return render(request, 'jobs/edit_job.html', {
        'form': form,
        'job': job
    })

@login_required
def view_applicants(request, job_id):
    """求人への応募者一覧"""
    if request.user.role != User.EMPLOYER:
        messages.warning(request, '企業アカウントのみがアクセスできます。')
        return redirect('core:home')
    
    try:
        company = request.user.company_profile
        job = get_object_or_404(JobPost, pk=job_id, company=company)
    except:
        messages.warning(request, 'この操作を行う権限がありません。')
        return redirect('core:home')
    
    applications = JobApplication.objects.filter(job=job).select_related('applicant')
    
    return render(request, 'jobs/view_applicants.html', {
        'job': job,
        'applications': applications
    })

@login_required
def update_application_status(request, application_id, new_status):
    """応募ステータスの更新"""
    if request.user.role != User.EMPLOYER:
        messages.warning(request, '企業アカウントのみがアクセスできます。')
        return redirect('core:home')
    
    application = get_object_or_404(JobApplication, pk=application_id)
    
    # 権限チェック
    if application.job.company.user != request.user:
        messages.warning(request, 'この操作を行う権限がありません。')
        return redirect('core:home')
    
    # ステータス更新
    valid_statuses = [status[0] for status in JobApplication.STATUS_CHOICES]
    
    if new_status in valid_statuses:
        application.status = new_status
        application.save()
        messages.success(request, '応募ステータスが更新されました。')
    else:
        messages.error(request, '無効なステータスです。')
    
    return redirect('jobs:view_applicants', job_id=application.job.id)