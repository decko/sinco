from django.conf.urls import patterns, include, url
from sinco.core.views import index, conselhos, conselho, conselheiro

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'conselhos.views.home', name='home'),
    # url(r'^conselhos/', include('conselhos.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^flexselect/', include('flexselect.urls')),

    url(r'^conselhos/(?P<categoria>\w+)/$', conselhos),
    url(r'^conselhos/$', index),

    url(r'^conselho/(?P<conselho_id>\d+)/$', conselho),
    url(r'^conselheiro/(?P<conselheiro_id>\d+)/$', conselheiro),
)
