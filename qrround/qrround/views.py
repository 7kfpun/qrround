from django.http import HttpResponse
from django.shortcuts import render
import json
import tweepy


CONSUMER_TOKEN = "2Icic6DEGROMML9U3Xrrg"
CONSUMER_SECRET = "2T4a3MpeqGSgOAehVrpm6hIO7ymf88XNabZgdZi7M"


def index(request):
    try:
        auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
        auth_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print 'Error! Failed to get request token.'
    
    if request.GET.get('oauth_verifier'):
        verifier = request.GET.get('oauth_verifier')

        try:
            auth.get_access_token(verifier)
        except tweepy.TweepError:
            print 'Error! Failed to get access token.'
        
        # api = tweepy.API(auth)
        # api.update_status('tweepy + oauth!')

    return render(request, 'index.html', {
        'auth_url': auth_url,
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
