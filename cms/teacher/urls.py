from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='teacher_index'),
    path('settings', views.settings, name='teacher_settings'),
    path('course', views.teacher_course, name='teacher_course'),
    path('score', views.teacher_score, name='teacher_score'),
    path('logout', views.logout, name='teacher_logout'),
]
