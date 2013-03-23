from celery import task
from django.contrib.auth import logout
from django.core.files import File
from django.db import transaction
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
)
from django.shortcuts import redirect, render   # , get_object_or_404
# from django.template import Context, Template
from django.utils.translation import ugettext_lazy as _
# from django.views.decorators.cache import cache_page
from jinja2 import Template
import json
import logging
import os
from ratelimit.decorators import ratelimit
import re
import requests
from settings.settings import MEDIA_ROOT, PROJECT_NAME_TEST  # TODOPROJECT_NAME
#import StringIO
from time import time
import tweepy
from urllib import urlencode

import qrcode
from .channels import *  # noqa
from .channels_settings import *  # noqa
from .forms import ContactForm, QueryForm
from .helpers import unique_generator
from .models import (
    UserClient,
    # Friend,
    QRCode,
    Query,
    CachedImage,
)


logger = logging.getLogger(__name__)


def login(request):
    if request.method == 'pOST':
        pass
    return render(request, 'login.html')


def index(request):
    print 'LANGUAGE_CODE LANGUAGE_CODE', request.LANGUAGE_CODE

    """
    state = request.session['state'] = str(time())

    # facebook
    params = {
        'scope': 'read_stream,publish_actions',
        'response_type': 'code',
        'state': state,
        'redirect_uri': FACEBOOK_REDIRECT_URI,
    }
    facebook_auth_url = facebook.get_authorize_url(**params)

    # google
    google.params.update({'state': state})
    google_auth_url = google.step1_get_authorize_url()

    # kaixin001
    params = {
        'scope': 'basic',
        'response_type': 'code',
        'state': state,
        'redirect_uri': KAIXIN001_REDIRECT_URI,
    }
    kaixin001_auth_url = kaixin001.get_authorize_url(**params)

    # linkedin
    params = {
        'scope': 'r_basicprofile r_emailaddress r_network',
        'response_type': 'code',
        'state': state,
        'redirect_uri': LINKEDIN_REDIRECT_URI,
    }
    linkedin_auth_url = linkedin.get_authorize_url(**params)

    # renren
    params = {
        'response_type': 'code',
        'state': state,
        'redirect_uri': RENREN_REDIRECT_URI,
    }
    renren_auth_url = renren.get_authorize_url(**params)

    try:
        twitter.callback = "%(redirect_url)s?state=%(state)s" \
            % {'redirect_url': RENREN_REDIRECT_URI, 'state': state}
        twitter_auth_url = twitter.get_authorization_url()
    except tweepy.TweepError:
        twitter_auth_url = None
        logger.error('Error! Failed to get access token.')

    # weibo
    params = {
        'scope': 'email,direct_messages_write,friendships_groups_read',
        'state': state,
        'redirect_uri': WEIBO_REDIRECT_URI,
        'grant_type': 'authorization_code',
    }
    weibo_auth_url = weibo.get_authorize_url(**params)

    return render(request, 'index.html', {
        'auth_urls': {
            'facebook': facebook_auth_url,
            'google': google_auth_url,
            'kaixin001': kaixin001_auth_url,
            'linkedin': linkedin_auth_url,
            'renren': renren_auth_url,
            'twitter': twitter_auth_url,
            'weibo': weibo_auth_url,
        },
        'form': QueryForm(session=request.session),
    })
    """
    return render(request, 'index.html', {
        'form': QueryForm(session=request.session),
        'contact_form': ContactForm(),
    })


def postfacebookphotos(request):
    post_id = []
    for client in request.session.get('facebook', []):
        user = UserClient.objects.filter(client=client)[0]
        url = 'https://graph.facebook.com/%s/feed' % user.client.split('#')[1]
        data = {
            'access_token': user.access_token,
            'message': PROJECT_NAME_TEST,
            'caption': PROJECT_NAME_TEST,
            'type': 'photo',
            'picture': 'http://img.photobucket.com/albums/v317/phillycrazy/blog/ZhangXuan.jpg',  # user.profile_picture_url,  # noqa
            'link': 'http://img.photobucket.com/albums/v317/phillycrazy/blog/ZhangXuan.jpg',  # user.profile_picture_url,  # noqa
        }
        r = requests.post(url, urlencode(data))
        post_id.append(r.json()['id'])

    return HttpResponse(' - '.join(post_id))


