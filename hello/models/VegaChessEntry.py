from django.db import models
from django.utils.html import mark_safe
from upload_validator import FileTypeValidator
from django.dispatch import receiver
from db_file_storage.model_utils import delete_file, delete_file_if_needed
# from django.utils.translation import gettext_lazy as _
from io import TextIOWrapper
from .Player import *

import numpy as np
import sympy as sp

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
    for i in range(len(firstNames)):
        fn = firstNames[i]
        ln = lastNames[i]

        SelectedPlayer = Player.objects.get(firstname=fn, lastname=ln)


        SelectedPlayer.last_active = instance.tournament_date
        SelectedPlayer.rating_diff = ratings[i] - SelectedPlayer.rating
        SelectedPlayer.rating = ratings[i]
        SelectedPlayer.save()




    instance.delete()
