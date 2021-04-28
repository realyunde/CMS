from django.shortcuts import render, redirect
from .models import Admin
from . import auth


def error(request):
    context = {'error': '不存在该用户或密码错误！'}
    return render(request, 'auth/index.html', context)


def check_student(request, userid, password):
    if not auth.auth_student(userid, password):
        return error(request)
    auth.login_student(request, userid)
    return redirect('student_index')


def check_teacher(request, userid, password):
    if not auth.auth_teacher(userid, password):
        return error(request)
    auth.login_teacher(request, userid)
    return redirect('teacher_index')


def check_admin(request, userid, password):
    if not auth.auth_admin(userid, password):
        return error(request)
    auth.login_admin(request, userid)
    return redirect('admin_index')


def index(request):
    if request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')
        role = request.POST.get('role')
        if not all((account, password, role)):
            return error(request)
        if role == 'student':
            return check_student(request, account, password)
        elif role == 'teacher':
            return check_teacher(request, account, password)
        elif role == 'admin':
            user = Admin.get_by_name(account)
            if user is None:
                if account == 'root' and password == 'root':
                    user = Admin(
                        name=account,
                        token=auth.make_token(password),
                    )
                    user.save()
                    auth.login_admin(request, user.id)
                    return redirect('admin_index')
                else:
                    return error(request)
            else:
                return check_admin(request, user.id, password)
        else:
            return error(request)
    elif request.method == 'GET':
        if auth.is_admin(request):
            return redirect('admin_index')
        elif auth.is_teacher(request):
            pass
        elif auth.is_student(request):
            return redirect('student_index')
    return render(request, 'auth/index.html')
