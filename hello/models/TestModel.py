from django.db import models

class TestModel(models.Model):
    test = models.IntegerField(default=0)
