from django.shortcuts import render
from django.http import HttpResponse
import requests, json, threading

from .models import *
from django.contrib.auth.models import User

def index(request):
	images = CarouselImage.objects.all().order_by('order')
	return render(request, "index.html", {'CarouselImageData': images})

def oldRankings(request):
	data = Player.objects.all().order_by('-rating')
	users = User.objects.all()
	return render(request, "rankings.html", {'playerData': data, 'userData': users})

def getPlayerInfo(playerData, ind, username):
	requests.get("https://lichess.org/api/user/" + username)
	y = json.loads(x.text)
	playerData['cRatings'][ind] = y['perfs']['classical']['rating']
	playerData['bRatings'][ind] = y['perfs']['blitz']['rating']
	playerData['wins'][ind] = y['count']['wins']
	playerData['draws'][ind] = y['count']['draws']
	playerData['losses'][ind] = y['count']['losses']

def rankings(request):
	players = Player.objects.all()
	# Player.objects.all().delete()
	# np = Player()
	# np.firstname = "sa"
	# np.lastname = "mi"
	# np.lichessUser = "smish2222"
	# np.save()
	# np = Player()
	# np.firstname = "sas"
	# np.lastname = "mit"
	# np.lichessUser = "sepy97"
	# np.save()
	playerData = {'cRatings': [None]*len(players), 'bRatings': [None]*len(players), 'wins': [None]*len(players), 'draws': [None]*len(players), 'losses': [None]*len(players)}
	# cRatings = []
	# bRatings = []
	# wins = []
	# losses = []
	# draws = []
	reqThreads = []
	playerIndex = 0
	for player in players:
		reqThreads.append(threading.Thread(target = getPlayerInfo, args = (playerData, playerIndex, player.lichessUser)))
		reqThreads[-1].start()
		playerIndex += 1

	for t in reqThreads:
		t.join()

	return render(request, "rankings.html", {'playerData': players, 'classicalRatings': playerData['cRatings'], 'blitzRatings': playerData['bRatings'], 'playerWins': playerData['wins'], 'playerLosses': playerData['losses'], 'playerDraws': playerData['draws']})

def about(request):
	ofs = Officer.objects.all().order_by('order', 'name')
	return render(request, "about.html", {'officerData': ofs})
