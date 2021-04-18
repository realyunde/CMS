from django.shortcuts import render, redirect


def index(request):
    logged = request.session.get('logged')
    if not logged:
        return redirect('/')
    return render(request, 'admin/index.html')


def settings(request):
    if request.method == 'GET':
        return render(request, 'admin/settings.html')
    elif request.method == 'POST':
        return render(request, 'admin/settings.html')


def logout(request):
    request.session.flush()
    return redirect('/')
