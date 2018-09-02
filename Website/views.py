from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserRegistrationForm
from django import forms
from django.contrib.auth.models import User
from .models import Person, Room, GuestHouse, Request



def index(request):
	vip_count = Room.objects.filter(vip=True).filter(active=False).count()
	if request.user.is_authenticated():
		return render(request, 'admin.html', {"count" : vip_count})
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
	vip_count = Room.objects.filter(vip=True).filter(active=False).count()
	if vip_count >= 3:
		rooms = Room.objects.filter(guesthouse=gh).filter(active=True)[vip_count+1:]
	else:
		rooms = Room.objects.filter(guesthouse=gh).filter(active=True)[3:]
	return render(request, 'room.html', {'rooms' : rooms})

def payment(request):
	rid = request.GET['room']
	uname = request.GET['uname']
	raw_user = User.objects.get(username=uname)
	user = Person.objects.get(user=raw_user)
	roomobj = Room.objects.get(id=rid)
	roomobj.active = False
	user.room = roomobj
	user.booked = True
	roomobj.save()
	user.save()
	return HttpResponse('<br><div class="ui container"><div class="ui positive message"><div class="header">Room Booked Successfully!</div></div></div>')


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
			return HttpResponse('<br><div class="ui container"><div class="ui positive message"><div class="header">'+str(room.name)+" room Blocked"+'</div></div></div>')
		else:
			room.active = True
			room.vip = False
			room.save()
			persons = Person.objects.filter(room=room)
			for person in persons:
				person.booked = False
				person.room = None
				person.save()
			return HttpResponse('<br><div class="ui container"><div class="ui positive message"><div class="header">'+str(room.name)+" room Unblocked"+'</div></div></div>')
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


def request_room(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')

	if Request.objects.filter(person=request.user.person).exists():
			return HttpResponse('<br><div class="ui container"><div class="ui negative message"><div class="header">'+"Already requested room "+'</div></div></div>')

	if 'rid' in request.GET:
		req = Request()
		req.person = request.user.person
		req.room = Room.objects.get(id=request.GET['rid'])
		req.save()
		return HttpResponse('<br><div class="ui container"><div class="ui positive message"><div class="header">'+str(req.room.name)+" room Requested"+'</div></div></div>') 
	else:
		vip_count = Room.objects.filter(vip=True).filter(active=False).count()
		if vip_count >= 3:
			rooms = Room.objects.filter(active=True)[vip_count+1:]
		else:
			rooms = Room.objects.filter(active=True)[3:]
		return render(request, 'request.html', {'rooms' : rooms})

def check_request(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')
	if not request.user.is_superuser:
		return HttpResponse("Unauthorized!")

	if 'uid' in request.GET:
		status = request.GET['status']
		req = Request.objects.get(person=request.GET['uid'])
		user = req.person
		roomobj = req.room
		if status=="1":
			roomobj.active = False
			user.room = roomobj
			user.booked = True
			roomobj.save()
			user.save()
			req.delete()
			return HttpResponse('<br><div class="ui container"><div class="ui positive message"><div class="header">'+str(roomobj.name)+" room Approved"+'</div></div></div>') 
		else:
			req.delete()
			return HttpResponse('<br><div class="ui container"><div class="ui negative message"><div class="header">'+str(roomobj.name)+" room Rejected"+'</div></div></div>') 
	else:
		reqs = Request.objects.all()
		return render(request, 'check_request.html', {'reqs' : reqs})

def occupied(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')
	if not request.user.is_superuser:
		return HttpResponse("Unauthorized!")

	occupied_users = Person.objects.filter(booked=True)
	return render(request, 'occupied.html', {'users' : occupied_users})
