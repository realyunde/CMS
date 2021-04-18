from django.shortcuts import render, redirect
from .models import Student, Teacher, Administrator


def auth_error(request):
    context = {}
    context.setdefault('error', '不存在该用户或密码错误！')
    request.session.clear()
    request.session.flush()
    return render(request, 'auth/index.html', context)


def auth_student(request, account, password):
    user = Student.get_by_sno(account)
    if user is None or user.password != password:
        return auth_error(request)
    request.session['user'] = {
        'role': 'student',
        'account': account
    }
    return redirect('student_index')


def auth_teacher(request, account, password):
    user = Teacher.get_by_tno(account)
    if user is None or user.password != password:
        return auth_error(request)
    request.session['user'] = {
        'role': 'teacher',
        'account': account
    }
    return redirect('teacher_index')


def auth_admin(request, account, password):
    user = Administrator.get_by_ano(account)
    if user is None or user.password != password:
        return auth_error(request)
    request.session['user'] = {
        'role': 'admin',
        'account': account
    }
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
