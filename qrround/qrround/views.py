from celery import task
from django.core.files import File
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render   # , get_object_or_404
# from django.template import Context, Template
from forms import QueryForm
from helpers import unique_generator
from jinja2 import Template
import json
import logging
import os
import qrcode
from qrround.clients import facebook, google, linkedin, renren, twitter
from qrround.models import (
    UserClient,
    # Friend,
    QRCode,
    Query,
    CachedImage,
)
from ratelimit.decorators import ratelimit
import requests
from settings.settings import MEDIA_ROOT
#import StringIO
#import tweepy


#CONSUMER_TOKEN = "2Icic6DEGROMML9U3Xrrg"
#CONSUMER_SECRET = "2T4a3MpeqGSgOAehVrpm6hIO7ymf88XNabZgdZi7M"

logger = logging.getLogger(__name__)


def index(request):
#    try:
#        twitter_auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
#        twitter_auth_url = twitter_auth.get_authorization_url()
#    except tweepy.TweepError:
#        twitter_auth_url = None
#        logger.error('Error! Failed to get request token.')

    # Protect against Cross-Site Request Forgery
    # STATE = 'YOUR_STATE_VALUEYOUR_STATE_VALUEYOUR_STATE_VALUE'

    state = request.session['state'] = unique_generator(32)

    params = {
        'scope': 'read_stream,publish_actions',
        'response_type': 'code',
        'state': state,
        'redirect_uri': 'http://127.0.0.1:8001/facebook_callback'}
    facebook_auth_url = facebook.get_authorize_url(**params)

#    facebook_auth_url = (
#        'https://www.facebook.com/dialog/oauth/?'
#        'client_id=236929692994329'
#        '&redirect_uri=http://127.0.0.1:8001/facebook_callback'
#        '&state=STATE'
#        '&scope=read_stream,publish_actions'
#    )

    request_token = twitter.get_request_token()[0]
    twitter_auth_url = twitter.get_authorize_url(
        request_token,
        callback_url='http://127.0.0.1:8001/twitter_callback'
    )
    # twitter_auth_url = None

    google_auth_url = (
        'https://accounts.google.com/o/oauth2/auth?'
        'scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email'
        '+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile'
        '&redirect_uri=http://127.0.0.1:8001/google_callback&response_type=code'  # noqa
        '&client_id=533974579689-j6h3lt2toobuok26n9o5g3n0qo0k2mbm.apps.googleusercontent.com'  # noqa
    )

    params = {
        'scope': 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email',  # noqa
        'response_type': 'code',
        'redirect_uri': 'http://127.0.0.1:8001/google_callback'
    }
    google_auth_url = google.get_authorize_url(**params)

    linkedin_auth_url = (
        'https://www.linkedin.com/uas/oauth2/authorization?response_type=code'
        '&client_id=2ykkt7cjhrcg'
        '&scope=r_basicprofile%20r_emailaddress%20r_network'
        '&state=STATE'
        '&redirect_uri=http://127.0.0.1:8001/linkedin_callback'
    )

    params = {
        'scope': 'r_basicprofile r_emailaddress r_network',
        'response_type': 'code',
        'state': state,
        'redirect_uri': 'http://127.0.0.1:8001/linkedin_callback',
    }
    linkedin_auth_url = linkedin.get_authorize_url(**params)

    params = {
        'response_type': 'code',
        'state': state,
        'redirect_uri': 'http://127.0.0.1:8001/renren_callback',
    }
    renren_auth_url = renren.get_authorize_url(**params)

#    if request.GET.get('oauth_verifier'):
#        verifier = request.GET.get('oauth_verifier')
#
#        try:
#            auth.get_access_token(verifier)
#        except tweepy.TweepError:
#            logger.error('Error! Failed to get access token.')

    return render(request, 'index.html', {
        'facebook_auth_url': facebook_auth_url,
        'google_auth_url': google_auth_url,
        'linkedin_auth_url': linkedin_auth_url,
        'twitter_auth_url': twitter_auth_url,
        'renren_auth_url': renren_auth_url,
        'form': QueryForm(session=request.session),
        'session': request.session.keys(),
    })


def facebookcallback(request):
    if request.GET.get('state') == request.session['state']:
        session = facebook.get_auth_session(data={
            'code': request.GET.get('code'),
            'redirect_uri': 'http://127.0.0.1:8001/facebook_callback'})

        me = session.get('me').json()
        friends = session.get(
            'fql?q=SELECT uid, first_name, middle_name,'
            + ' last_name, username, name, pic_square, profile_url'
            + ' FROM user WHERE uid in (SELECT uid2 FROM friend'
            + ' WHERE uid1 = me())').json()['data']

        request.session['facebook_id'] = 'facebook#' + str(me['id'])
        data = {
            "meta": {
                "text": "this is text",
                "method": "text",
                "channel": "facebook",
            },
            "user": me,
            "friends": friends,
        }
        data

