# hello_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 新增根路径映射
    path('greet/', views.greet, name='greet'),
]
