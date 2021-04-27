from django.shortcuts import render, redirect
from ..auth.models import School, Administrator, Course, Student
from ..auth import make_token


def has_permission(request):
    user = request.session.get('user')
    if not user or user['role'] != 'admin':
        return False
    return True


def index(request):
    if not has_permission(request):
        return redirect('/')
    return render(request, 'admin/index.html')


def settings(request):
    if not has_permission(request):
        return redirect('/')
    context = {}
    if request.method == 'POST':
        account = request.session.get('user')['account']
        password = request.POST.get('password')
        new_password1 = request.POST.get('newPassword1')
        new_password2 = request.POST.get('newPassword2')
        if new_password1 != new_password2:
            context['notification'] = "两次密码不一致！"
        else:
            user = Administrator.get_by_name(account)
            if user is None or user.password != password:
                context['notification'] = "当前密码错误！"
            else:
                user.password = new_password1
                user.save()
                context['notification'] = "修改成功！"
    return render(request, 'admin/settings.html', context)


def logout(request):
    if not has_permission(request):
        return redirect('/')
    request.session.clear()
    request.session.flush()
    return redirect('/')


def admin_school(request):
    if not has_permission(request):
        return redirect('/')
    keyword = request.GET.get('keyword', '').strip()
    page = request.GET.get('page', 1)
    try:
        page = int(page)
        if page < 0:
            page = 1
    except ValueError:
        page = 1
    context = {}
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            school_id = request.POST.get('schoolId', '')
            school_name = request.POST.get('schoolName', '')
            if len(school_id) and len(school_name):
                item = School(id=school_id, name=school_name)
                item.save()
                context['information'] = '添加成功！'
            else:
                context['information'] = '添加失败：学院代码或学院名称不符合要求'
        elif action == 'delete':
            school_id = request.POST.get('schoolId')
            school = School.get_by_id(school_id)
            if school:
                school.delete()
            context['information'] = '已删除！'
        elif action == 'edit':
            _id = request.POST.get('schoolId')
            _name = request.POST.get('schoolName')
            school = School.get_by_id(_id)
            school.name = _name
            school.save()
            context['information'] = '已修改！'
    # get school list
    offset = (page - 1) * 10
    if len(keyword) == 0:
        count = int(School.objects.count() / 10) + 1
        school_list = School.objects.all()[offset:offset + 10]
    else:
        count = int(School.objects.filter(name__contains=f'{keyword}').count() / 10) + 1
        school_list = School.objects.filter(name__contains=f'{keyword}')[offset:offset + 10]
    context['school_list'] = school_list
    context['page_now'] = page - 1
    context['page_prev'] = count if page <= 1 else (page - 1)
    context['page_next'] = 1 if page >= count else (page + 1)
    context['page_count'] = range(count)
    context['page_keyword'] = keyword
    return render(request, 'admin/school.html', context)


def admin_course(request):
    context = {}
    if not has_permission(request):
        return redirect('/')
    keyword = request.GET.get('keyword', '').strip()
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            course_id = request.POST.get('courseId')
            course_name = request.POST.get('courseName')
            course_school_id = request.POST.get('courseSchoolId')
            try:
                item = Course(
                    id=course_id,
                    name=course_name,
                    school=School.get_by_id(course_school_id),
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
            school_id = request.POST.get('courseSchoolId')
            course = Course.get_by_id(course_id)
            course.name = course_name
            course.school = School.get_by_id(school_id)
            course.save()
            context['information'] = '已修改！'

    if len(keyword) == 0:
        course_list = Course.objects.all()
    else:
        course_list = Course.objects.filter(name__contains=keyword)
    context['course_list'] = course_list
    context['school_list'] = School.objects.all()
    return render(request, 'admin/course.html', context)


def admin_student(request):
    context = {}
    if not has_permission(request):
        return redirect('/')
    keyword = request.GET.get('keyword', '').strip()
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            _id = request.POST.get('studentId')
            _name = request.POST.get('studentName')
            _school_id = request.POST.get('studentSchoolId')
            try:
                item = Student(
                    id=_id,
                    name=_name,
                    token=make_token(_id),
                    school=School.get_by_id(_school_id),
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
            school_id = request.POST.get('studentSchoolId')
            student = Student.get_by_id(_id)
            student.name = _name
            student.school = School.get_by_id(school_id)
            student.save()
            context['information'] = '已修改！'
    if len(keyword) == 0:
        student_list = Student.objects.all()
    else:
        student_list = Student.objects.filter(name__contains=keyword)
    context['student_list'] = student_list
    context['school_list'] = School.objects.all()
    return render(request, 'admin/student.html', context)
