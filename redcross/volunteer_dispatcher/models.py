from django.db import models
import django.contrib.auth.models
from phonenumber_field.modelfields import PhoneNumberField

class HasLocation(models.Model) :
	class Meta :
		abstract = True

	# home address
	city = models.CharField(max_length=20, null=False)
	state = models.CharField(max_length=2, null=False)
	county = models.CharField(max_length=20, null=False)

	addr1 = models.CharField(max_length=50, null=True, blank=True)
	addr2 = models.CharField(max_length=50, null=True, blank=True)
	addr3 = models.CharField(max_length=50, null=True, blank=True)
	postcode = models.CharField(max_length=10, null=True, blank=True)

	# current location if known, otherwise their home
	latitude = models.DecimalField(max_digits=10, decimal_places=6)
	longitude = models.DecimalField(max_digits=10, decimal_places=6)

	def __unicode__(self) :
		return self.county

# Create your models here.
class Volunteer (HasLocation) :
	user = models.ForeignKey(django.contrib.auth.models.User, blank=True, null=True)

	first_name = models.CharField(max_length=30, null=False)
	last_name = models.CharField(max_length=40, null=False)

	cell_phone = PhoneNumberField(blank=True, null=True)
	work_phone = PhoneNumberField(blank=True, null=True)
	home_phone = PhoneNumberField(blank=True, null=True)

	def __unicode__(self) :
		return '%s, %s (%s)' % (self.last_name, self.first_name, HasLocation.__unicode__(self))

class IncidentType(models.Model) :
	name = models.CharField(max_length=20, null=False)

	def __unicode__(self) :
		return self.name

class Incident(HasLocation) :
	incident_type = models.ForeignKey(IncidentType)
	dispatcher_initial_description = models.TextField()

	def __unicode__(self) :
		return '%s: %s' % (str(self.incident_type), self.dispatcher_initial_description[0:50])
