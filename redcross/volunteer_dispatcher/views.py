import sms_integration
import coordinates
from django import http
import django.db
from django.contrib import auth
from django.template import RequestContext, Context, loader

# save us from csrf!
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.context_processors import csrf

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect


import time
import models
import decimal
import pprint
import traceback
import datetime

import uuid
import re
UUID_RE = re.compile('^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$')

def uuidgen() :
  return str(uuid.uuid4())

def user_properties(request, csrf_unsafe=False) :
  user = None
  if request.user.is_authenticated() :
    if csrf_unsafe :
      print 'user_properties: pre-authenticated requests must be csrf safe'
      return http.HttpResponse('Unauthorized', status=401)
    user = request.user
    print 'user_properties: authenticated'
  elif ('username' in request.POST) and ('password' in request.POST) :
    print 'user_properties: trying to authenticate'
    user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
  else :
    print 'user_properties: was not logged in and did not send username and password, they have no rights'

  return user_properties_core(user)

def user_properties_core(user) :
  d = {}
  volunteer = None

  if user :
    volunteers = list(models.Volunteer.objects.filter(user=user))
    if len(volunteers) != 1 :
      print 'error with how many volunteer records associated with user, aborting request with bad permissions'
    else :
      volunteer = volunteers[0]

  if volunteer :
    d['logged_in'] = True
    d['is_dispatcher'] = volunteer.is_dispatcher
    d['is_trainee'] = volunteer.is_trainee
    d['is_responder'] = True # TODO not always true, but this is for permissions so yes it is for now
    d['volunteer'] = volunteer
  else :
    d['logged_in'] = False
    d['is_dispatcher'] = False
    d['is_trainee'] = False
    d['is_responder'] = False

  return d

def render_respond(request, tfilename, context_dict=None, do_csrf=False) :
  t = loader.get_template(tfilename)

  cd = {
  }
  if context_dict :
    cd.update(context_dict)

  if 'title' not in cd :
    cd['title'] = "REDCROSS"
  
  ctx = RequestContext(request, cd)
  if do_csrf :
    ctx.update(csrf(request))

  return http.HttpResponse(t.render(ctx))

@csrf_protect
def fieldreports_home(request) :
  d = {"title" : "Field Reports"}
  d['user_properties'] = user_properties(request)

  if d['user_properties']['is_dispatcher'] :
    d['fieldreport_disposition'] = 'view'
  else :
    d['fieldreport_disposition'] = 'file'

  if 'action' in request.POST :
    if not d['user_properties']['is_dispatcher'] :
      return http.HttpResponse('Unauthorized', status=401)

    if request.POST['action'] == 'mark_read' and 'fieldreport_id' in request.POST :
      # TODO handle bad value for field report id well
      fieldreport_id = long(request.POST['fieldreport_id'])
      fieldreport = models.FieldReport.objects.get(id=fieldreport_id)
      fieldreport.read = True
      fieldreport.read_ts = long(time.time())
      fieldreport.save()

  add_open_fieldreports(d)

  return render_respond(request, "tmpl/fieldreport.html", d)

@csrf_protect
def incidents_home(request) :
  d = {"title" : "Dispatch Incident"}
  d['user_properties'] = user_properties(request)

  if not d['user_properties']['is_dispatcher'] :
    return http.HttpResponse('Unauthorized', status=401)

  add_open_incidents(d)

  return render_respond(request, "tmpl/incident.html", d)

@csrf_protect
def volunteer_dispatch_auto(request) :
  try :
    n_paged = 0

    d = {"title" : "Dispatched Incident"} # TODO make this say how many users were dispatched
    d['user_properties'] = user_properties(request)

    if not d['user_properties']['is_dispatcher'] :
      return http.HttpResponse('Unauthorized', status=401)

    if 'incident_id' in request.POST :
      # TODO handle bad value for field report id well
      incident_id = long(request.POST['incident_id'])

      # XXX this is incomplete change it
      incident = models.Incident.objects.get(id=incident_id)

      # inefficient XXX
      all_volunteers = [v for v in list(models.Volunteer.objects.all()) if (v.cell_phone and v.latitude and v.longitude)]
      print all_volunteers
      # get fancy and sort this later and limit by the number of people wanted later, WHOOPS
      #all_volunteers.sort(cmp=lambda a,b: int.__cmp__.



      for v in all_volunteers :
        cellnum = str(v.cell_phone)

        print cellnum

        notifier = sms_integration.Notifiers.get()
        notifier.send(cellnum, ("You've been paged to an incident at %s, please call dispatch. Details: %s" % (incident.addr1, incident.dispatcher_initial_description))[0:120])
        n_paged += 1

    d['n_paged'] = n_paged
    return render_respond(request, "tmpl/paged.html", d)
  except :
    print traceback.format_exc()
    return http.HttpResponse('Unhandled error', status=500)
    
  
