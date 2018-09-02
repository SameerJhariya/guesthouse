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
		if request.user.is_superuser:
			return render(request, 'admin.html')
		else:
			return render(request, 'student.html')
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
	roomobj = Room.objects.get(id=rid)
	roomobj.active = False
	roomobj.save()
	return HttpResponse("Room Booked Successfully!")


def block(request):
	return HttpResponse('Block')
