from django.contrib import admin
from django.conf.urls import patterns, include, url
from qrround.settings import settings


admin.autodiscover()

urlpatterns = patterns(
    'qrround.views',
    # Examples:
    # url(r'^$', 'qrround.views.home', name='home'),
    # url(r'^qrround/', include('qrround.foo.urls')),
    url(r'^$', 'index', name='index'),
    url(r'^getfriends', 'getfriends', name='getfriends'),
    url(r'^getqrcode$', 'getqrcode', name='getqrcode'),

    # Callback
    url(r'^oauth2callback$', 'oauth2callback', name='oauth2callback'),
    url(r'^facebook_callback$', 'facebookcallback', name='facebookcallback'),  # noqa
    url(r'^google_callback$', 'googlecallback', name='googlecallback'),
    url(r'^linkedin_callback$', 'linkedincallback', name='linkedincallback'),  # noqa
    url(r'^twitter_callback$', 'twittercallback', name='twittercallback'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^close_window$', 'close_window', name='close_window'),
    url(r'^close_window_reload$', 'close_window', {'is_reload': True},
        name='close_window_reload'),

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