def add_open_fieldreports(d) :
  if not d['user_properties']['is_dispatcher'] :
    d['fieldreports'] = []
  else :
    reports = list(models.FieldReport.objects.filter(read=False))
    reports.reverse()
    for i in range(len(reports)) :
      reports[i].sequence_id = i + 1
      reports[i].ts=datetime.datetime.fromtimestamp(reports[i].ts);
    d['fieldreports'] = reports


def add_open_incidents(d) :
  if not d['user_properties']['is_dispatcher'] :
    d['incidents'] = []
  else :
    incidents = list(models.Incident.objects.filter(is_open=True))
    incidents.reverse()
    for i in range(len(incidents)) :
      incidents[i].sequence_id = i + 1
      #incidents[i].ts=datetime.datetime.fromtimestamp(reports[i].ts);
    d['incidents'] = incidents

@csrf_protect
def fieldreports_mark_read(request) :
  d = {}
  d['user_properties'] = user_properties(request)

  if d['user_properties']['is_dispatcher'] :
    d["title"] = "Field Report Marked Read"

    # TODO implement
  else :
    d["title"] = "Error, no permissions"

  return render_respond(request, "tmpl/fieldreport.html", d)

@csrf_exempt
def fieldreports_create_api(request) :
  return fieldreports_create_core(request, True, True)

@csrf_protect
def fieldreports_create(request) :
  return fieldreports_create_core(request, False, False)

def fieldreports_create_core(request, csrf_unsafe, uuid_required) :
  pprint.pprint(request.POST) 

  uuid_input = None
  try :
    uuid_i = request.POST['uuid']
    if UUID_RE.match(uuid_i) :
      uuid_input = uuid_i
  except KeyError :
    pass

  if not uuid_input :
    if uuid_required :
      return http.HttpResponse('UUID invalid or not supplied when required', status=403)
    else :
      uuid_input = uuidgen()

  try :
    d = {}
    d['user_properties'] = user_properties(request, csrf_unsafe=csrf_unsafe)

    if not d['user_properties']['is_responder'] :
      return http.HttpResponse('Unauthorized', status=401)

    description = request.POST['description']

    latitude = None
    longitude = None
    try :
      slat = request.POST['latitude']
      slon = request.POST['longitude']

      if slat and slon :
        latitude = float(slat)
        longitude = float(slon)
    except KeyError :
      print 'oh no, no location known :('
    except decimal.InvalidOperation :
      return http.HttpResponse("Bad input, could not parse the decimal value for lat or lon", status=400)

    try :
      fieldreport = models.FieldReport()
      fieldreport.volunteer = d['user_properties']['volunteer']
      fieldreport.uuid = uuid_input
      fieldreport.ts = long(time.time())
      fieldreport.latitude = latitude
      fieldreport.longitude = longitude
      fieldreport.description = description
      fieldreport.save()

      d['message'] = 'Report filed'
      d['fieldreport_disposition'] = 'file'
    except django.db.IntegrityError :
      d['message'] = 'Report not filed, it was a duplicate'
      d['fieldreport_disposition'] = 'file'
    
    add_open_fieldreports(d)
    return render_respond(request, "tmpl/fieldreport.html", d, do_csrf=True)
  except :
    print traceback.format_exc()
    return http.HttpResponse('Unhandled error', status=500)

@csrf_protect
def home(request) :
  d = {}
  d['user_properties'] = user_properties(request)
  return render_respond(request, "tmpl/home.html", d)
