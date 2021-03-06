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

	is_trainee = models.BooleanField(default=False)
	is_dispatcher = models.BooleanField(default=False)

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
	volunteer = models.ForeignKey(Volunteer, blank=True, null=True)
	incident_type = models.ForeignKey(IncidentType)
	dispatcher_initial_description = models.TextField()
	required_responders = models.IntegerField(default=1)
	required_trainees = models.IntegerField(default=1)
	is_open = models.BooleanField(default=True)

	def __unicode__(self) :
		return '%s: %s' % (str(self.incident_type), self.dispatcher_initial_description[0:50])

class FieldReport(models.Model) :
	ts = models.BigIntegerField(blank=True, null=True)
	uuid = models.TextField(max_length=36, blank=True, null=True, db_index=True, unique=True)
	volunteer = models.ForeignKey(Volunteer)
	latitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
	longitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
	description = models.TextField()
	read = models.BooleanField(default=False)
        read_ts = models.BigIntegerField(blank=True, null=True)
	# it would be fancy later to make it so a field report could be linked to an incident after the fact, but nah.
