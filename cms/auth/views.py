from django.shortcuts import render, redirect
from .models import Student, Teacher, Administrator
from . import login, make_token


def auth_error(request):
    context = {'error': '不存在该用户或密码错误！'}
    return render(request, 'auth/index.html', context)


def auth_student(request, account, password):
    token = make_token(password)
    user = Student.get_by_id(account)
    if user is None or user.token != token:
        return auth_error(request)
    login(request, 'student', account)
    return redirect('student_index')


def auth_teacher(request, account, password):
    user = Teacher.get_by_id(account)
    if user is None or user.password != password:
        return auth_error(request)
    login(request, 'teacher', account)
    return redirect('teacher_index')


def auth_admin(request, account, password):
    token = make_token(password)
    user = Administrator.get_by_name(account)
    if user is None:
        if account == 'root' and password == 'root':
            user = Administrator(name=account, token=token)
            user.save()
            login(request, 'admin', account)
            return redirect('admin_index')
        return auth_error(request)
    if token != user.token:
        return auth_error(request)
    login(request, 'admin', account)
    return redirect('admin_index')


def index(request):
    if request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')
        role = request.POST.get('role')
        if not all((account, password, role)):
            return auth_error(request)
        if role == 'student':
            return auth_student(request, account, password)
        elif role == 'teacher':
            return auth_teacher(request, account, password)
        elif role == 'admin':
            return auth_admin(request, account, password)
        else:
            return auth_error(request)
    elif request.method == 'GET':
        user = request.session.get('user')
        if user:
            if user['role'] == 'admin':
                return redirect('admin_index')
    return render(request, 'auth/index.html')
