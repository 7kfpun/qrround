from django.core.files import File
from django.db import transaction
from django.http import HttpResponse
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

    google_auth_url = (
        'https://accounts.google.com/o/oauth2/auth?'
        'scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email'
        '+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile'
        '&redirect_uri=http://127.0.0.1:8001/oauth2callback&response_type=code'
        '&client_id=533974579689.apps.googleusercontent.com'
    )

    linkedin_auth_url = (
        'https://www.linkedin.com/uas/oauth2/authorization?response_type=code'
        '&client_id=2ykkt7cjhrcg'
        '&scope=r_basicprofile%20r_emailaddress%20r_network'
        '&state=STATE'
        '&redirect_uri=http://127.0.0.1:8001/'
    )

#    if request.GET.get('oauth_verifier'):
#        verifier = request.GET.get('oauth_verifier')
#
#        try:
#            auth.get_access_token(verifier)
#        except tweepy.TweepError:
#            logger.error('Error! Failed to get access token.')

    return render(request, 'index.html', {
        'google_auth_url': google_auth_url,
        'twitter_auth_url': None,
        'linkedin_auth_url': linkedin_auth_url,
    })


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
                box_size=10,
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


def oauth2callback(request):
    return HttpResponse(request.GET.get('code'))


@transaction.commit_on_success
def getfriends(request):
    data = None
    if request.method == 'GET':
        pass

    elif request.method == 'POST' and request.is_ajax():

        data = json.loads(request.body)

        channel = data['meta']['channel']
        channel_id = data['user']['id']

        if channel == 'linkedin':
            first_name = data['user']['firstName']
            last_name = data['user']['lastName']
            username = first_name + ' ' + last_name

        elif channel == 'facebook':
            first_name = data['user']['first_name']
            last_name = data['user']['last_name']
            username = data['user']['username']

        elif channel == 'google+':
            first_name = data['user']['name']['givenName']
            last_name = data['user']['name']['familyName']
            username = data['user']['displayName']

        userclient, created = UserClient.objects.get_or_create(
            client=channel + '#' + channel_id,
        )
        userclient.username = username
        userclient.first_name = first_name
        userclient.last_name = last_name
        userclient.friends = data["friends"]
        userclient.save()

        for frd in data["friends"]:

            if channel == 'linkedin':
                url = frd.get("pictureUrl", None)
            elif channel == 'facebook':
                url = frd.get("pic_square", None)
            elif channel == 'google+':
                url = frd["image"]["url"] if "image" in frd else None
            else:
                url = None

            if url:
                cachedimage, created = CachedImage.objects.get_or_create(
                    url=url)
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
