from django.db import models


class TenantStatus(models.Model):
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)
	name = models.CharField(max_length=50, unique=True)
	description = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class Tenant(models.Model):
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)	
	name = models.CharField(max_length=100)
	location = models.CharField(max_length=100)
	ip_address = models.GenericIPAddressField(blank=True, null=True)
	port = models.PositiveIntegerField(blank=True, null=True)
	status = models.ForeignKey(TenantStatus, on_delete=models.CASCADE, blank=True, null=True) 	

	def __str__(self):
		return self.name
