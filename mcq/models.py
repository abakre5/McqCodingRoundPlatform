from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime 
from django.utils import timezone
# Create your models here.

class Qrecord(models.Model):
	question = models.TextField(max_length=500)
	snipphet = models.TextField(max_length=500)
	answer1 = models.TextField(max_length=100)
	answer2 = models.TextField(max_length=100)
	answer3 = models.TextField(max_length=100)
	answer4 = models.TextField(max_length=100)
	correct = models.IntegerField()
	def __str__(self):
		return (self.question)

class SeniorQrecord(models.Model):
	question = models.TextField(max_length=500)
	snipphet = models.TextField(max_length=500)
	answer1 = models.TextField(max_length=100)
	answer2 = models.TextField(max_length=100)
	answer3 = models.TextField(max_length=100)
	answer4 = models.TextField(max_length=100)
	correct = models.IntegerField()
	def __str__(self):
		return (self.question)
		
class Profile(models.Model):
	user = models.OneToOneField(User)                   # done by shreyash
	#email = models.CharField(max_length=40)  #done by shreyash
	score = models.IntegerField(blank=True, null=True, default=0)
	name1 = models.CharField(max_length=30 , blank=True)
	name2 = models.CharField(max_length=30 , blank=True, null=True)
	contact = models.CharField(max_length=30 , blank=True)
	college = models.CharField(max_length=50, blank=True)
	reciept = models.CharField(blank=True,max_length=10)
	skip = models.IntegerField(default=2)
	count = models.IntegerField(default=0)
	start = models.DateTimeField(null=True)
	end = models.DateTimeField(blank=False)
	endgame = models.BooleanField(default=False)
	level = models.CharField(max_length=20,null=True)
	lasttimeupdated = models.DateTimeField(null=True)
	skipscoreadded = models.IntegerField(default=0)
	correct_count = models.IntegerField(default=0)
	wrong_count = models.IntegerField(default=0)
	def __str__(self):
		return (self.name1)

class Qattempt(models.Model):
	user = models.ForeignKey(Profile)
	attempt = models.ForeignKey(Qrecord,SeniorQrecord)
	correct_count = models.IntegerField(default=0)
	def __str__(self):
		return (str(self.correct_count))

class SeniorQattempt(models.Model):
	user = models.ForeignKey(Profile)
	attempt = models.ForeignKey(SeniorQrecord)
	correct_count = models.IntegerField(default=0)
	def __str__(self):
		return (str(self.correct_count))
