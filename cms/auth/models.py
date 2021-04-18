from django.db import models


class School(models.Model):
    id = models.CharField(max_length=32, primary_key=True, null=False)
    name = models.CharField(max_length=256, null=False)


class Speciality(models.Model):
    id = models.CharField(max_length=32, primary_key=True, null=False)
    name = models.CharField(max_length=256, null=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE)


class Course(models.Model):
    cno = models.CharField(max_length=32, primary_key=True, null=False)
    name = models.CharField(max_length=256, null=False)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)


class Student(models.Model):
    sno = models.CharField(max_length=12, primary_key=True, null=False)
    name = models.CharField(max_length=32, null=False)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE, null=False)
    password = models.CharField(max_length=64)

    @classmethod
    def get_by_sno(cls, sno):
        try:
            return cls.objects.get(sno=sno)
        except cls.DoesNotExist:
            return None


class Teacher(models.Model):
    tno = models.CharField(max_length=32, primary_key=True, null=False)
    name = models.CharField(max_length=32, null=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    password = models.CharField(max_length=64)

    @classmethod
    def get_by_tno(cls, tno):
        try:
            cls.objects.get(tno=tno)
        except cls.DoesNotExist:
            return None


class Administrator(models.Model):
    ano = models.CharField(max_length=32, primary_key=True, null=False)
    name = models.CharField(max_length=32, null=False)
    password = models.CharField(max_length=64)

    @classmethod
    def get_by_ano(cls, ano):
        try:
            return cls.objects.get(ano=ano)
        except cls.DoesNotExist:
            return None


class Selection(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        unique_together = ('student_id', 'course_id')
