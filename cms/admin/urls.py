from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='admin_index'),
    path('settings', views.settings, name='admin_settings'),
    path('logout', views.logout, name='admin_logout'),
    path('school', views.admin_school, name='admin_school'),
]
