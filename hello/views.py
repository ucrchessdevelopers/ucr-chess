from django.shortcuts import render
from django.http import HttpResponse
import requests, json

from .models import *
from django.contrib.auth.models import User

def index(request):
	images = CarouselImage.objects.all().order_by('order')
	return render(request, "index.html", {'CarouselImageData': images})

def oldRankings(request):
	data = Player.objects.all().order_by('-rating')
	users = User.objects.all()
	return render(request, "rankings.html", {'playerData': data, 'userData': users})

def rankings(request):
	players = Player.objects.all()#.order_by('-rating')
	cRatings = []
	bRatings = []
	wins = []
	losses = []
	draws = []
	for player in players:
		x = requests.get("https://lichess.org/api/user/" + player.lichessUser)
		y = json.loads(x.text)
		cRatings += y['perfs']['classical']['rating']
		bRatings += y['perfs']['blitz']['rating']
		wins += y['count']['wins']
		losses += y['count']['losses']
		draws += y['count']['draws']
	return render(request, "rankings.html", {'playerData': players, 'classicalRatings': cRatings, 'blitzRatings': bRatings, 'playerWins': wins, 'playerLosses': losses, 'playerDraws': draws})

def about(request):
	ofs = Officer.objects.all().order_by('order', 'name')
	return render(request, "about.html", {'officerData': ofs})
