from django.shortcuts import render, redirect
import cms.auth.auth as auth
from cms.auth.models import Admin, Course, Student


def index(request):
    if not auth.is_admin(request):
        return redirect('auth_index')
    return render(request, 'admin/index.html')


def settings(request):
    if not auth.is_admin(request):
        return redirect('auth_index')
    context = {}
    if request.method == 'POST':
        account = request.session.get('user')['account']
        password = request.POST.get('password')
        new_password1 = request.POST.get('newPassword1')
        new_password2 = request.POST.get('newPassword2')
        if new_password1 != new_password2:
            context['notification'] = "两次密码不一致！"
        else:
            user = Admin.get_by_name(account)
            if user is None or user.password != password:
                context['notification'] = "当前密码错误！"
            else:
                user.password = new_password1
                user.save()
                context['notification'] = "修改成功！"
    return render(request, 'admin/settings.html', context)


def logout(request):
    if not auth.is_admin(request):
        return redirect('auth_index')
    request.session.clear()
    request.session.flush()
    return redirect('/')


def admin_course(request):
    context = {}
    if not auth.is_admin(request):
        return redirect('auth_index')
    keyword = request.GET.get('keyword', '').strip()
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            course_id = request.POST.get('courseId')
            course_name = request.POST.get('courseName')
            try:
                item = Course(
                    id=course_id,
                    name=course_name,
                )
                item.save()
                context['information'] = '添加成功！'
            except:
                context['information'] = '添加失败！'
        elif action == 'delete':
            course_id = request.POST.get('courseId')
            if course_id:
                course = Course.get_by_id(course_id)
                if course:
                    course.delete()
                context['information'] = '已删除！'
        elif action == 'edit':
            course_id = request.POST.get('courseId')
            course_name = request.POST.get('courseName')
            course = Course.get_by_id(course_id)
            course.name = course_name
            course.save()
            context['information'] = '已修改！'

    if len(keyword) == 0:
        course_list = Course.objects.all()
    else:
        course_list = Course.objects.filter(name__contains=keyword)
    context['course_list'] = course_list
    return render(request, 'admin/course.html', context)


def admin_student(request):
    context = {}
    if not auth.is_admin(request):
        return redirect('auth_index')
    keyword = request.GET.get('keyword', '').strip()
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            _id = request.POST.get('studentId')
            _name = request.POST.get('studentName')
            try:
                item = Student(
                    id=_id,
                    name=_name,
                    token=auth.make_token(_id),
                )
                item.save()
                context['information'] = '添加成功！'
            except:
                context['information'] = '添加失败！'
        elif action == 'delete':
            _id = request.POST.get('studentId')
            if _id:
                student = Student.get_by_id(_id)
                if student:
                    student.delete()
                context['information'] = '已删除！'
        elif action == 'edit':
            _id = request.POST.get('studentId')
            _name = request.POST.get('studentName')
            student = Student.get_by_id(_id)
            student.name = _name
            student.save()
            context['information'] = '已修改！'
    if len(keyword) == 0:
        student_list = Student.objects.all()
    else:
        student_list = Student.objects.filter(name__contains=keyword)
    context['student_list'] = student_list
    return render(request, 'admin/student.html', context)
