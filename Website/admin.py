from django.contrib import admin
from .models import Room, Person, GuestHouse, Request

# Register your models here.

admin.site.register(Room)
admin.site.register(Person)
admin.site.register(GuestHouse)
admin.site.register(Request)