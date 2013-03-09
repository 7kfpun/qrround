from django.http import HttpResponse
from django.shortcuts import render
import json
import tweepy
from settings.settings import TEMPLATE_DIRS, STATICFILES_DIRS

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

def getqrcode(request):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        print dir(request)
        print request.body
        data = json.loads(request.body)
        print len(data)

    return HttpResponse("Get qr code")

def oauth2callback(request):
    return HttpResponse(request.GET.get('code'))

