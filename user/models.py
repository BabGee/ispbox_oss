from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

from tenant.models import *

class User(AbstractUser):
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)	
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.EmailField(null=True, blank=True)
	phone_number = models.CharField(max_length=13)
	
	
class AccessLevel(models.Model):
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)
	name = models.CharField(max_length=50, unique=True)
	description = models.CharField(max_length=100)

	def __str__(self):
		return self.name
	
	

class ProfileStatus(models.Model):
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)
	name = models.CharField(max_length=50, unique=True)
	description = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class Profile(models.Model):
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)	
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, blank=True, null=True) 
	access_level = models.ForeignKey(AccessLevel, on_delete=models.CASCADE, blank=True, null=True)
	status = models.ForeignKey(ProfileStatus, on_delete=models.CASCADE, blank=True, null=True)
	def __str__(self):
		return self.user.username     

def post_save_profile_create(sender, instance, created,*args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)                                       
        
post_save.connect(post_save_profile_create, sender=User)            

