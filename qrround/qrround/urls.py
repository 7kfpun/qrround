from django.contrib import admin
from django.conf.urls import patterns, include, url
from settings import settings
from qrround import views


admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'qrround.views.home', name='home'),
    # url(r'^qrround/', include('qrround.foo.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^getfriends', views.getfriends, name='getfriends'),
    url(r'^getqrcode$', views.getqrcode, name='getqrcode'),

    # Callback
    url(r'^oauth2callback$', views.oauth2callback, name='oauth2callback'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Static files
    # url(r'^js/*', ),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
            }),
    )
