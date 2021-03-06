from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='admin_index'),
    path('settings', views.settings, name='admin_settings'),
    path('logout', views.logout, name='admin_logout'),
    path('course', views.admin_course, name='admin_course'),
    path('teacher', views.admin_teacher, name='admin_teacher'),
    path('student', views.admin_student, name='admin_student'),
]
