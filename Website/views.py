from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserRegistrationForm
from django import forms
from django.contrib.auth.models import User
from .models import Person, Room, GuestHouse



def index(request):
	if request.user.is_authenticated():
		return render(request, 'admin.html')
	else:
		return HttpResponseRedirect('/login')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email =  userObj['email']
            password =  userObj['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)

                user = authenticate(username = username, password = password)
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/signup.html', {'form' : form})

def book(request):
	guesthouses = GuestHouse.objects.all();
	return render(request, 'book.html', {'gh' : guesthouses})

def room(request):
	gh = request.GET['gid']
	rooms = Room.objects.filter(guesthouse=gh)
	return render(request, 'room.html', {'rooms' : rooms})

def payment(request):
	rid = request.GET['room']
	user = request.user.person
	roomobj = Room.objects.get(id=rid)
	roomobj.active = False
	user.room = roomobj
	user.booked = True
	roomobj.save()
	user.save()
	return HttpResponse("<br>Room Booked Successfully!")


def block(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')
	if not request.user.is_superuser:
		return HttpResponse("Unauthorized!")

	if 'rid' in request.GET:
		room = Room.objects.get(id=request.GET['rid'])
		if(room.active):
			room.active = False
			room.save()
			return HttpResponse("<br>"+str(room.name)+" room Blocked")
		else:
			room.active = True
			room.save()
			person = Person.objects.get(room=room)
			person.booked = False
			person.room = None
			person.save()
			return HttpResponse("<br>"+str(room.name)+" room Unblocked")
	else:
		rooms = Room.objects.all()
		return render(request, 'block.html', {'rooms' : rooms})

def changecap(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')
	if not request.user.is_superuser:
		return HttpResponse("Unauthorized!")

	if request.method == 'POST' :
		room = Room.objects.get(name=request.POST['room'])
		room.capacity = request.POST['cap']
		room.save()
		return HttpResponse("<br>"+str(room.name)+" capacity changed to "+str(room.capacity))
	else:
		rooms = Room.objects.all()
		return render(request, 'change.html', {'rooms' : rooms})
