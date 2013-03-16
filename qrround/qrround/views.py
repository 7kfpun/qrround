from django.core.files import File
from django.db import transaction
from django.http import HttpResponse  # , HttpResponseRedirect
from django.shortcuts import render  # , get_object_or_404
from django.template import Context, Template
from helpers import unique_generator
import json
import logging
import os
import qrcode
from qrround.models import (
    UserClient,
    # Friend,
    QRCode,
    Query,
    CachedImage,
)
from ratelimit.decorators import ratelimit
from rauth import OAuth1Service, OAuth2Service
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

    facebook = OAuth2Service(
        client_id='236929692994329',
        client_secret='9d65f7d0069567d6958f559ad918ada7',
        name='facebook',
        authorize_url='https://graph.facebook.com/oauth/authorize',
        access_token_url='https://graph.facebook.com/oauth/access_token',
        base_url='https://graph.facebook.com/')
    redirect_uri = 'http://127.0.0.1:8001/facebook_callback'
    params = {'scope': 'read_stream,publish_actions',
              'response_type': 'code',
              'redirect_uri': redirect_uri}

    facebook_auth_url = facebook.get_authorize_url(**params)

    facebook_auth_url = (
        'https://www.facebook.com/dialog/oauth/?'
        'client_id=236929692994329'
        '&redirect_uri=http://127.0.0.1:8001/facebook_callback'
        '&state=STATE'
        '&scope=read_stream,publish_actions'
    )

    twitter = OAuth1Service(
        consumer_key='2Icic6DEGROMML9U3Xrrg',
        consumer_secret='2T4a3MpeqGSgOAehVrpm6hIO7ymf88XNabZgdZi7M',
        name='twitter',
        access_token_url='https://api.twitter.com/oauth/access_token',
        authorize_url='https://api.twitter.com/oauth/authorize',
        request_token_url='https://api.twitter.com/oauth/request_token',
        base_url='https://api.twitter.com/1/'
    )
    request_token = twitter.get_request_token()[0]

    twitter_auth_url = twitter.get_authorize_url(
        request_token,
        callback_url='http://127.0.0.1:8001/twitter_callback'
    )

    google_auth_url = (
        'https://accounts.google.com/o/oauth2/auth?'
        'scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email'
        '+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile'
        '&redirect_uri=http://127.0.0.1:8001/google_callback&response_type=code'  # noqa
        '&client_id=533974579689-j6h3lt2toobuok26n9o5g3n0qo0k2mbm.apps.googleusercontent.com'  # noqa
    )

    linkedin_auth_url = (
        'https://www.linkedin.com/uas/oauth2/authorization?response_type=code'
        '&client_id=2ykkt7cjhrcg'
        '&scope=r_basicprofile%20r_emailaddress%20r_network'
        '&state=STATE'
        '&redirect_uri=http://127.0.0.1:8001/linkedin_callback'
    )

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
    })


def facebookcallback(request):
    response = HttpResponse('facebook_auth_session:' + json.dumps(request.GET))
    response.set_cookie('facebook_auth_session',
                        request.GET.get('code'), max_age=1000)
    return response


def googlecallback(request):
    response = HttpResponse('google_auth_session:' + json.dumps(request.GET))
    response.set_cookie('google_auth_session',
                        request.GET.get('code'), max_age=1000)
    return response


def linkedincallback(request):
    response = HttpResponse('linkedin_auth_session:' + json.dumps(request.GET))
    response.set_cookie('linkedin_auth_session',
                        request.GET.get('code'), max_age=1000)
    return response


def twittercallback(request):
    response = HttpResponse('twitter_auth_session:' + json.dumps(request.GET))
    response.set_cookie('twitter_auth_session',
                        request.GET.get('oauth_token'), max_age=1000)
    return response


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
        return HttpResponse('Noooone')

    elif getattr(request, 'limited', False):
        return HttpResponse('Was_limited')

    elif request.method == 'POST' and request.is_ajax():
        text = request.POST.get('text')
        if len(text) > 1000:
            return HttpResponse('Text is too long')

        try:
            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=25,
                border=1,
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
                         'width="480" height="480" />').
                render(Context({'photo': photo}))
            )

#            return HttpResponse('<img src="/media/qrcode/%s" '
#                                'width="480" height="480" />' % filename)

        except IndexError, e:
            return HttpResponse(e)


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
