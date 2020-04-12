from django.shortcuts import render
from django.http import HttpResponse

from .models import *
from django.contrib.auth.models import User

def index(request):
    images = CarouselImage.objects.all().order_by('order')
    buttons = LinkButton.objects.all().order_by('order')
    pageText = FrontPageText.objects.all()
    return render(request, "index.html", {'CarouselImageData': images, 'LinkButtonData': buttons, 'pageText': pageText})

def rankings(request):
    data = Player.objects.all().order_by('-rating')
    users = User.objects.all()
    return render(request, "rankings.html", {'playerData': data, 'userData': users})

def about(request):
    ofs = Officer.objects.all().order_by('order', 'name')
    return render(request, "about.html", {'officerData': ofs})

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
