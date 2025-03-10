from django.db import models

# coreアプリにはモデルがなく、主にビューやテンプレートを提供します
# 必要に応じて、将来的に共通モデルを追加することができます

# 例えば、以下のようなモデルを追加することができます
# class SystemSettings(models.Model):
#     """システム設定モデル"""
#     key = models.CharField(max_length=100, unique=True)
#     value = models.TextField()
#     description = models.TextField(blank=True)
#     
#     def __str__(self):
#         return self.key