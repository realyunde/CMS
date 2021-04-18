from django.contrib import admin
from .models import School, Speciality, Teacher, Course, Student, Selection, Admin

admin.site.register(School)
admin.site.register(Speciality)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Selection)
admin.site.register(Admin)
