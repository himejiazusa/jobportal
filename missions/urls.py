from django.urls import path
from . import views

app_name = 'missions'

urlpatterns = [
    path('', views.mission_list, name='mission_list'),
]