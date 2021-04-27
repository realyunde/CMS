from django.shortcuts import render, redirect
from ..auth.models import School, Administrator


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
        if action == 'delete':
            school_id = request.POST.get('schoolId')
            school = School.get_by_id(school_id)
            if school:
                school.delete()
            context['information'] = '已删除！'
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
