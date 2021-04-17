from django.db import models


class School(models.Model):
    id = models.CharField(max_length=32, primary_key=True, null=False)
    name = models.CharField(max_length=256, null=False)


class Speciality(models.Model):
    id = models.CharField(max_length=32, primary_key=True, null=False)
    name = models.CharField(max_length=256, unique=True, null=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE)


class Teacher(models.Model):
    id = models.CharField(max_length=32, primary_key=True, null=False)
    name = models.CharField(max_length=32, null=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE)


class Course(models.Model):
    id = models.CharField(max_length=32, primary_key=True, null=False)
    name = models.CharField(max_length=256, unique=True, null=False)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)


class Student(models.Model):
    id = models.CharField(max_length=32, primary_key=True, null=False)
    name = models.CharField(max_length=32, null=False)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)


class Selection(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    grade = models.IntegerField()

    class Meta:
        unique_together = ('student_id', 'course_id')
