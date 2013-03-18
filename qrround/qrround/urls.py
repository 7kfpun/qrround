from django.contrib import admin
from django.conf.urls import patterns, include, url
from settings import settings


admin.autodiscover()

urlpatterns = patterns(
    'qrround.views',

    url(r'^$', 'index', name='index'),
    url(r'^getfriends$', 'getfriendsrequest', name='getfriendsrequest'),
    url(r'^getqrcode$', 'getqrcode', name='getqrcode'),

    # Callback
    url(r'^oauth2callback$', 'oauth2callback', name='oauth2callback'),
    url(r'^facebook_callback$', 'facebookcallback', name='facebookcallback'),  # noqa
    url(r'^google_callback$', 'googlecallback', name='googlecallback'),
    url(r'^linkedin_callback$', 'linkedincallback', name='linkedincallback'),  # noqa
    url(r'^twitter_callback$', 'twittercallback', name='twittercallback'),
    url(r'^renren_callback$', 'renrencallback', name='renrencallback'),

    url(r'^logout/$', 'logout_user', name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^close_window$', 'close_window', name='close_window'),
    url(r'^close_window_reload$', 'close_window', {
        'is_reload': True}, name='close_window_reload'),

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
