from django.contrib import admin
from django.conf.urls import patterns, include, url

import volunteer_dispatcher.models

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

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login', {
    'login': 'myapp/login.html'
	}),
)
