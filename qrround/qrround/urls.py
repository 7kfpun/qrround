# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from settings import settings


admin.autodiscover()

urlpatterns = patterns(
    'qrround.views',

    url(r'getfriends/$', 'getfriendsrequest', name='getfriendsrequest'),
    url(r'getgallery/$', 'getgallery', name='getgallery'),
    url(r'autopostfacebook/$', 'autopostfacebook', name='autopostfacebook'),

    url(r'postfacebookphotos', 'postfacebookphotos', name='postfacebookphotos'),  # noqa
    url(r'postkaixin001photos', 'postkaixin001photos', name='postkaixin001photos'),  # noqa

    # Callback
    url(r'^facebook_callback$', 'facebookcallback', name='facebookcallback'),  # noqa
    url(r'^google_callback$', 'googlecallback', name='googlecallback'),
    url(r'^kaixin001_callback$', 'kaixin001callback', name='kaixin001callback'),  # noqa
    url(r'^linkedin_callback$', 'linkedincallback', name='linkedincallback'),  # noqa
    url(r'^twitter_callback$', 'twittercallback', name='twittercallback'),
    url(r'^renren_callback$', 'renrencallback', name='renrencallback'),
    url(r'^weibo_callback$', 'weibocallback', name='weibocallback'),

    url(r'sendcontact$', 'sendcontact', name='sendcontact'),

    # Uncomment the next line to enable the admin:
    url(r'^accounts/login/$', 'login', name='login'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rosetta/', include('rosetta.urls')),

    url(r'^logout/$', 'logout_user', name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^close_window$', 'close_window', name='close_window'),
    url(r'^close_window_reload$', 'close_window', {
        'is_reload': True}, name='close_window_reload'),

    url(r'testtasks$', 'testtasks', name='testtasks'),

    # the rest is above
    url(r'^i18n/', include('django.conf.urls.i18n')),
)

urlpatterns += i18n_patterns(
    'qrround.views',

    url(r'^$', 'index', name='index'),
    url(r'^getauthurls/$', 'getauthurls', name='getauthurls'),
    url(r'^getqrcode/$', 'getqrcode', name='getqrcode'),
    url('^tasks/', include('djcelery.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^(.*)/media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            }),
        url(r'^(.*)/static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
            }),
    )
