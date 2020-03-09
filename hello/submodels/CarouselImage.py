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