@ratelimit(rate='20/m')
def getauthurls(request):
    if getattr(request, 'limited', False):
        # Reach rate limit
        return HttpResponseBadRequest(
            _('Was_limited: we are poor, cannot afford server cost. '
              'Donate some and we can buy more server time'))

    elif True:  # and request.is_ajax():
        state = request.session['state'] = str(time())

        # facebook
        params = {
            'scope': 'read_stream,publish_actions',
            'response_type': 'code',
            'state': state,
            'redirect_uri': FACEBOOK_REDIRECT_URI,
        }
        facebook_auth_url = facebook.get_authorize_url(**params)

        # google
        google.params.update({'state': state})
        google_auth_url = google.step1_get_authorize_url()

        # kaixin001
        params = {
            'scope': 'basic',
            'response_type': 'code',
            'state': state,
            'redirect_uri': KAIXIN001_REDIRECT_URI,
        }
        kaixin001_auth_url = kaixin001.get_authorize_url(**params)

        # linkedin
        params = {
            'scope': 'r_basicprofile r_emailaddress r_network rw_nus',
            'response_type': 'code',
            'state': state,
            'redirect_uri': LINKEDIN_REDIRECT_URI,
        }
        linkedin_auth_url = linkedin.get_authorize_url(**params)

        # renren
        params = {
            'response_type': 'code',
            'state': state,
            'redirect_uri': RENREN_REDIRECT_URI,
        }
        renren_auth_url = renren.get_authorize_url(**params)

        try:
            twitter.callback = "%(redirect_url)s?state=%(state)s" \
                % {'redirect_url': RENREN_REDIRECT_URI, 'state': state}
            twitter_auth_url = twitter.get_authorization_url()
        except tweepy.TweepError:
            twitter_auth_url = None
            logger.error('Error! Failed to get access token.')

        # weibo
        params = {
            'scope': 'email,direct_messages_write,friendships_groups_read',
            'state': state,
            'redirect_uri': WEIBO_REDIRECT_URI,
            'grant_type': 'authorization_code',
        }
        weibo_auth_url = weibo.get_authorize_url(**params)

        print request.session.get('state', '***')

        return HttpResponse(json.dumps({
            'facebook': facebook_auth_url,
            'google': google_auth_url,
            'kaixin001': kaixin001_auth_url,
            'linkedin': linkedin_auth_url,
            'renren': renren_auth_url,
            'twitter': twitter_auth_url,
            'weibo': weibo_auth_url,
        }), mimetype="application/json")


def store_session(request, channel, client_id, access_token, me, friends):
    data = {
        'meta': {
            'text': 'this is text',
            'method': 'text',
            'channel': channel,
            'access_token': access_token,
        },
        'user': me,
        'friends': friends,
    }

    getfriends(data, cache_image=False)

    request.session[client_id] = data
    if channel in request.session:
        tmp = request.session[channel]
        if client_id not in tmp:
            tmp.append(client_id)
        request.session[channel] = tmp
    else:
        request.session[channel] = [client_id]

    response = redirect('/close_window')

    response = HttpResponse(json.dumps(data))  # block and see return data  TODO remove it  # noqa

    response.set_cookie(channel, time())
    return response


def facebookcallback(request):
    if request.GET.get('state', '') == request.session.get('state', '***'):
        session = facebook.get_auth_session(data={
            'code': request.GET.get('code'),
            'redirect_uri': FACEBOOK_REDIRECT_URI})
        access_token = session.access_token

        # me = session.get('me').json()
        # to get pic_square of me()
        me = session.get(
            'fql?q=SELECT uid, first_name, middle_name,'
            + ' last_name, username, name, pic_square, profile_url'
            + ' FROM user WHERE uid = me()').json()['data'][0]

        friends = session.get(
            'fql?q=SELECT uid, first_name, middle_name,'
            + ' last_name, username, name, pic_square, profile_url'
            + ' FROM user WHERE uid in (SELECT uid2 FROM friend'
            + ' WHERE uid1 = me())').json()['data']

        client_id = 'facebook#' + str(me['uid'])
        return store_session(request, 'facebook', client_id,
                             access_token, me, friends)

    else:
        return HttpResponse('CSFS?')


