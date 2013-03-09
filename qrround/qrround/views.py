from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import render
import json
import os
import qrcode
import random
from settings.settings import TEMPLATE_DIRS, STATICFILES_DIRS, MEDIA_ROOT
import string
import StringIO
import tweepy


CONSUMER_TOKEN = "2Icic6DEGROMML9U3Xrrg"
CONSUMER_SECRET = "2T4a3MpeqGSgOAehVrpm6hIO7ymf88XNabZgdZi7M"


def index(request):
    print 'TEMPLATE_DIRS', TEMPLATE_DIRS
    print 'STATICFILES_DIRS', STATICFILES_DIRS
    try:
        auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
        auth_url = auth.get_authorization_url()
    except tweepy.TweepError:
        auth_url = None
        print 'Error! Failed to get request token.'

    google_auth_url = (
        'https://accounts.google.com/o/oauth2/auth?'
        'scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email'
        '+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile'
        '&redirect_uri=http://127.0.0.1:8000/oauth2callback&response_type=code'
        '&client_id=533974579689.apps.googleusercontent.com'
    )

    linkedin_auth_url = (
        'https://www.linkedin.com/uas/oauth2/authorization?response_type=code'
        '&client_id=2ykkt7cjhrcg'
        '&scope=r_basicprofile%20r_emailaddress%20r_network'
        '&state=STATE'
        '&redirect_uri=http://127.0.0.1:8000/'
    )

    if request.GET.get('oauth_verifier'):
        verifier = request.GET.get('oauth_verifier')

        try:
            auth.get_access_token(verifier)
        except tweepy.TweepError:
            print 'Error! Failed to get access token.'
        
        # api = tweepy.API(auth)
        # api.update_status('tweepy + oauth!')

    return render(request, 'index.html', {
        'google_auth_url': google_auth_url,
        'twitter_auth_url': auth_url,
        'linkedin_auth_url': linkedin_auth_url,
    })


def getPic(request):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        print dir(request)
        print request.body
        data = json.loads(request.body)
        print len(data)

    return HttpResponse("ya")


def unique_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def getqrcode(request):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        text = request.POST.get('text')

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=100,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image()
        filename = '.'.join([unique_generator(), 'png'])
        img.save(os.path.join(MEDIA_ROOT, filename))
        # f = open(os.path.join(MEDIA_ROOT, 'hello.png'), 'wb+')
        # f.write(img)
        # File(f)
        # pilImage = open('/tmp/myfile.jpg','rb')

    return HttpResponse(filename)

def oauth2callback(request):
    return HttpResponse(request.GET.get('code'))

