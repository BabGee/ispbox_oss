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
	name = models.CharField(max_length=100,unique=True)
	location = models.CharField(max_length=100)
	status = models.ForeignKey(TenantStatus, on_delete=models.CASCADE, blank=True, null=True) 	

	def __str__(self):
		return self.name



class Port(models.Model):
	port_number = models.IntegerField(unique=True)
	is_allocated = models.BooleanField(default=False) 	

	def __str__(self):
		return str(self.port_number)
	

class TenantPortAssignment(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    port = models.ForeignKey(Port, on_delete=models.CASCADE)
