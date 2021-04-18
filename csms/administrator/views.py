from django.shortcuts import render, redirect


def index(request):
    logged = request.session.get('logged')
    if not logged:
        return redirect('/')
    return render(request, 'administrator/index.html')


def logout(request):
    request.session.flush()
    return redirect('/')