# Still have problem
def googlecallback(request):
    if request.GET.get('state', '') == request.session.get('state', '***'):
        credentials = google.step2_exchange(request.GET.get('code'))
        access_token = credentials.access_token

        me_url = (
            'https://www.googleapis.com/plus/v1/people/me'
            '?access_token=' + access_token
        )
        me = requests.get(me_url).json()

        friends_url = (
            'https://www.googleapis.com/plus/v1/people/me/people/visible'
            '?access_token=' + access_token
        )
        friends = requests.get(friends_url).json()['items']

        client_id = 'google#' + str(me['id'])
        return store_session(request, 'google', client_id,
                             access_token, me, friends)

    else:
        return HttpResponse('CSFS?')


def linkedincallback(request):
    if request.GET.get('state', '') == request.session.get('state', '***'):
        exchange_url = (
            'https://www.linkedin.com/uas/oauth2/accessToken'
            '?grant_type=authorization_code'
            '&code=' + request.GET.get('code')
            + '&redirect_uri=' + LINKEDIN_REDIRECT_URI
            + '&client_id=' + LINKEDIN_CLIENT_ID
            + '&client_secret=' + LINKEDIN_CLIENT_SECRET + ''
        )
        r = requests.post(exchange_url)
        access_token = r.json()['access_token']

        me_url = (
            'https://api.linkedin.com/v1/people/~'
            ':(id,first-name,last-name,headline,picture-url)'
            '?oauth2_access_token=' + access_token + '&format=json'
        )
        me = requests.get(me_url).json()

        try:
            friends_url = (
                'https://api.linkedin.com/v1/people/~/connections'
                '?oauth2_access_token=' + access_token + '&format=json')
            friends = requests.get(friends_url).json()['values']
        except KeyError:
            friends = []

        client_id = 'linkedin#' + str(me['id'])
        return store_session(request, 'linkedin', client_id,
                             access_token, me, friends)

    else:
        return HttpResponse('CSFS?')


def kaixin001callback(request):
    if request.GET.get('state', '') == request.session.get('state', '***'):
        exchange_url = (
            'https://api.kaixin001.com/oauth2/access_token'
            '?grant_type=authorization_code'
            '&code=' + request.GET.get('code')
            + '&client_id=1214876808351987b5b2f5659b72f67c'
            '&client_secret=bf2726ad4eb6dc8e3c41fa6f9edf8ab3'
            '&redirect_uri=http://127.0.0.1:8001/kaixin001_callback'
        )
        r = requests.get(exchange_url)
        access_token = r.json()['access_token']

        me_url = (
            'https://api.kaixin001.com/users/me.json'
            '?access_token=' + access_token
        )
        me = requests.get(me_url).json()

        friends_url = (
            'https://api.kaixin001.com/friends/me.json'
            '?num=50'
            '&access_token=' + access_token
        )
        friends = requests.get(friends_url).json()['users']

        client_id = 'kaixin001#' + str(me['uid'])
        return store_session(request, 'kaixin001', client_id,
                             access_token, me, friends)

    else:
        return HttpResponse('CSFS?')


def twittercallback(request):
    if request.GET.get('state', '') == request.session.get('state', '***'):
        verifier = request.GET.get('oauth_verifier')
        try:
            twitter.get_access_token(verifier)
        except tweepy.TweepError:
            print 'Error! Failed to get access token.'
            return HttpResponseNotFound('Failed to get access token')

        twitter.set_access_token(twitter.access_token.key,
                                 twitter.access_token.secret)
        api = tweepy.API(twitter)
        me = api.me()  # <object>

        friends = api.friends_ids()

#        import jsonpickle
#        me = jsonpickle.encode(me)
#        return HttpResponse(me)

        data = {
            'meta': {
                'text': 'this is text',
                'method': 'text',
                'channel': 'twitter',
            },
            'user': {
                'id': me.id_str,
                'username': me.name,
                'screen_name': me.screen_name,
                'lang': me.lang,
                'url': me.url,
                'location': me.location,
                'time_zone': me.time_zone,
                'profile_image_url': me.profile_image_url,
                'profile_image_url_https': me.profile_image_url_https,
                'profile_background_image_url': me.profile_background_image_url,  # noqa
                'profile_background_image_url_https': me.profile_background_image_url_https,  # noqa
            },
            'friends': [{'id': str(friend)} for friend in friends],
        }

        client_id = 'twitter#' + me.id_str
        return store_session(request, 'twitter', client_id,
                             data['user'], data['friends'])

    else:
        return HttpResponse('CSFS?')


