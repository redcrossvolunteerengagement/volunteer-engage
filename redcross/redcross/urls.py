import os

from django.contrib import admin
from django.conf.urls import patterns, include, url

import django.views.static
import volunteer_dispatcher.models
import volunteer_dispatcher.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

admin.site.register(volunteer_dispatcher.models.Volunteer, admin.ModelAdmin)
admin.site.register(volunteer_dispatcher.models.Incident, admin.ModelAdmin)
admin.site.register(volunteer_dispatcher.models.IncidentType, admin.ModelAdmin)
admin.site.register(volunteer_dispatcher.models.FieldReport, admin.ModelAdmin)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'redcross.views.home', name='home'),
    # url(r'^redcross/', include('redcross.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'media'))}),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fieldreport/$', 'volunteer_dispatcher.views.fieldreports_home'), # list field reports or file them
    url(r'^fieldreport/mark_read$', 'volunteer_dispatcher.views.fieldreports_mark_read'), # list field reports or file them
    url(r'^fieldreport/create$', 'volunteer_dispatcher.views.fieldreports_create'), # create a field report
    #url(r'^fieldreport/mark_read$', 'volunteer_dispatcher.views.fieldreports_mark_read'), # list field reports or file them
    url(r'login/$', 'django.contrib.auth.views.login', {'template_name':'tmpl/login.html'}, name='login')
)
