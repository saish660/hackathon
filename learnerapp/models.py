from django.contrib.auth.models import AbstractUser
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100)
    max_level = 0


class User(AbstractUser):
    courses = models.ManyToManyField(Course, related_name="student", default=None)
    avg_score = models.FloatField(default=0)
    quizzes_attempted = models.IntegerField(default=0)
    score1 = models.IntegerField(default=0)
    score2 = models.IntegerField(default=0)
    score3 = models.IntegerField(default=0)
    score4 = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    level_completed = models.IntegerField(default=1)
    badges_won = models.IntegerField(default=0)


