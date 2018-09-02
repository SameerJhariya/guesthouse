from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class GuestHouse(models.Model):
	name = models.CharField(max_length=64)
	description = models.CharField(max_length=128)
	def __str__(self):
		return self.name


class Room(models.Model):
	name = models.CharField(max_length=64)
	description = models.CharField(max_length=128)
	active = models.BooleanField(default=True)
	vip = models.BooleanField(default=False)
	guesthouse = models.ForeignKey(GuestHouse, on_delete=models.CASCADE, null=True)
	capacity = models.IntegerField(default=2)
	def __str__(self):
		return self.name

class Person(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	booked = models.BooleanField(default=False)
	room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
	def __str__(self):
		return self.user.username

class Request(models.Model):
	person = models.ForeignKey(Person, on_delete=models.CASCADE)
	room = models.ForeignKey(Room, on_delete=models.CASCADE)
	def __str__(self):
		return self.person.user.username

# To keep Person and User consistent, changes in Users are replicated in Person

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Person.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.person.save()