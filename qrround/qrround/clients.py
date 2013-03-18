from oauth2client.client import OAuth2WebServerFlow  # for google
from rauth import OAuth2Service
import tweepy


facebook = OAuth2Service(
    client_id='236929692994329',
    client_secret='9d65f7d0069567d6958f559ad918ada7',
    name='facebook',
    authorize_url='https://graph.facebook.com/oauth/authorize',
    access_token_url='https://graph.facebook.com/oauth/access_token',
    base_url='https://graph.facebook.com/',
)

google = OAuth2WebServerFlow(
    client_id='533974579689-j6h3lt2toobuok26n9o5g3n0qo0k2mbm.apps.googleusercontent.com',  # noqa
    client_secret='dtLZ9z-AGhid6knEOC54qudr',
    scope='https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/plus.login https://www.googleapis.com/auth/plus.me',  # noqa
    redirect_uri='http://127.0.0.1:8001/google_callback',
)

linkedin = OAuth2Service(
    client_id='2ykkt7cjhrcg',
    client_secret='TV7x10lw1JY6Zfe2',
    name='linkedin',
    authorize_url='https://www.linkedin.com/uas/oauth2/authorization',
    access_token_url='https://www.linkedin.com/uas/oauth2/accessToken',
    base_url='https://api.linkedin.com/v1/',
)

renren = OAuth2Service(
    client_id='229108',
    client_secret='8815838e95504011a18673ea9f37f3b4',
    name='renren',
    authorize_url='https://graph.renren.com/oauth/authorize',
    access_token_url='https://graph.renren.com/oauth/authorize',
    base_url='https://api.linkedin.com/v1/',
)

twitter = tweepy.OAuthHandler(
    consumer_key="2Icic6DEGROMML9U3Xrrg",
    consumer_secret="2T4a3MpeqGSgOAehVrpm6hIO7ymf88XNabZgdZi7M",
)

weibo = OAuth2Service(
    client_id='1736274547',
    client_secret='f6f8fa98288e0cb75d9fe291f14c33eb',
    name='weibo',
    authorize_url='https://api.weibo.com/oauth2/authorize',
    access_token_url='https://api.weibo.com/oauth2/access_token',
    base_url='https://api.weibo.com/2/',
)
# POST  https://api.weibo.com/2/statuses/update.json?access_token=2.00wQWhVDL1OVtB1375cc41d6BUNfYB status=status  # noqa
