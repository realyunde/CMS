from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='student_index'),
    path('settings', views.settings, name='student_settings'),
    path('logout', views.logout, name='student_logout'),
]
