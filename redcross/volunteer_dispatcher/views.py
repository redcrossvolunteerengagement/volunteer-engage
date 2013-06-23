from django import http
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
def fieldreports_create_auth(request) :
  return fieldreports_create_core(request, True)

@csrf_protect
def fieldreports_create(request) :
  return fieldreports_create_core(request, False)

def fieldreports_create_core(request, csrf_unsafe) :
  pprint.pprint(request.POST) 

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
      if slat :
        latitude = float(slat)
      slon = request.POST['longitude']
      if slon :
        longitude = float(slon)
    except KeyError :
      print 'oh no, no location known :('
    except decimal.InvalidOperation :
      return http.HttpResponse("Bad input, could not parse the decimal value for lat or lon", status=400)

    fieldreport = models.FieldReport()
    fieldreport.volunteer = d['user_properties']['volunteer']
    fieldreport.ts = long(time.time())
    fieldreport.latitude = latitude
    fieldreport.longitude = longitude
    fieldreport.description = description
    fieldreport.save()

    d['message'] = 'Report filed'
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
