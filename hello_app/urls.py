# hello_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('greet/', views.greet, name='greet'),
    path('sensor/data/', views.sensor_data, name='sensor_data'),
    path('sensor/history/', views.sensor_history, name='sensor_history'),
    path('sensor/dashboard/', views.sensor_dashboard, name='sensor_dashboard'),
    path('drag-drop-editor/', views.drag_drop_editor, name='drag_drop_editor'),
]