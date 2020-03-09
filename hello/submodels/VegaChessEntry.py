class VegaChessEntry(models.Model):
    tournament_date = models.DateField(auto_now=False, auto_now_add=False)
    entry = models.FileField(upload_to='hello.PictureWrapper/bytes/filename/mimetype',
        validators=[
        FileTypeValidator(allowed_types=['text/plain']),
            # validate_vega_chess_entry
        ]
    )

    def save(self, *args, **kwargs):
        delete_file_if_needed(self, 'entry')
        super(VegaChessEntry, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(VegaChessEntry, self).delete(*args, **kwargs)
        delete_file(self, 'entry')
