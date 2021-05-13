from django.shortcuts import render, redirect
from django.db.models import Q
import cms.auth.auth as auth
from cms.auth.models import Admin, Course, Student, Teacher


def admin_required(handler):
    def wrapper(request):
        if not auth.is_admin(request):
            return redirect('auth_index')
        return handler(request)

    return wrapper


@admin_required
def index(request):
    userid = auth.get_userid(request)
    username = Admin.get_by_id(userid).name
    context = {
        'teacher_count': Teacher.objects.count(),
        'course_count': Course.objects.count(),
        'student_count': Student.objects.count(),
        'username': username,
    }
    return render(request, 'admin/index.html', context)


@admin_required
def settings(request):
    userid = auth.get_userid(request)
    username = Admin.get_by_id(userid).name
    context = {
        'username': username,
    }
    if request.method == 'POST':
        # POST data
        password = request.POST.get('password')
        new_password1 = request.POST.get('newPassword1')
        new_password2 = request.POST.get('newPassword2')
        userid = auth.get_userid(request)
        if new_password1 != new_password2:
            context['message'] = "两次密码不一致！"
        else:
            user = Admin.get_by_id(userid)
            if user is None or auth.make_token(password) != user.token:
                context['message'] = "当前密码错误！"
            else:
                user.token = auth.make_token(new_password1)
                user.save()
                context['message'] = "修改成功！"
    return render(request, 'admin/settings.html', context)


@admin_required
def logout(request):
    auth.logout(request)
    return redirect('auth_index')


@admin_required
def admin_course(request):
    userid = auth.get_userid(request)
    username = Admin.get_by_id(userid).name
    context = {
        'username': username,
    }
    keyword = request.GET.get('keyword', '').strip()
    order_by = request.GET.get('orderBy', '').strip()
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            course_id = request.POST.get('courseId')
            course_name = request.POST.get('courseName')
            teacher_id = request.POST.get('courseTeacher')
            description = request.POST.get('courseDescription')
            if len(description) == 0:
                description = None
            if len(teacher_id) == 0:
                teacher = None
            else:
                teacher = Teacher.get_by_id(teacher_id)
            try:
                Course.objects.create(
                    id=course_id,
                    name=course_name,
                    teacher=teacher,
                    description=description,
                )
                context['message'] = '添加成功！'
            except Exception as e:
                context['message'] = '添加失败！' + e.__str__()
        elif action == 'delete':
            course_id = request.POST.get('courseId')
            if course_id:
                course = Course.get_by_id(course_id)
                if course:
                    course.delete()
                context['message'] = '已删除！'
        elif action == 'edit':
            course_id = request.POST.get('courseId')
            course_name = request.POST.get('courseName')
            teacher_id = request.POST.get('courseTeacher')
            description = request.POST.get('courseDescription')
            if len(teacher_id) == 0:
                teacher = None
            else:
                teacher = Teacher.get_by_id(teacher_id)
            if len(description) == 0:
                description = None
            course = Course.get_by_id(course_id)
            if course:
                course.name = course_name
                course.teacher = teacher
                course.description = description
                course.save()
            context['message'] = '已修改！'

    if len(keyword) == 0:
        course_list = Course.objects.all()
    else:
        course_list = Course.objects.filter(
            Q(id__contains=keyword) | Q(name__contains=keyword) | Q(teacher__name__contains=keyword)
        )
    if order_by in ('id', 'name'):
        course_list = course_list.order_by(order_by)
    context['course_list'] = course_list
    context['teacher_list'] = Teacher.objects.all()
    return render(request, 'admin/course.html', context)


@admin_required
def admin_student(request):
    userid = auth.get_userid(request)
    username = Admin.get_by_id(userid).name
    context = {
        'username': username,
    }
    keyword = request.GET.get('keyword', '').strip()
    order_by = request.GET.get('orderBy', '').strip()
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            _id = request.POST.get('studentId')
            _name = request.POST.get('studentName')
            try:
                Student.objects.create(
                    id=_id,
                    name=_name,
                    token=auth.make_token(_id),
                )
                context['message'] = '添加成功！'
            except Exception as e:
                context['message'] = '添加失败！' + e.__str__()
        elif action == 'delete':
            _id = request.POST.get('studentId')
            if _id:
                student = Student.get_by_id(_id)
                if student:
                    student.delete()
                context['message'] = '已删除！'
        elif action == 'edit':
            _id = request.POST.get('studentId')
            _name = request.POST.get('studentName')
            _password = request.POST.get('studentPassword')
            student = Student.get_by_id(_id)
            student.name = _name
            if _password and len(_password) > 0:
                student.token = auth.make_token(_password)
            student.save()
            context['message'] = '已修改！'
    if len(keyword) == 0:
        student_list = Student.objects.all()
    else:
        student_list = Student.objects.filter(
            Q(id__contains=keyword) | Q(name__contains=keyword)
        )
    if order_by in ('id', 'name'):
        student_list = student_list.order_by(order_by)
    context['student_list'] = student_list
    return render(request, 'admin/student.html', context)


@admin_required
def admin_teacher(request):
    if not auth.is_admin(request):
        return redirect('auth_index')
    userid = auth.get_userid(request)
    username = Admin.get_by_id(userid).name
    context = {
        'username': username,
    }
    keyword = request.GET.get('keyword', '').strip()
    order_by = request.GET.get('orderBy', '').strip()
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            _id = request.POST.get('teacherId')
            _name = request.POST.get('teacherName')
            try:
                Teacher.objects.create(
                    id=_id,
                    name=_name,
                    token=auth.make_token(_id),
                )
                context['message'] = '添加成功！'
            except Exception as e:
                context['message'] = '添加失败！' + e.__str__()
        elif action == 'delete':
            _id = request.POST.get('teacherId')
            if _id:
                teacher = Teacher.get_by_id(_id)
                if teacher:
                    teacher.delete()
                context['message'] = '已删除！'
        elif action == 'edit':
            _id = request.POST.get('teacherId')
            _name = request.POST.get('teacherName')
            _password = request.POST.get('teacherPassword')
            teacher = Teacher.get_by_id(_id)
            teacher.name = _name
            if _password and len(_password) > 0:
                teacher.token = auth.make_token(_password)
            teacher.save()
            context['message'] = '已修改！'
    if len(keyword) == 0:
        teacher_list = Teacher.objects.all()
    else:
        teacher_list = Teacher.objects.filter(
            Q(id__contains=keyword) | Q(name__contains=keyword)
        )
    if order_by in ('id', 'name'):
        teacher_list = teacher_list.order_by(order_by)
    context['teacher_list'] = teacher_list
    return render(request, 'admin/teacher.html', context)
