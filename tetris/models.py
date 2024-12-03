from django.db import models


class Score(models.Model):
    name = models.CharField(max_length=200)
    score = models.IntegerField()
