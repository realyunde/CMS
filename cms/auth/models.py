from django.db import models


class Student(models.Model):
    id = models.CharField(
        null=False,
        blank=False,
        max_length=12,
        primary_key=True,
    )
    name = models.CharField(
        null=False,
        blank=False,
        max_length=32,
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
        max_length=8,
        primary_key=True,
    )
    name = models.CharField(
        null=False,
        blank=False,
        max_length=32,
    )
    token = models.CharField(max_length=64)

    @classmethod
    def get_by_id(cls, _id):
        try:
            return cls.objects.get(id=_id)
        except cls.DoesNotExist:
            return None


class Course(models.Model):
    id = models.CharField(
        null=False,
        blank=False,
        max_length=32,
        primary_key=True,
    )
    name = models.CharField(
        null=False,
        blank=False,
        max_length=255,
    )
    teacher = models.ForeignKey(
        Teacher,
        null=True,
        on_delete=models.SET_NULL,
    )

    @classmethod
    def get_by_id(cls, _id):
        try:
            return cls.objects.get(id=_id)
        except cls.DoesNotExist:
            return None


class Admin(models.Model):
    name = models.CharField(
        null=False,
        blank=False,
        unique=True,
        max_length=32,
    )
    token = models.CharField(max_length=64)

    @classmethod
    def get_by_id(cls, _id):
        try:
            return cls.objects.get(id=_id)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_by_name(cls, name):
        try:
            return cls.objects.get(name=name)
        except cls.DoesNotExist:
            return None


class Selection(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
    )
    score = models.IntegerField(default=None)
    comment = models.TextField(default=None)

    class Meta:
        unique_together = ('student', 'course')