# Still have problem
def renrencallback(request):
    exchange_url = (
        'https://graph.renren.com/oauth/authorize'
        '?response_type=code'
        '&code=' + request.GET.get('code')
        + '&redirect_uri=http://127.0.0.1:8001/renren_callback'
        '&client_id=229108'
        '&client_secret=8815838e95504011a18673ea9f37f3b4'
        '&scope=read_user_album+read_user_feed'
    )

    r = requests.post(exchange_url)
    return HttpResponse(r.text)
    print r.text
    access_token = r.json()['access_token']
    print access_token

    return redirect('/close_window/')  # HttpResponse(response)


def weibocallback(request):
    if request.GET.get('state', '') == request.session.get('state', '***'):
        exchange_url = (
            'https://api.weibo.com/oauth2/access_token'
            '?client_id=1736274547'
            '&client_secret=f6f8fa98288e0cb75d9fe291f14c33eb'
            '&grant_type=authorization_code'
            '&code=' + request.GET.get('code')
            + '&redirect_uri=http://127.0.0.1:8001/weibo_callback'
        )
        r = requests.post(exchange_url)
        access_token = r.json()['access_token']
        uid = str(r.json()['uid'])

        me_url = (
            'https://api.weibo.com/2/users/show.json'
            '?uid=3216837074' + uid
            + '&access_token=' + access_token
        )
        me = requests.get(me_url).json()

        friends_url = (
            'https://api.weibo.com/2/friendships/friends.json'
            '?uid=' + uid
            + '&count=200'
            '&access_token=' + access_token
        )
        friends = requests.get(friends_url).json()['users']

        client_id = 'weibo#' + uid
        return store_session(request, 'weibo', client_id,
                             access_token, me, friends)

    else:
        return HttpResponse('CSFS?')


def oauth2callback(request):
    return HttpResponse(request.GET.get('code'))


def close_window(request, is_reload=False):
    url = 'window.opener.document.location.href'
    reload_line = 'window.opener.document.location.href = %s;' % url \
        if is_reload else ''
    html = '''<script type="text/javascript">
           %swindow.close();</script>''' % reload_line
    return HttpResponse(html)


def logout_user(request):
    logout(request)
    response = redirect('close_window_reload')
    response.delete_cookie('user_location')
    return response


@ratelimit(rate='20/m')
def getqrcode(request):
    if request.method == 'GET':
        return HttpResponseBadRequest('Noooone')

    elif getattr(request, 'limited', False):
        # Reach rate limit
        return HttpResponseBadRequest(
            _('Was_limited: we are poor, cannot afford server cost. '
              'Donate some and we can buy more server time'))

    elif request.method == 'POST' and request.is_ajax():

        form = QueryForm(request.POST, session=request.session)
        if not form.is_valid():
            return HttpResponseBadRequest(json.dumps(form.errors))

        text = form.data['text']
        error_correct = form.data['error_correct_choice']
        channel_choice = form.data.getlist('channel_choice', [])
        options = {}
        # Convert string 'rgb(x,x,x)' --> tuple (x,x,x)
        options['color'] = tuple(map(
            lambda x: int(x),
            re.findall(r'\b\d+\b', form.data.get('color', 'rgb(0, 0, 0)'))))
        print options['color']
        try:
            qr = qrcode.QRCode(
                version=None,
                error_correction=getattr(qrcode.constants, error_correct),
                box_size=25,
                border=1,
                users=channel_choice,
                options=options,
            )
            qr.add_data(text)
            qr.make(fit=True)

            img = qr.make_image()
            filename = unique_generator() + '.png'
            img.save(os.path.join(MEDIA_ROOT + '/qrcode', filename))

            query = Query(text=text)
            query.save()

            photo = QRCode(
                query=query,
                text=text,
                photo=File(
                    open(os.path.join(MEDIA_ROOT + '/qrcode', filename), 'rb')
                )
            )
            photo.save()

            return HttpResponse(
                Template('<img src="{{ MEDIA_URL }}{{ photo.photo.url }}" '
                         'width="480" height="480" />').render(photo=photo)
            )