#        response = HttpResponse(
#            'facebook_auth_session:' + json.dumps(request.GET)
#            + '<br /><br /><br />' + json.dumps(me)
#            + '<br /><br /><br />' + json.dumps(friends)
#        )
#        response.set_cookie('facebook_auth_session',
#                            request.GET.get('code'), max_age=1000)
#        return HttpResponse(response)

        return redirect('/close_window/')
    else:
        return HttpResponse('CSFS?')


# Still have problem
def googlecallback(request):
    response = HttpResponse('google_auth_session:' + json.dumps(request.GET))
    response.set_cookie('google_auth_session',
                        request.GET.get('code'), max_age=1000)

#    session = google.get_auth_session(data={
#        'code': request.GET.get('code'),
#        'data-type': 'jsonp',
#        'redirect_uri': 'http://127.0.0.1:8001/google_callback'})

    exchange_url = (
        'https://accounts.google.com/o/oauth2/token?'
        'code=' + request.GET.get('code') + '&redirect_uri=http://127.0.0.1:8001/google_callback'  # noqa
        '&client_id=533974579689-j6h3lt2toobuok26n9o5g3n0qo0k2mbm.apps.googleusercontent.com'  # noqa
        '&client_secret=dtLZ9z-AGhid6knEOC54qudr'
        '&grant_type=authorization_code'
    )
    print exchange_url
    r = requests.post(exchange_url)
    print r.json()

    #print session.get('userinfo').json()
    return response


def linkedincallback(request):
    if request.GET.get('state') == request.session['state']:

        exchange_url = (
            'https://www.linkedin.com/uas/oauth2/accessToken'
            '?grant_type=authorization_code'
            '&code=' + request.GET.get('code') + '&redirect_uri=http://127.0.0.1:8001/linkedin_callback'  # noqa
            '&client_id=2ykkt7cjhrcg'
            '&client_secret=TV7x10lw1JY6Zfe2'
        )
        r = requests.post(exchange_url)
        access_token = r.json()['access_token']

        me_url = (
            'https://api.linkedin.com/v1/people/~'
            ':(id,first-name,last-name,headline,picture-url)'
            '?oauth2_access_token=' + access_token + '&format=json'
        )
        me = requests.get(me_url).json()

        friends_url = (
            'https://api.linkedin.com/v1/people/~/connections'
            '?oauth2_access_token=' + access_token + '&format=json')
        friends = requests.get(friends_url).json()['values']

        request.session['linkedin_id'] = 'linkedin#' + str(me['id'])
        data = {
            "meta": {
                "text": "this is text",
                "method": "text",
                "channel": "linkedin",
            },
            "user": me,
            "friends": friends,
        }
        data = data

#        response = HttpResponse(
#            'linkedin_auth_session:' + json.dumps(request.GET)
#            + '<br /><br /><br />' + json.dumps(r.json())
#            + '<br /><br /><br />' + json.dumps(me)
#            + '<br /><br /><br />' + json.dumps(friends)
#        )
#        response.set_cookie('linkedin_auth_session',
#                            request.GET.get('code'), max_age=1000)
#
#        return HttpResponse(response)

        return redirect('/close_window/')
    else:
        return HttpResponse('CSFS?')


def twittercallback(request):
    response = HttpResponse('twitter_auth_session:' + json.dumps(request.GET))
    response.set_cookie('twitter_auth_session',
                        request.GET.get('oauth_token'), max_age=1000)

    print '#### get_request_token', twitter.get_request_token()
    request_token = twitter.get_request_token()[0]
    authorization_url = twitter.get_authorize_url(request_token)
    print '#### authorization_url', authorization_url
    # session = twitter.get_auth_session(request_token, request_token_secret)

    return response


