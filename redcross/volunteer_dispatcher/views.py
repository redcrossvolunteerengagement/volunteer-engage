# Create your views here.

from django import http
from django.template import RequestContext, Context, loader

import models

def user_properties(request) :
  d = {}

  volunteer = None

  if request.user.is_authenticated() :
    volunteers = list(models.Volunteer.objects.filter(user=request.user))
    if len(volunteers) != 1 :
      print 'error with how many volunteer records associated with user, aborting request with bad permissions'
    else :
      volunteer = volunteers[0]

  if volunteer :
    d['logged_in'] = True
    d['is_dispatcher'] = volunteer.is_dispatcher
    d['is_trainee'] = volunteer.is_trainee
    d['is_responder'] = True # TODO not always true, but this is for permissions so yes it is for now
  else :
    d['logged_in'] = False
    d['is_dispatcher'] = False
    d['is_trainee'] = False
    d['is_responder'] = False
    
    
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

  return render_respond(request, "tmpl/fieldreports_home.html", d)
