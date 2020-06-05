from django.db import models

class TestModel(models.Model):
    test = models.IntegerField(default=0)
    test2 = models.IntegerField(default = 33)
