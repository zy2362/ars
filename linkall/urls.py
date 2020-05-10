from django.urls import path

from . import views

app_name = 'linkall'
urlpatterns = [
    path('initialize/', views.initialize, name="initialize"),
    path('submit/<int:weight>', views.submit, name="submit"),
    path('setting/', views.settings, name="settings"),
    path('dashboard', views.dashboard, name="dashboard")
]