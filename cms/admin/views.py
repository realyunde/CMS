from django.shortcuts import render, redirect


def index(request):
    user = request.session.get('user')
    if not user:
        return redirect('/')
    return render(request, 'admin/index.html')


def settings(request):
    if request.method == 'GET':
        return render(request, 'admin/settings.html')
    elif request.method == 'POST':
        return render(request, 'admin/settings.html')


def logout(request):
    request.session.clear()
    request.session.flush()
    return redirect('/')
