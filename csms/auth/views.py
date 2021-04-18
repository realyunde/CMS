from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from .models import School, Speciality, Teacher, Course, Student, Selection, Admin


def index(request):
    context = {}
    if request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if not all((account, password, role)):
            context.setdefault('error', '不存在该用户或密码错误！')
            return render(request, 'auth/index.html', context)
        if role == 'student':
            pass
        elif role == 'teacher':
            pass
        elif role == 'admin':
            user = Admin.get_object_by_name(account)
            if user is None or user.password != password:
                context.setdefault('error', '不存在该用户或密码错误！')
                return render(request, 'auth/index.html', context)
            else:
                request.session['role'] = role
                request.session['account'] = account
                request.session['logged'] = True
                return redirect('/admin/')
        else:
            request.session.flush()
            context.setdefault('error', '不存在该用户或密码错误！')
            return render(request, 'auth/index.html', context)
    elif request.method == 'GET':
        if request.session.get('logged'):
            return redirect('/admin/')
    return render(request, 'auth/index.html', context)
