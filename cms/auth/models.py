from django.db import models


class School(models.Model):
    id = models.CharField(
        null=False,
        blank=False,
        max_length=32,
        primary_key=True,
    )
    name = models.CharField(
        null=False,
        max_length=255,
    )


class Major(models.Model):
    id = models.CharField(
        null=False,
        blank=False,
        max_length=32,
        primary_key=True,
    )
    name = models.CharField(
        null=False,
        max_length=255,
    )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
    )


class Course(models.Model):
    id = models.CharField(
        null=False,
        blank=False,
        max_length=32,
        primary_key=True,
    )
    name = models.CharField(max_length=255, null=False)
    speciality = models.ForeignKey(Major, on_delete=models.CASCADE)


class Student(models.Model):
    id = models.CharField(
        null=False,
        blank=False,
        max_length=32,
        primary_key=True,
    )
    name = models.CharField(
        null=False,
        blank=False,
        max_length=32,
    )
    major = models.ForeignKey(
        Major,
        on_delete=models.CASCADE,
    )
    token = models.CharField(max_length=64)

    @classmethod
    def get_by_id(cls, _id):
        try:
            return cls.objects.get(id=_id)
        except cls.DoesNotExist:
            return None


class Teacher(models.Model):
    id = models.CharField(
        null=False,
        blank=False,
        max_length=32,
        primary_key=True,
    )
    name = models.CharField(
        null=False,
        blank=False,
        max_length=32,
    )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
    )
    token = models.CharField(max_length=64)

    @classmethod
    def get_by_id(cls, _id):
        try:
            cls.objects.get(id=_id)
        except cls.DoesNotExist:
            return None


class Administrator(models.Model):
    name = models.CharField(
        null=False,
        blank=False,
        unique=True,
        max_length=32,
    )
    token = models.CharField(max_length=64)

    @classmethod
    def get_by_name(cls, name):
        try:
            return cls.objects.get(name=name)
        except cls.DoesNotExist:
            return None


class Selection(models.Model):
    course_id = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )
    student_id = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
    )
    score = models.IntegerField()

    class Meta:
        unique_together = ('student_id', 'course_id')
