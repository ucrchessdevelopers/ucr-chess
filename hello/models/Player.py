from django.db import models
from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Player(models.Model):
    firstname = models.CharField(max_length = 20, help_text="FULL FIRST NAME, this is how we pair this entry with previous entries")
    lastname = models.CharField(max_length = 30, help_text="Same as previous field; please make sure entry is correct. These are integral to how we match players to their history")
    rating = models.IntegerField(default=1500)
    rating_diff = models.IntegerField(default=0, blank=True)
    last_active = models.DateField(auto_now=False, auto_now_add=False, blank=True, default=datetime.now())
    wins = models.IntegerField(default=0, blank=True)
    losses = models.IntegerField(default=0, blank=True)
    draws = models.IntegerField(default=0, blank=True)

    def clean(self):
        self.firstname = self.firstname.lower()
        self.lastname = self.lastname.lower()
        try:
            testplayer = Player.objects.get(firstname=self.firstname, lastname=self.lastname)
            if testplayer != self:
                raise ValidationError(_('Name is identical to another player'))
        except Player.DoesNotExist:
            print()

    def __str__(self):
        return '{}'.format(self.firstname) + ' {}'.format(self.lastname) + ': {}'.format(self.rating)
