from oauth2client.client import OAuth2WebServerFlow  # for google
from rauth import OAuth2Service
import tweepy

from .channels_settings import *  # noqa


channels = ['facebook', 'google', 'linkedin',
            'renren', 'twitter', 'weibo', 'kaixin001']

facebook = OAuth2Service(
    client_id=FACEBOOK_CLIENT_ID,
    client_secret=FACEBOOK_CLIENT_SECRET,
    name='facebook',
    authorize_url='https://graph.facebook.com/oauth/authorize',
    access_token_url='https://graph.facebook.com/oauth/access_token',
    base_url='https://graph.facebook.com/',
)

google = OAuth2WebServerFlow(
    client_id=GOOGLE_CLIENT_ID,  # noqa
    client_secret=GOOGLE_CLIENT_SECRET,
    scope='https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/plus.login https://www.googleapis.com/auth/plus.me',  # noqa
    redirect_uri=GOOGLE_REDIRECT_URI,
)

linkedin = OAuth2Service(
    client_id=LINKEDIN_CLIENT_ID,
    client_secret=LINKEDIN_CLIENT_SECRET,
    name='linkedin',
    authorize_url='https://www.linkedin.com/uas/oauth2/authorization',
    access_token_url='https://www.linkedin.com/uas/oauth2/accessToken',
    base_url='https://api.linkedin.com/v1/',
)

renren = OAuth2Service(
    client_id=RENREN_CLIENT_ID,
    client_secret=RENREN_CLIENT_SECRET,
    name='renren',
    authorize_url='https://graph.renren.com/oauth/authorize',
    access_token_url='https://graph.renren.com/oauth/authorize',
    base_url='https://api.linkedin.com/v1/',
)

twitter = tweepy.OAuthHandler(
    consumer_key=TWITTER_CONSUMER_KEY,
    consumer_secret=TWITTER_CONSUMER_SECRET,
)

weibo = OAuth2Service(
    client_id=WEIBO_CLIENT_ID,
    client_secret=WEIBO_CLIENT_SECRET,
    name='weibo',
    authorize_url='https://api.weibo.com/oauth2/authorize',
    access_token_url='https://api.weibo.com/oauth2/access_token',
    base_url='https://api.weibo.com/2/',
)
# POST  https://api.weibo.com/2/statuses/update.json?access_token=2.00wQWhVDL1OVtB1375cc41d6BUNfYB status=status  # noqa

kaixin001 = OAuth2Service(
    client_id=KAIXIN001_CLIENT_ID,
    client_secret=KAIXIN001_CLIENT_SECRET,
    name='weibo',
    authorize_url='http://api.kaixin001.com/oauth2/authorize',
    access_token_url='https://api.kaixin001.com/oauth2/access_token',
    base_url='https://api.weibo.com/2/',
)
