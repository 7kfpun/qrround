from django.conf.urls import patterns, include, url

from qrround import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'qrround.views.home', name='home'),
    # url(r'^qrround/', include('qrround.foo.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^getPic$', views.getPic, name='getPic'),
    url(r'^getqrcode$', views.getqrcode, name='getqrcode'),

    # Callback
    url(r'^oauth2callback$', views.oauth2callback, name='oauth2callback'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Static files
    # url(r'^js/*', ),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
