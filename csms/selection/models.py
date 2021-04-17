from django.db import models


# 学院
class School(models.Model):
    id = models.CharField(max_length=32, primary_key=True, null=False)
    name = models.CharField(max_length=256, null=False)


# 专业
class Speciality(models.Model):
    id = models.CharField(max_length=32, primary_key=True, null=False)
    name = models.CharField(max_length=256, unique=True, null=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE)


# 教师
class Teacher(models.Model):
    id = models.CharField(max_length=32, primary_key=True, null=False)
    name = models.CharField(max_length=32, null=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE)


# 课程
class Course(models.Model):
    id = models.CharField(max_length=32, primary_key=True, null=False)
    name = models.CharField(max_length=256, unique=True, null=False)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)


# 管理员
class Admin(models.Model):
    id = models.CharField(max_length=32, primary_key=True, null=False)
    name = models.CharField(max_length=32, unique=True, null=False)
    password = models.CharField(max_length=32, null=False)

    @classmethod
    def get_object_by_name(cls, name):
        try:
            return cls.objects.get(name=name)
        except cls.DoesNotExist:
            return None


# 学生
class Student(models.Model):
    id = models.CharField(max_length=32, primary_key=True, null=False)
    name = models.CharField(max_length=32, null=False)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)


# 选课
class Selection(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        unique_together = ('student_id', 'course_id')
