from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from .models import User, Travel
# Create your views here.
from django.contrib.auth import authenticate, login, logout

def index(request):
    return render(request, 'travel_buddy/index.html')

def register(request):
    if request.method == 'GET':
        return redirect ('/travel/')
    newuser = User.objects.validate(request.POST)
    if newuser[0] == False:
        for each in newuser[1]:
            messages.error(request, each) #for each error in the list, make a message for each one.
        return redirect('/travel/')
    if newuser[0] == True:
        messages.success(request, 'Well done')
        request.session['id'] = newuser[1].id
        return redirect('/travel/travel')

def login_user(request):
    if 'id' in request.session:
        return redirect('/travel/travel')
    if request.method == "GET":
        return redirect('/travel')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.add_message(request, messages.INFO,'')
                request.session['id'] = user.id
                return redirect('/travel/travel')
        else:
            messages.add_message(request, messages.INFO,"Invalid login")
        return redirect('/travel/')


def travel(request):
    if 'id' not in request.session:
        return redirect ("/travel/")
    context = {
        "user": User.objects.get(id=request.session['id']),
        "travels" : Travel.objects.all(),
        "others": Travel.objects.all().exclude(join__id=request.session['id'])
    }
    return render(request, 'travel_buddy/travelplan.html', context)


def addplan(request):
    if 'id' not in request.session:
        return redirect ("/travel/")
    else:
        context= {
            "user":User.objects.get(id=request.session['id']),
        }
        return render(request, 'travel_buddy/addplan.html', context)

def createplan(request):
    if request.method != 'POST':
        return redirect ("/travel/addplan")
    newplan= Travel.objects.travelval(request.POST, request.session["id"])
    if newplan[0] == True:
        return redirect('/travel/travel')
    else:
        for message in newplan[1]:
            messages.error(request, message)
        return redirect('/travel/addplan')

def show(request, travel_id):
    try:
        travel= Travel.objects.get(id=travel_id)
    except Travel.DoesNotExist:
        messages.info(request,"Travel Not Found")
        return redirect('/travel/travel')
    context={
        "travel": travel,
        "user":User.objects.get(id=request.session['id']),
        "others": User.objects.filter(joiner__id=travel.id).exclude(id=travel.creator.id),
    }
    return render(request, 'travel_buddy/showdetail.html', context)

def join(request, travel_id):
    if request.method == "GET":
        messages.error(request,"What trip?")
        return redirect('/travel/')
    joiner= Travel.objects.join(request.session["id"], travel_id)
    if 'errors' in joiner:
        messages.error(request, joiner['errors'])
    return redirect('/travel/travel')

#
def delete(request, id):
    try:
        target= Travel.objects.get(id=id)
    except Travel.DoesNotExist:
        messages.info(request,"Message Not Found")
        return redirect('/travel/travel')
    target.delete()
    return redirect('/travel/travel')
#

def logout_user(request):
    logout(request)
    return redirect('/')
