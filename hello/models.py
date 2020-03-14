import os
import numpy as np
import sympy as sp

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
    rating = models.IntegerField(default=1500)
    rating_diff = models.IntegerField(default=0, blank=True)
    games_played = models.IntegerField(default=0, blank=True)
    last_active = models.DateField(auto_now=False, auto_now_add=False, blank=True, default=datetime.now())
    wins = models.IntegerField(default=0, blank=True)
    losses = models.IntegerField(default=0, blank=True)
    draws = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return '{}'.format(self.firstname) + ' {}'.format(self.lastname) + ': {}'.format(self.rating)

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from io import TextIOWrapper

# def validate_vega_chess_entry(entry):
#     raise ValidationError(_('Line is too long'))

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

def adjustEloFromAllGames(provisional, ratings, gameResults, gamePlayers, K):
    nonProvIndices = np.where(provisional[np.arange(provisional.size)] == False)[0]
    temp = (10 ** (ratings / 400))[..., np.newaxis]
    ratings[nonProvIndices] += K*np.sum((gameResults - temp/(temp + 10 ** (ratings[gamePlayers] / 400)))[nonProvIndices], axis=1)

def centerProvisionalPlayers(provisional, ratings, gamePlayers, gameResults):
    provIndices = np.where(provisional[np.arange(provisional.size)])[0]
    nonProvIndices = np.where(provisional[np.arange(provisional.size)] == False)[0]
    reversePImap = {provIndices[i] : i for i in range(provIndices.size)}
    provMatrix = np.zeros((provIndices.size, provIndices.size + 1))
    ratingAnchor = False
    for i in range(provIndices.size):
        for j in range(gamePlayers.shape[1]):
            opp = gamePlayers[provIndices[i]][j]
            if provisional[opp]:
                provMatrix[i][reversePImap[opp]] -= 1
                provMatrix[i][provIndices.size] += 800*gameResults[provIndices[i]][j] - 400
            else:
                ratingAnchor = True
                provMatrix[i][provIndices.size] += ratings[opp] + 800*gameResults[provIndices[i]][j] - 400
        provMatrix[i][i] += gamePlayers.shape[1]

    # To prevent the matrix from being degenerate, which it SHOULD be in this case, but we're cheating around it anyways...
    if not ratingAnchor:
        provMatrix[0][provIndices.size] += 1
        provMatrix[0][0] += 1

    newMat = sp.Matrix(provMatrix).rref()
    print(newMat)
    lastCol = np.array(newMat[0].col(-1).transpose())
    print(lastCol)

    if not ratingAnchor:
        lastCol += 1500 - np.sum(lastCol)/lastCol.size
        print(lastCol)

    for x, y in reversePImap.items():
        ratings[x] = lastCol[0][y]

@receiver(models.signals.post_save, sender=VegaChessEntry)
def parse_vega_chess_entry(sender, instance, **kwargs):
    file = TextIOWrapper(instance.entry)
    games = []
    firstNames = []
    lastNames = []
    ratings = []
    flag = False
    for line in file:
        if line[0] == '-':
            flag = True
        elif flag and line.strip() == "":
            break
        elif flag:
            firstNames.append(line.split()[1])
            lastNames.append(line.split()[2])
            games.append(line[line.find('|') + 1 : line.rfind('|')].split())

    print(games)

    for i in range(len(firstNames)):
        fn = firstNames[i]
        ln = lastNames[i]
        try:
            SelectedPlayer = Player.objects.get(firstname=fn, lastname=ln)

        except Player.DoesNotExist:
            SelectedPlayer = Player.objects.create(firstname=fn, lastname=ln)

        ratings.append(SelectedPlayer.rating)

    gamePlayers = [[None]*len(games[i]) for i in range(len(games))]
    gameResults = [[None]*len(games[i]) for i in range(len(games))]

    for i in range(len(games)):
        for j in range(len(games[i])):
            if games[i][j][0] == '+':
                if games[i][j][1:] == "BYE":
                    gamePlayers[i][j] = i
                    gameResults[i][j] = 0.5
                    continue
                else:
                    gameResults[i][j] = 1
            elif games[i][j] == '--':
                gamePlayers[i][j] = i
                gameResults[i][j] = 0.5
                continue
            elif games[i][j][0] == '-':
                gameResults[i][j] = 0
            else:
                gameResults[i][j] = 0.5
            gamePlayers[i][j] = int(games[i][j][2:]) - 1
    provisionalN = np.asarray([True for i in range(len(ratings))])
    #provisionalN[2] = False
    #provisionalN[6] = False
    ratingsN =  np.asarray(ratings, dtype="float64")
    gamePlayersN = np.asarray(gamePlayers)
    gameResultsN = np.asarray(gameResults)
    print(ratings)
    print(provisionalN)
    print(ratingsN)
    print(gameResultsN)
    print(np.sum(gameResultsN == 0), np.sum(gameResultsN == 1))
    centerProvisionalPlayers(provisionalN, ratingsN, gamePlayersN, gameResultsN)
    print(ratingsN)
    adjustEloFromAllGames(provisionalN, ratingsN, gameResultsN, gamePlayersN, 32)
    print(ratingsN)

    # for row in games:
    #     toAddP = []
    #     toAddR = []
    #     for entry in row:
    #         if entry[0] == '+':
    #             if entry[1:] == "BYE":
    #                 toAddR.append(0.5)
    #                 toAddP.append(int(entry[2:]) - 1)
    #                 continue
    #             else:
    #                 toAddR.append(1)
    #         elif entry[0] == '-':
    #             if entry[1] != '-':
    #                 toAddR.append(0)
    #             else:
    #                 toAddR.append(0.5)
    #                 toAddP.append(int(entry[2:]) - 1)
    #                 continue
    #         elif entry[0] == '=':
    #             toAddR.append(0.5)
    #
    #         toAddP.append(int(entry[2:]) - 1)
    #
    #     gamePlayers.append(toAddP)
    #     gameResults.append(toAddR)

    # fn = "test4"
    # ln = "test4"
    # try:
    #     SelectedPlayer = Player.objects.get(firstname=fn, lastname=ln)
    #     SelectedPlayer.rating = SelectedPlayer.rating + 500
    #     SelectedPlayer.save()
    #
    # except Player.DoesNotExist:
    #     SelectedPlayer = Player.objects.create(firstname=fn, lastname=ln)

    instance.delete()

class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)
