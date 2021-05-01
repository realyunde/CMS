from django.shortcuts import render, redirect
from django.db.models import Q
import cms.auth.auth as auth
from cms.auth.models import Teacher, Course, Selection


def index(request):
    if not auth.is_teacher(request):
        return redirect('auth_index')
    context = {}
    userid = auth.get_userid(request)
    context['username'] = Teacher.get_by_id(userid).name
    course_list = Course.objects.filter(
        teacher_id=userid,
    )
    course_count = course_list.count()
    score_count = 0
    for item in course_list:
        n = Selection.objects.filter(
            course_id=item.id,
        ).count()
        score_count += n
    context['course_count'] = course_count
    context['score_count'] = score_count
    return render(request, 'teacher/index.html', context)


def settings(request):
    if not auth.is_teacher(request):
        return redirect('auth_index')
    context = {}
    userid = auth.get_userid(request)
    context['username'] = Teacher.get_by_id(userid).name
    if request.method == 'POST':
        password = request.POST.get('password')
        new_password1 = request.POST.get('newPassword1')
        new_password2 = request.POST.get('newPassword2')
        if new_password1 != new_password2:
            context['information'] = '两次密码不一致！'
        else:
            user = Teacher.get_by_id(userid)
            if auth.make_token(password) != user.token:
                context['information'] = '原密码错误！'
            else:
                user.token = auth.make_token(new_password1)
                user.save()
                context['information'] = '修改成功！'
    return render(request, 'teacher/settings.html', context)


def teacher_course(request):
    if not auth.is_teacher(request):
        return redirect('auth_index')
    context = {}
    userid = auth.get_userid(request)
    context['username'] = Teacher.get_by_id(userid).name
    keyword = request.GET.get('keyword', '').strip()
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'edit':
            course_id = request.POST.get('courseId')
            description = request.POST.get('courseDescription')
            course = Course.get_by_id(course_id)
            course.description = description
            course.save()
            context['information'] = '修改成功！'
    course_list = Course.objects.filter(
        teacher_id=userid,
    )
    if len(keyword) != 0:
        course_list = course_list.filter(
            Q(id__contains=keyword) | Q(name__contains=keyword)
        )
    context['course_list'] = course_list
    return render(request, 'teacher/course.html', context)


def teacher_score(request):
    if not auth.is_teacher(request):
        return redirect('auth_index')
    context = {}
    userid = auth.get_userid(request)
    context['username'] = Teacher.get_by_id(userid).name
    keyword = request.GET.get('keyword', '').strip()
    return render(request, 'teacher/score.html', context)


def logout(request):
    auth.logout(request)
    return redirect('auth_index')
