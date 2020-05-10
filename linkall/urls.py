from django.urls import path

from . import views

app_name = 'linkall'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/<int:id>', views.register, name='register'),
    path('claim/<int:user_id>/<int:thing_id>', views.claim, name='claim'),
    path('settings/', views.settings, name='settings'),
    path('sets/', views.sets, name="sets"),
    path('dashboard/<int:user_id>', views.dashboard, name="dashboard")
]