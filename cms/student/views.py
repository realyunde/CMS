from django.shortcuts import render, redirect
from django.db.models import Q
import cms.auth.auth as auth
from cms.auth.models import Course, Selection


def index(request):
    if not auth.is_student(request):
        return redirect('auth_index')
    return render(request, 'student/index.html')


def settings(request):
    if not auth.is_student(request):
        return redirect('auth_index')
    return render(request, 'student/settings.html')


def select(request):
    if not auth.is_student(request):
        return redirect('auth_index')
    context = {}
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'select':
            course_id = request.POST.get('courseId')
            userid = auth.get_userid(request)
            selection = Selection(
                course_id=course_id,
                student_id=userid,
            )
            selection.save()
            context['information'] = '选课成功！'
    keyword = request.GET.get('keyword', '').strip()
    userid = auth.get_userid(request)
    # selected_course = Selection.objects.filter(student_id=userid)
    course_list = Course.objects.exclude(
        id__in=Selection.objects.filter(student_id=userid).values_list('course_id', flat=True),
    )
    if len(keyword) > 0:
        course_list = course_list.filter(
            Q(id__contains=keyword) | Q(name__contains=keyword)
        )
    context['course_list'] = course_list
    return render(request, 'student/select.html', context)


def list_course(request):
    if not auth.is_student(request):
        return redirect('auth_index')
    context = {}
    keyword = request.GET.get('keyword', '').strip()
    userid = auth.get_userid(request)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'withdraw':
            course_id = request.POST.get('courseId')
            selection = Selection.objects.get(
                student_id=userid,
                course_id=course_id,
            )
            selection.delete()
            context['information'] = '已退选！'
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

    course_list = Course.objects.filter(
        selection__student__id=userid,
    )
    if len(keyword) > 0:
        course_list = course_list.filter(
            Q(id__contains=keyword) | Q(name__contains=keyword)
        )
    context['course_list'] = course_list
    return render(request, 'student/list.html', context)


def logout(request):
    auth.logout(request)
    return redirect('auth_index')
