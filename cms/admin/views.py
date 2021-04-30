from django.shortcuts import render, redirect
from django.db.models import Q
import cms.auth.auth as auth
from cms.auth.models import Admin, Course, Student, Teacher


def index(request):
    if not auth.is_admin(request):
        return redirect('auth_index')
    return render(request, 'admin/index.html')


def settings(request):
    if not auth.is_admin(request):
        return redirect('auth_index')
    context = {}
    if request.method == 'POST':
        # POST data
        password = request.POST.get('password')
        new_password1 = request.POST.get('newPassword1')
        new_password2 = request.POST.get('newPassword2')
        userid = auth.get_userid(request)
        if new_password1 != new_password2:
            context['notification'] = "两次密码不一致！"
        else:
            user = Admin.get_by_id(userid)
            if user is None or auth.make_token(password) != user.token:
                context['notification'] = "当前密码错误！"
            else:
                user.token = auth.make_token(new_password1)
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
            teacher_id = request.POST.get('courseTeacher')
            if len(teacher_id) == 0:
                teacher = None
            else:
                teacher = Teacher.get_by_id(teacher_id)
            try:
                item = Course.objects.create(
                    id=course_id,
                    name=course_name,
                    teacher=teacher,
                )
                context['information'] = '添加成功！'
            except Exception as e:
                context['information'] = '添加失败！' + e.__str__()
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
            teacher_id = request.POST.get('courseTeacher')
            if len(teacher_id) == 0:
                teacher = None
            else:
                teacher = Teacher.get_by_id(teacher_id)
            course = Course.get_by_id(course_id)
            if course:
                course.name = course_name
                course.teacher = teacher
                course.save()
            context['information'] = '已修改！'

    if len(keyword) == 0:
        course_list = Course.objects.all()
    else:
        course_list = Course.objects.filter(
            Q(id__contains=keyword) | Q(name__contains=keyword)
        )
    context['course_list'] = course_list
    context['teacher_list'] = Teacher.objects.all()
    return render(request, 'admin/course.html', context)


def admin_student(request):
    if not auth.is_admin(request):
        return redirect('auth_index')
    context = {}
    keyword = request.GET.get('keyword', '').strip()
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            _id = request.POST.get('studentId')
            _name = request.POST.get('studentName')
            try:
                item = Student.objects.create(
                    id=_id,
                    name=_name,
                    token=auth.make_token(_id),
                )
                context['information'] = '添加成功！'
            except Exception as e:
                context['information'] = '添加失败！' + e.__str__()
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
            _password = request.POST.get('studentPassword')
            student = Student.get_by_id(_id)
            student.name = _name
            if _password and len(_password) > 0:
                student.token = auth.make_token(_password)
            student.save()
            context['information'] = '已修改！'
    if len(keyword) == 0:
        student_list = Student.objects.all()
    else:
        student_list = Student.objects.filter(
            Q(id__contains=keyword) | Q(name__contains=keyword)
        )
    context['student_list'] = student_list
    return render(request, 'admin/student.html', context)


def admin_teacher(request):
    if not auth.is_admin(request):
        return redirect('auth_index')
    context = {}
    keyword = request.GET.get('keyword', '').strip()
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            _id = request.POST.get('teacherId')
            _name = request.POST.get('teacherName')
            try:
                item = Teacher.objects.create(
                    id=_id,
                    name=_name,
                    token=auth.make_token(_id),
                )
                context['information'] = '添加成功！'
            except Exception as e:
                context['information'] = '添加失败！' + e.__str__()
        elif action == 'delete':
            _id = request.POST.get('teacherId')
            if _id:
                teacher = Teacher.get_by_id(_id)
                if teacher:
                    teacher.delete()
                context['information'] = '已删除！'
        elif action == 'edit':
            _id = request.POST.get('teacherId')
            _name = request.POST.get('teacherName')
            _password = request.POST.get('teacherPassword')
            teacher = Teacher.get_by_id(_id)
            teacher.name = _name
            if _password and len(_password) > 0:
                teacher.token = auth.make_token(_password)
            teacher.save()
            context['information'] = '已修改！'
    if len(keyword) == 0:
        teacher_list = Teacher.objects.all()
    else:
        teacher_list = Teacher.objects.filter(
            Q(id__contains=keyword) | Q(name__contains=keyword)
        )
    context['teacher_list'] = teacher_list
    return render(request, 'admin/teacher.html', context)
