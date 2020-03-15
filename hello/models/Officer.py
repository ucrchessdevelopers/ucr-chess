from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.html import mark_safe
from db_file_storage.model_utils import delete_file, delete_file_if_needed


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

#Garbage Collection
@receiver(post_delete, sender=Officer)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    instance.picture.delete(False)

@receiver(models.signals.pre_save, sender=Officer)
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
