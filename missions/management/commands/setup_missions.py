# missions/management/commands/setup_missions.py
from django.core.management.base import BaseCommand
from missions.models import Mission

class Command(BaseCommand):
    help = '初期ミッションの設定'
    
    def handle(self, *args, **options):
        # 基本的なミッションの作成
        missions = [
            {
                'name': 'ユーザー登録',
                'description': 'サイトに登録してアカウントを作成する',
                'points': 10,
                'is_recurring': False
            },
            {
                'name': 'プロフィール作成',
                'description': '基本情報を入力してプロフィールを完成させる',
                'points': 10,
                'is_recurring': False
            },
            # 他のミッション...
        ]
        
        for mission_data in missions:
            Mission.objects.get_or_create(
                name=mission_data['name'],
                defaults={
                    'description': mission_data['description'],
                    'points': mission_data['points'],
                    'is_recurring': mission_data['is_recurring']
                }
            )
        
        self.stdout.write(self.style.SUCCESS('ミッションが正常に設定されました'))