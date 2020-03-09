class Player(models.Model):
    firstname = models.CharField(max_length = 20, help_text="FULL FIRST NAME, this is how we pair this entry with previous entries")
    lastname = models.CharField(max_length = 30, help_text="Same as previous field; please make sure entry is correct. These are integral to how we match players to their history")
    rating = models.IntegerField(default=3000)
    rating_diff = models.IntegerField(default=0, blank=True)
    games_played = models.IntegerField(default=0, blank=True)
    last_active = models.DateField(auto_now=False, auto_now_add=False, blank=True, default=datetime.now())
    wins = models.IntegerField(default=0, blank=True)
    losses = models.IntegerField(default=0, blank=True)
    draws = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return '{}'.format(self.firstname) + ' {}'.format(self.lastname) + ': {}'.format(self.rating)
