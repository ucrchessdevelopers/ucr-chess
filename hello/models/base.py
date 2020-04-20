import os
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# from django.core import validators
# from django.core.files.storage import default_storage as storage

class PictureWrapper(models.Model):
    bytes = models.BinaryField()
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=50)

# import sys
# sys.path.append('submodels/')
# from submodels/CarouselImage.py import *

# sys.path.append('../')
class FrontPageText(models.Model):
    text = models.CharField(max_length = 2000, help_text="Max 2000 Characters")

    def clean(self):
        if FrontPageText.objects.count() > 0:
            raise ValidationError(_('There is only one instance of front page text allowed, please edit the existing instance'))

    class Meta:
        verbose_name_plural = "Front Page Text"

class LinkButton(models.Model):
    order = models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20)])
    title = models.CharField(max_length = 20, help_text="Max 20 Characters")
    url = models.URLField(max_length = 200, help_text="Max 200 Characters")

    def clean(self):
        if LinkButton.objects.count() > 3:
            raise ValidationError(_('Maximum of 4 buttons allowed. Please edit or delete an existing button'))

    def __str__(self):
        return '{}'.format(self.title)

class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)
