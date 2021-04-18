from django.shortcuts import render, redirect


def index(request):
    logged = request.session.get('logged')
    if not logged:
        redirect('/')
    return render(request, 'administrator/index.html')
