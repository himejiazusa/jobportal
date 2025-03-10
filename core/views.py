from django.shortcuts import render
from jobs.models import JobPost

def home(request):
    """ホームページ表示"""
    context = {}
    
    # 企業ユーザーの場合、掲載中の求人を取得
    if request.user.is_authenticated and request.user.role == 'employer':
        try:
            from jobs.models import JobPost
            from django.db.models import Count
            
            company = request.user.company_profile
            jobs = JobPost.objects.filter(company=company).order_by('-posted_date')
            
            # 応募者数を取得
            jobs = jobs.annotate(application_count=Count('jobapplication'))
            
            context['jobs'] = jobs
        except:
            # プロフィールがない場合や他のエラーの場合は何も表示しない
            pass
    
    # 最新の求人を取得（求職者や未ログインユーザー用）
    elif not request.user.is_authenticated or request.user.role == 'seeker':
        try:
            from jobs.models import JobPost
            latest_jobs = JobPost.objects.filter(is_active=True).order_by('-posted_date')[:5]
            context['latest_jobs'] = latest_jobs
        except:
            pass
    
    return render(request, 'core/home.html', context)

def about(request):
    """サイト情報ページ"""
    return render(request, 'core/about.html')