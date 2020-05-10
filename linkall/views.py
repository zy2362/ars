from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from .models import User, Thing
from random import random

def hello(request, name):
    newUser = User(id=int(random()*20),nick_name=str(random()*20),login_name=str(random()*20))
    newUser.save()
    users = User.objects.all()
    output = [u.nick_name for u in users]
    message = "There are %s users in this website. They are: %s" % (len(users), output)
    return HttpResponse("Hello! Welcome to my home, %s.<br>%s" % (name, message))

def index(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'linkall/index.html', context)

def dashboard(request, user_id):
    things = Thing.objects.all()
    user = User.objects.get(id=1)
    context = {'user': user, 'things': things}
    return render(request, 'linkall/dashboard.html', context)

def register(request, id):
    try:
        newThing = Thing.objects.get(id=id)
    except:
        newThing = Thing(id=id)
        newThing.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'})

def settings(request):
    things = Thing.objects.all()
    user = User.objects.get(id=1)
    context = {'user': user, 'things': things}
    return render(request, 'linkall/settings.html', context)

def sets(request):
    return HttpResponse("Success")

def claim(request, thing_id, user_id):
    try: user = User.objects.get(id=user_id)
    except: return JsonResponse({'status': 'failed', 'msg': 'User is not exsists'})
    try: thing = Thing.objects.get(id=thing_id)
    except: return JsonResponse({'status': 'failed', 'msg': 'Thing is not exsists'})
    thing.owned_by = user.id
    thing.save()
    return JsonResponse({'status': 'success'})
