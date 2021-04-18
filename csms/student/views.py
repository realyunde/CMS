from django.shortcuts import render, redirect


def index(request):
    return render(request, 'student/index.html')


def settings(request):
    return render(request, 'student/settings.html')


def logout(request):
    request.session.clear()
    request.session.flush()
    return redirect('/')
