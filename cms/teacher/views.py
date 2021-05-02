from django.shortcuts import render, redirect
from django.db.models import Q
import cms.auth.auth as auth
from cms.auth.models import Teacher, Course, Selection


def teacher_required(handler):
    def wrapper(request):
        if not auth.is_teacher(request):
            return redirect('auth_index')
        return handler(request)

    return wrapper


@teacher_required
def index(request):
    context = {}
    userid = auth.get_userid(request)
    context['username'] = Teacher.get_by_id(userid).name
    course_list = Course.objects.filter(
        teacher_id=userid,
    )
    course_count = course_list.count()
    score_count = 0
    for item in course_list:
        selections = Selection.objects.filter(
            course_id=item.id,
        )
        for s in selections:
            if s.score is None:
                score_count += 1
    context['course_count'] = course_count
    context['score_count'] = score_count
    return render(request, 'teacher/index.html', context)


@teacher_required
def settings(request):
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


@teacher_required
def teacher_course(request):
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
    for item in course_list:
        count = Selection.objects.filter(
            course_id=item.id,
        ).count()
        item.student_count = count
    context['course_list'] = course_list
    return render(request, 'teacher/course.html', context)


@teacher_required
def teacher_score(request):
    context = {}
    userid = auth.get_userid(request)
    context['username'] = Teacher.get_by_id(userid).name
    keyword = request.GET.get('keyword', '').strip()
    if request.method == 'POST':
        print(request.POST)
        action = request.POST.get('action')
        if action == 'edit':
            course_id = request.POST.get('courseId')
            student_id = request.POST.get('studentId')
            score = request.POST.get('courseScore')
            item = Selection.objects.get(
                course_id=course_id,
                student_id=student_id,
            )
            item.score = score
            item.save()
            context['information'] = '修改成功！'
    sql = "SELECT auth_selection.id as id, auth_course.id as c_id, auth_course.name as c_name," \
          "auth_student.id as s_id, auth_student.name as s_name," \
          "auth_selection.score as score, auth_selection.comment as comment " \
          "FROM auth_course " \
          "JOIN auth_selection " \
          "JOIN auth_student " \
          "ON auth_course.id=auth_selection.course_id " \
          "AND auth_student.id=auth_selection.student_id " \
          "AND auth_course.teacher_id='{}'".format(userid)
    if len(keyword) != 0:
        sql += " WHERE auth_course.id LIKE '%{0}%'" \
               " OR auth_course.name LIKE '%{0}%'" \
               " OR auth_student.id LIKE '%{0}%'" \
               " OR auth_student.name LIKE '%{0}%'".format(keyword)
    course_list = Course.objects.raw(sql)
    context['course_list'] = course_list
    return render(request, 'teacher/score.html', context)


@teacher_required
def logout(request):
    auth.logout(request)
    return redirect('auth_index')
