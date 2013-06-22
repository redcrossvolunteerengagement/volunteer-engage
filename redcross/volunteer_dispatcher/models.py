from django.db import models

# Create your models here.
class Volunteer (models.Model):
	first_name = models.CharField(max_length=30, null=False)
	last_name = models.CharField(max_length=40, null=False)
	city = models.CharField(max_length=20, null=False)
	state = models.CharField(max_length=2, null=False)
	county = models.CharField(max_length=20, null=False)
	latitude = models.DecimalField(max_digits=10, decimal_places=6)
	longitude = models.DecimalField(max_digits=10, decimal_places=6)