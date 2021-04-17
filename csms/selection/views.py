from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .models import School, Speciality, Teacher, Course, Student, Selection, Admin


def index(request: HttpRequest):
    context = {}
    if request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if not all((account, password, role)):
            context.setdefault('error', '不存在该用户或密码错误！')
            return render(request, 'selection/index.html', context)
        if role == 'student':
            pass
        elif role == 'teacher':
            pass
        elif role == 'admin':
            admin = Admin.get_object_by_name(account)
            if admin is None or admin.password != password:
                context.setdefault('error', '不存在该用户或密码错误！')
                return render(request, 'selection/index.html', context)
            else:
                request.session['role'] = role
                request.session['account'] = account
                request.session['logged'] = True
                context.setdefault('error', str(vars(request.session)))
                return render(request, 'selection/index.html', context)
        else:
            context.setdefault('error', '不存在该用户或密码错误！')
            return render(request, 'selection/index.html', context)
    elif request.method == 'GET':
        if request.session['logged']:
            context.setdefault('error', '已经登录')
            return render(request, 'selection/index.html', context)
    return render(request, 'selection/index.html', context)
