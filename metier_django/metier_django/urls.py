from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'metier_django.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^serveurweb/',    include('serveurweb.urls')),
    url(r'^serveurXMLRPC/', include('serveurXMLRPC.urls')),
    url(r'^serveurREST/',   include('serveurREST.urls')),
    url(r'^admin/doc/',     include('django.contrib.admindocs.urls')),
    url(r'^admin/',         include(admin.site.urls)),
  )
