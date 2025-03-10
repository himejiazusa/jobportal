from django.db import models
from django.conf import settings
from django.utils import timezone

class Mission(models.Model):
    """ミッションモデル"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    points = models.IntegerField(default=10)
    is_recurring = models.BooleanField(default=False)  # 繰り返し達成可能なミッションか
    
    def __str__(self):
        return self.name

class UserMission(models.Model):
    """ユーザーミッション達成状況モデル"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        unique_together = ('user', 'mission')
        
    def __str__(self):
        status = "完了" if self.completed else "未完了"
        return f"{self.user.username} - {self.mission.name} ({status})"
        
    def complete(self):
        """ミッションを完了状態にする"""
        if not self.completed:
            self.completed = True
            self.completed_date = timezone.now()
            self.save()
            
            # ポイント付与処理
            user = self.user
            user.points += self.mission.points
            user.save()