from django import http
from django.contrib import auth
from django.template import RequestContext, Context, loader
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf


import time
import models
import decimal
import pprint
import traceback

def user_properties(request) :
  user = None
  if request.user.is_authenticated() :
    user = request.user
  elif ('username' in request.POST) and ('password' in request.POST) :
    user = django.contrib.auth.authenticate(username, password)

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

def render_respond(request, tfilename, context_dict=None) :
  t = loader.get_template(tfilename)

  cd = {
  }
  if context_dict :
    cd.update(context_dict)

  if 'title' not in cd :
    cd['title'] = "REDCROSS"
  
  return http.HttpResponse(t.render(RequestContext(request, cd)))

def fieldreports_home(request) :
  d = {"title" : "Field Reports"}
  d['user_properties'] = user_properties(request)

  return render_respond(request, "tmpl/fieldreport.html", d)

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

@csrf_protect
def fieldreports_create(request) :
  try :
    d = {}
    d['user_properties'] = user_properties(request)

    if not d['user_properties']['is_responder'] :
      return http.HttpResponse('Unauthorized', status=401)

    description = request.POST['description']

    latitude = None
    longitude = None
    try :
      latitude = float(request.POST['lat'])
      longitude = float(request.POST['lon'])
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

    return render_respond(request, "tmpl/fieldreport.html", d)
  except :
    print traceback.format_exc()
    return http.HttpResponse('Unhandled error', status=500)

def login(request):
	return render_respond(request,'tmpl/login.html')

def logout(request):
	auth.logout(request)
	return render_response(request, 'tmpl/home.html')


