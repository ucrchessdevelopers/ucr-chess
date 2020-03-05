import os

from django.db import models

from django.db.models.signals import post_delete
from django.dispatch import receiver

from db_file_storage.model_utils import delete_file, delete_file_if_needed

from django.utils.html import mark_safe
from upload_validator import FileTypeValidator

from datetime import datetime
from django.core import validators

from django.core.files.storage import default_storage as storage


class Player(models.Model):
    firstname = models.CharField(max_length = 20, help_text="FULL FIRST NAME, this is how we pair this entry with previous entries")
    lastname = models.CharField(max_length = 30, help_text="Same as previous field; please make sure entry is correct. These are integral to how we match players to their history")
    rating = models.IntegerField(default=3000)
    rating_diff = models.IntegerField(default=0, blank=True)
    last_active = models.DateField(auto_now=False, auto_now_add=False, blank=True, default=datetime.now())
    wins = models.IntegerField(default=0, blank=True)
    losses = models.IntegerField(default=0, blank=True)
    draws = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return '{}'.format(self.firstname) + ' {}'.format(self.lastname) + ': {}'.format(self.rating)

class VegaChessEntry(models.Model):
    tournament_date = models.DateField(auto_now=False, auto_now_add=False)
    entry = models.FileField(upload_to='hello.PictureWrapper/bytes/filename/mimetype')
    #     validators=[FileTypeValidator(allowed_types=['text/plain'])]
    # )

    def save(self, *args, **kwargs):
        delete_file_if_needed(self, 'entry')
        super(VegaChessEntry, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(VegaChessEntry, self).delete(*args, **kwargs)
        delete_file(self, 'entry')

class PictureWrapper(models.Model):
    bytes = models.BinaryField()
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=50)

class Officer(models.Model):
    order = models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20)])
    picture = models.ImageField(upload_to='hello.PictureWrapper/bytes/filename/mimetype', height_field=None, width_field=None, max_length=100, blank=False)
    name = models.CharField(max_length = 40)
    position = models.CharField(max_length = 40)
    email = models.EmailField(max_length = 40)
    about = models.CharField(max_length = 200, help_text="Max 200 Characters")

    def save(self, *args, **kwargs):
        delete_file_if_needed(self, 'picture')
        super(Officer, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(Officer, self).delete(*args, **kwargs)
        delete_file(self, 'picture')

    def picture_tag(self):
        return mark_safe('<img src="../../..%s" height="200em" />' % (self.picture.url))
    picture_tag.short_description = 'Picture Preview'

    def picture_edit_tag(self):
        return mark_safe('<img src="../../../../..%s" height="200em" />' % (self.picture.url))
    picture_edit_tag.short_description = 'Picture Preview'

    def __str__(self):
        return '{}'.format(self.name) + ': {}'.format(self.position)

class CarouselImage(models.Model):
    order = models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20)])
    description = models.CharField(max_length = 50)
    picture = models.ImageField(upload_to='hello.PictureWrapper/bytes/filename/mimetype', height_field=None, width_field=None, max_length=100, blank=False)

    def save(self, *args, **kwargs):
        delete_file_if_needed(self, 'picture')
        super(CarouselImage, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(CarouselImage, self).delete(*args, **kwargs)
        delete_file(self, 'picture')

    def picture_tag(self):
        return mark_safe('<img src="../../..%s" height="200em" />' % (self.picture.url))
    picture_tag.short_description = 'Picture Preview'

    def picture_edit_tag(self):
        return mark_safe('<img src="../../../../..%s" height="200em" />' % (self.picture.url))
    picture_edit_tag.short_description = 'Picture Preview'

    # def __str__(self):
    #     return '{}'.format(self.picture.name)

class LinkButton(models.Model):
    order = models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20)])
    title = models.CharField(max_length = 20, help_text="Max 20 Characters")
    url = models.URLField(max_length = 200, help_text="Max 200 Characters")

    def __str__(self):
        return '{}'.format(self.title)

#Garbage Collection
@receiver(post_delete, sender=Officer)
@receiver(post_delete, sender=CarouselImage)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    instance.picture.delete(False)

@receiver(models.signals.pre_save, sender=Officer)
@receiver(models.signals.pre_save, sender=CarouselImage)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).picture
    except sender.DoesNotExist:
        return False

    new_file = instance.picture
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

import csv
from io import TextIOWrapper

@receiver(models.signals.post_save, sender=VegaChessEntry)
def parse_vega_chess_entry(sender, instance, **kwargs):
    csv_file = TextIOWrapper(instance.entry)
    csv_reader = csv.reader(csv_file, delimiter=',')
    line = 0
    for row in csv_reader:
        print(f'{row[0]} | {row[1]} | {row[2]}.', flush=True)
        line += abs(-1 - line)


        #sanat does this part


    fn = "test4"
    ln = "test4"
    try:
        SelectedPlayer = Player.objects.get(firstname=fn, lastname=ln)
        SelectedPlayer.rating = SelectedPlayer.rating + 500
        SelectedPlayer.save()

    except Player.DoesNotExist:
        SelectedPlayer = Player.objects.create(firstname=fn, lastname=ln)

    instance.delete()

class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)
