from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('logout', views.logout, name='admin_logout'),
]