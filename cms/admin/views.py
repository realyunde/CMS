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
    page = request.GET.get('keyword', 0)
    try:
        page = int(page) - 1
        if page < 0:
            page = 0
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
    # get all schools
    context['school_list'] = School.objects.filter(name__contains=f'{keyword}')
    return render(request, 'admin/school.html', context)