# Still have problem
def renrencallback(request):
    exchange_url = (
        'https://graph.renren.com/oauth/authorize'
        '?response_type=code'
        '&code=' + request.GET.get('code') + '&redirect_uri=http://127.0.0.1:8001/renren_callback'  # noqa
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


def oauth2callback(request):
    return HttpResponse(request.GET.get('code'))


def close_window(request, is_reload=False):
    url = "window.opener.document.location.href"
    reload_line = "window.opener.document.location.href = %s;" % url \
        if is_reload else ""
    html = '''<script type="text/javascript">
           %swindow.close();</script>''' % reload_line
    return HttpResponse(html)


@ratelimit(rate='20/m')
def getqrcode(request):

    if request.method == 'GET':
        return HttpResponseBadRequest('Noooone')

    elif getattr(request, 'limited', False):
        # Reach rate limit
        return HttpResponseBadRequest('Was_limited')

    elif request.method == 'POST' and request.is_ajax():

        form = QueryForm(request.POST, session=request.session)
        if not form.is_valid():
            return HttpResponseBadRequest(json.dumps(form.errors))

        text = form.data['text']
        error_correct = form.data['error_correct_choice']
        channel_choice = form.data.getlist('channel_choice', [])

        print form.data
        try:
            qr = qrcode.QRCode(
                version=None,
                error_correction=getattr(qrcode.constants, error_correct),
                box_size=25,
                border=1,
                users=channel_choice,
            )
            qr.add_data(text)
            qr.make(fit=True)

            img = qr.make_image()
            filename = '.'.join([unique_generator(), 'png'])
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
                Template('<img src="{{ photo.photo.url }}" '
                         'width="480" height="480" />').render(photo=photo)
            )

#            return HttpResponse('<img src="/media/qrcode/%s" '
#                                'width="480" height="480" />' % filename)

        except IndexError, e:
            return HttpResponse(e)


@task(ignore_result=True)
@ratelimit(rate='20/m')
@transaction.commit_on_success
def getfriends(request):
    data = None
    if request.method == 'GET':
        pass

    elif request.method == 'POST' and request.is_ajax():

        data = json.loads(request.body)

        channel = data['meta']['channel']
        channel_id = data['user']['id']

        if channel == 'facebook':
            first_name = data['user']['first_name']
            last_name = data['user']['last_name']
            username = data['user']['username']

        elif channel == 'google+':
            first_name = data['user']['name']['givenName']
            last_name = data['user']['name']['familyName']
            username = data['user']['displayName']

        elif channel == 'linkedin':
            first_name = data['user']['firstName']
            last_name = data['user']['lastName']
            username = first_name + ' ' + last_name

        userclient, created = UserClient.objects.get_or_create(
            client=channel + '#' + channel_id,
        )
        userclient.username = username
        userclient.first_name = first_name
        userclient.last_name = last_name
        userclient.friends = data["friends"]
        userclient.save()

        if channel == 'facebook':
            url = data['user'].get("pic_square", None)
        elif channel == 'google+':
            url = data['user']["image"]["url"] \
                if "image" in data['user'] else None
        elif channel == 'linkedin':
            url = data['user'].get("pictureUrl", None)
        else:
            url = None

        if url:
            cachedimage, created = CachedImage.objects.get_or_create(
                url=url)
            cachedimage.cache_and_save()

        frd_cachedimage = userclient.cachedimage_set.values_list('url',
                                                                 flat=True)
        # Caching friend's profile picture
        for frd in data["friends"]:

            if channel == 'facebook':
                url = frd.get("pic_square", None)
            elif channel == 'google+':
                url = frd["image"]["url"] if "image" in frd else None
            elif channel == 'linkedin':
                url = frd.get("pictureUrl", None)
            else:
                url = None

            if url and url not in frd_cachedimage:
                cachedimage, created = CachedImage.objects.get_or_create(
                    url=url)
                # cachedimage = CachedImage(url=url)
                cachedimage.user = userclient
                cachedimage.cache_and_save()

#            username = filter(
#                lambda x: x in data["user"], [
#                    "firstName", "displayName", "username"
#                    # LinkedIn   Google+        Facebook
#                ])[0] or None
#            first_name = filter(
#                lambda x: x in data["user"], [
#                    "firstName", "name", "first_name"
#                    # LinkedIn   Google+        Facebook
#                ])[0] or None
#            last_name = filter(
#                lambda x: x in data["user"], [
#                    "lastName", "name", "last_name"
#                    # LinkedIn   Google+        Facebook
#                ])[0] or None

#            frd_channel = data["meta"]["channel"]
#            frd_channel_id = str(frd["id"] if "id" in frd else frd["uid"])
#            friend, created = Friend.objects.get_or_create(
#                user=userclient,
#                client=frd_channel + '#' + frd_channel_id,
#            )
#            friend.save()

    return HttpResponse(
        channel + '#' + channel_id + '\n'
        + username + " has " + str(len(data["friends"]))
    )


@task(ignore_result=True)
def add(x, y):
    return x + y
