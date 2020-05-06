from django.shortcuts import render
from django.http import HttpResponse
from .models import User

def hello(request, name):
    users = User.objects.all()
    output = [u.nick_name for u in users]
    message = "There are %s users in this website. They are: %s" % (len(users), output)
    return HttpResponse("Hello! Welcome to my home, %s.<br>%s" % (name, message))

def index(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'linkall/index.html', context)