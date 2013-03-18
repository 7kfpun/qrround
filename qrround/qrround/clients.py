from rauth import OAuth1Service, OAuth2Service
from oauth2client.client import OAuth2WebServerFlow  # for google


twitter = OAuth1Service(
    consumer_key='2Icic6DEGROMML9U3Xrrg',
    consumer_secret='2T4a3MpeqGSgOAehVrpm6hIO7ymf88XNabZgdZi7M',
    name='twitter',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize',
    request_token_url='https://api.twitter.com/oauth/request_token',
    base_url='https://api.twitter.com/1/'
)

facebook = OAuth2Service(
    client_id='236929692994329',
    client_secret='9d65f7d0069567d6958f559ad918ada7',
    name='facebook',
    authorize_url='https://graph.facebook.com/oauth/authorize',
    access_token_url='https://graph.facebook.com/oauth/access_token',
    base_url='https://graph.facebook.com/'
)

linkedin = OAuth2Service(
    client_id='2ykkt7cjhrcg',
    client_secret='TV7x10lw1JY6Zfe2',
    name='linkedin',
    authorize_url='https://www.linkedin.com/uas/oauth2/authorization',
    access_token_url='https://www.linkedin.com/uas/oauth2/accessToken',
    base_url='https://api.linkedin.com/v1/'
)

renren = OAuth2Service(
    client_id='229108',
    client_secret='8815838e95504011a18673ea9f37f3b4',
    name='renren',
    authorize_url='https://graph.renren.com/oauth/authorize',
    access_token_url='https://graph.renren.com/oauth/authorize',
    base_url='https://api.linkedin.com/v1/'
)

# google_auth_url = (
#     'https://accounts.google.com/o/oauth2/auth?'
#     'scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email'
#     '+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile'
#     '&redirect_uri=http://127.0.0.1:8001/google_callback&response_type=code'  # noqa
#     '&client_id=533974579689-j6h3lt2toobuok26n9o5g3n0qo0k2mbm.apps.googleusercontent.com'  # noqa
# )

# params = {
#     'scope': 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email',  # noqa
#     'response_type': 'code',
#     'redirect_uri': 'http://127.0.0.1:8001/google_callback'
# }
# google_auth_url = google.get_authorize_url(**params)

google = OAuth2WebServerFlow(
    client_id='533974579689-j6h3lt2toobuok26n9o5g3n0qo0k2mbm.apps.googleusercontent.com',  # noqa
    client_secret='dtLZ9z-AGhid6knEOC54qudr',
    scope='https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/plus.login https://www.googleapis.com/auth/plus.me',  # noqa
    redirect_uri='http://127.0.0.1:8001/google_callback',
    state='@@@@@@@@@@@@@@@@@@@@'
)
