from django.shortcuts import render, redirect
from django.db.models import Q
import cms.auth.auth as auth
from cms.auth.models import Course, Selection, Student


def student_required(handler):
    def wrapper(request):
        if not auth.is_student(request):
            return redirect('auth_index')
        return handler(request)

    return wrapper


@student_required
def index(request):
    userid = auth.get_userid(request)
    username = Student.get_by_id(userid).name
    context = {
        'username': username,
    }
    list_count = Selection.objects.filter(
        student_id=userid,
    ).count()
    course_count = Course.objects.exclude(
        selection__student__id=userid,
    ).count()
    context['list_count'] = list_count
    context['course_count'] = course_count
    return render(request, 'student/index.html', context)


@student_required
def settings(request):
    userid = auth.get_userid(request)
    user = Student.get_by_id(userid)
    context = {
        'username': user.name,
    }
    if request.method == 'POST':
        password = request.POST.get('password')
        new_password1 = request.POST.get('newPassword1')
        new_password2 = request.POST.get('newPassword2')
        if new_password1 != new_password2:
            context['information'] = "两次密码不一致！"
        else:
            if auth.make_token(password) != user.token:
                context['information'] = "当前密码错误！"
            else:
                user.token = auth.make_token(new_password1)
                user.save()
                context['information'] = "修改成功！"
    return render(request, 'student/settings.html', context)


@student_required
def select(request):
    userid = auth.get_userid(request)
    username = Student.get_by_id(userid).name
    context = {
        'username': username,
    }
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'select':
            course_id = request.POST.get('courseId')
            try:
                selection = Selection.objects.create(
                    course_id=course_id,
                    student_id=userid,
                )
            except Exception as e:
                context['information'] = '选课失败！' + e.__str__()
            else:
                context['information'] = '选课成功！' + Course.get_by_id(course_id).name
    keyword = request.GET.get('keyword', '').strip()
    course_list = Course.objects.exclude(
        id__in=Selection.objects.filter(student_id=userid).values('course_id'),
    )
    if len(keyword) > 0:
        course_list = course_list.filter(
            Q(id__contains=keyword) | Q(name__contains=keyword)
        )
    context['course_list'] = course_list
    return render(request, 'student/select.html', context)


@student_required
def list_course(request):
    userid = auth.get_userid(request)
    username = Student.get_by_id(userid).name
    context = {
        'username': username,
    }
    keyword = request.GET.get('keyword', '').strip()
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'withdraw':
            course_id = request.POST.get('courseId')
            selection = Selection.objects.get(
                student_id=userid,
                course_id=course_id,
            )
            selection.delete()
            context['information'] = '已退选！' + Course.get_by_id(course_id).name
        elif action == 'comment':
            course_id = request.POST.get('courseId')
            comment = request.POST.get('courseComment')
            selection = Selection.objects.get(
                student_id=userid,
                course_id=course_id,
            )
            selection.comment = comment
            selection.save()
            context['information'] = '评价已更新！'
    if len(keyword) > 0:
        course_list = Course.objects.raw(
            "SELECT * "
            "FROM auth_course "
            "JOIN auth_selection "
            "ON auth_course.id=auth_selection.course_id AND auth_selection.student_id='{0}' "
            "WHERE auth_course.id LIKE '%{1}%' OR auth_course.name LIKE '%{1}%'".format(userid, keyword)
        )
    else:
        course_list = Course.objects.raw(
            "SELECT * "
            "FROM auth_course "
            "JOIN auth_selection "
            "ON auth_course.id=auth_selection.course_id AND auth_selection.student_id='{}'".format(userid)
        )
    context['course_list'] = course_list
    return render(request, 'student/list.html', context)


@student_required
def logout(request):
    auth.logout(request)
    return redirect('auth_index')
