from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='student_index'),
    path('settings', views.settings, name='student_settings'),
    path('select', views.select, name='student_select'),
    path('list', views.list_course, name='student_list_course'),
    path('logout', views.logout, name='student_logout'),
]
