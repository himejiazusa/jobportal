from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import Mission, UserMission

@login_required
def mission_list(request):
    """ミッション一覧表示"""
    # 企業ユーザーの場合はダッシュボードにリダイレクト
    if request.user.role == 'employer':
        messages.warning(request, 'ミッション機能は求職者向けの機能です。')
        return redirect('accounts:dashboard')
    
    # 全ミッションを取得
    all_missions = Mission.objects.all()
    
    # ユーザーのミッション達成状況を取得
    user_missions = UserMission.objects.filter(user=request.user)
    
    # ミッションの達成状態をマッピング
    mission_status = {}
    for user_mission in user_missions:
        mission_status[user_mission.mission.id] = {
            'completed': user_mission.completed,
            'completed_date': user_mission.completed_date
        }
    
    # ミッションをグループ化
    completed_missions = []
    incomplete_missions = []
    
    for mission in all_missions:
        status = mission_status.get(mission.id, {'completed': False, 'completed_date': None})
        
        mission_data = {
            'mission': mission,
            'completed': status['completed'],
            'completed_date': status['completed_date'],
        }
        
        if status['completed']:
            completed_missions.append(mission_data)
        else:
            # 繰り返し達成可能なミッションは常に未完了として表示
            if mission.is_recurring or not status['completed']:
                incomplete_missions.append(mission_data)
    
    return render(request, 'missions/mission_list.html', {
        'completed_missions': completed_missions,
        'incomplete_missions': incomplete_missions,
        'total_points': sum(mission['mission'].points for mission in completed_missions)
    })

@login_required
def complete_mission(request, mission_id):
    """手動でミッションを完了させる（開発用・一部のミッション向け）"""
    if not request.user.is_staff:  # 管理者のみ実行可能
        messages.error(request, 'この操作を行う権限がありません。')
        return redirect('missions:mission_list')
    
    try:
        mission = Mission.objects.get(pk=mission_id)
        user_mission, created = UserMission.objects.get_or_create(
            user=request.user,
            mission=mission
        )
        
        if not user_mission.completed or mission.is_recurring:
            user_mission.completed = True
            user_mission.completed_date = timezone.now()
            user_mission.save()
            
            # ポイント付与
            request.user.points += mission.points
            request.user.save()
            
            messages.success(request, f'「{mission.name}」ミッションを達成しました！ +{mission.points}ポイント')
        else:
            messages.info(request, 'このミッションは既に達成しています。')
    except Mission.DoesNotExist:
        messages.error(request, '指定されたミッションが見つかりません。')
    
    return redirect('missions:mission_list')