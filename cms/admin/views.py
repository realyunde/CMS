from django.shortcuts import render, redirect
from ..auth.models import School


def index(request):
    user = request.session.get('user')
    if not user:
        return redirect('/')
    return render(request, 'admin/index.html')


def settings(request):
    if request.method == 'GET':
        return render(request, 'admin/settings.html')
    elif request.method == 'POST':
        return render(request, 'admin/settings.html')


def logout(request):
    request.session.clear()
    request.session.flush()
    return redirect('/')


def school(request):
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
            schools = request.POST.getlist('schoolIdList')
            print(schools)
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
