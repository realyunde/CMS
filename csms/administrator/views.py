from django.shortcuts import render, redirect


def index(request):
    logged = request.session.get('logged')
    if not logged:
        return redirect('/')
    return render(request, 'administrator/index.html')


def settings(request):
    if request.method == 'GET':
        return render(request, 'administrator/settings.html')
    elif request.method == 'POST':
        return render(request, 'administrator/settings.html')


def logout(request):
    request.session.flush()
    return redirect('/')
