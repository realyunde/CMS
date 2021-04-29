from django.shortcuts import render, redirect
import cms.auth.auth as auth


def index(request):
    return render(request, 'teacher/index.html')


def settings(request):
    return render(request, 'teacher/settings.html')


def logout(request):
    auth.logout(request)
    return redirect('auth_index')