#            return HttpResponse('<img src="/media/qrcode/%s" '
#                                'width="480" height="480" />' % filename)

        except IndexError, e:
            return HttpResponse(e)


@ratelimit(rate='20/m')
@transaction.commit_on_success
def getfriendsrequest(request):
    if request.method == 'GET':
        return HttpResponse('Geeeet')

    elif getattr(request, 'limited', False):
        # Reach rate limit
        return HttpResponseBadRequest(
            _('Was_limited: we are poor, cannot afford server cost. '
              'Donate some and we can buy more server time'))

    elif request.method == 'POST' and request.is_ajax() \
            and 'import' in request.POST:
        html = ''
        for client_id in request.session[request.POST['import']]:
            if client_id in request.session:
                data = request.session.pop(client_id)
                getfriends(data, True)

                html += client_id \
                    + '\n' + json.dumps(data['user']) + ' has ' \
                    + str(len(data['friends'])) + '\n\n'
        return HttpResponse(html)


@task(ignore_result=True)
def getfriendstask(data):
    getfriends(data, True)


def getfriends(data, cache_image=False):
    channel = data['meta']['channel']
    channel_id = str(data['user'].get('id', None)
                     or data['user'].get('uid', None))

    if channel == 'facebook':
        first_name = data['user']['first_name']
        last_name = data['user']['last_name']
        username = data['user']['username']

    elif channel == 'google':
        first_name = data['user']['name']['givenName']
        last_name = data['user']['name']['familyName']
        username = data['user']['displayName']

    elif channel == 'linkedin':
        first_name = data['user']['firstName']
        last_name = data['user']['lastName']
        username = first_name + ' ' + last_name

    elif channel == 'kaixin001':
        first_name = ''
        last_name = ''
        username = data['user']['name']

    elif channel == 'twitter':
        first_name = ''
        last_name = ''
        username = data['user']['username']

    userclient, created = UserClient.objects.get_or_create(
        client=channel + '#' + channel_id,
    )
    userclient.username = username
    userclient.first_name = first_name
    userclient.last_name = last_name
    userclient.friends = data['friends']
    userclient.access_token = data['meta']['access_token']

    if channel == 'facebook':
        profile_picture_url = data['user'].get('pic_square', None)
    elif channel == 'google':
        profile_picture_url = data['user']['image']['url'] \
            if 'image' in data['user'] else None
    elif channel == 'linkedin':
        profile_picture_url = data['user'].get('pictureUrl', None)
    elif channel == 'kaixin001':
        profile_picture_url = data['user'].get('logo50', None)
    elif channel == 'twitter':
        profile_picture_url = data['user']['profile_image_url']
    else:
        profile_picture_url = None

    userclient.profile_picture_url = profile_picture_url
    userclient.save()

    if cache_image:
        if profile_picture_url:
            cachedimage, created = CachedImage.objects.get_or_create(
                url=profile_picture_url)
            cachedimage.cache_and_save()

        frd_cachedimage = userclient.cachedimage_set.values_list('url',
                                                                 flat=True)
        # Caching friend's profile picture
        for frd in data['friends']:
            if channel == 'facebook':
                profile_picture_url = frd.get('pic_square', None)
            elif channel == 'google':
                profile_picture_url = frd['image']['url'] \
                    if 'image' in frd else None
            elif channel == 'linkedin':
                profile_picture_url = frd.get('pictureUrl', None)
            elif channel == 'kaixin001':
                profile_picture_url = frd.get('logo50', None)
            elif channel == 'twitter':
                profile_picture_url = None
                # TODO: complicated get
            else:
                profile_picture_url = None

            if profile_picture_url \
                    and profile_picture_url not in frd_cachedimage:
                cachedimage, created = CachedImage.objects.get_or_create(
                    url=profile_picture_url)
                # cachedimage = CachedImage(url=url)
                cachedimage.user = userclient
                cachedimage.cache_and_save()


@task(ignore_result=True)
def add(x, y):
    return x + y
