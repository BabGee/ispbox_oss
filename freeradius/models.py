# models.py
from django.db import models

class RadCheck(models.Model):
    username = models.CharField(max_length=64)
    attribute = models.CharField(max_length=64)
    op = models.CharField(max_length=2, default='==')
    value = models.CharField(max_length=253)

    class Meta:
        managed = False  # tells Django not to manage the schema for this model
        db_table = 'radcheck'    
