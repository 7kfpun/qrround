from rauth import OAuth1Service, OAuth2Service


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

google = OAuth2Service(
    client_id=('533974579689-j6h3lt2toobuok26n9o5g3n0qo0k2mbm'
               '.apps.googleusercontent.com'),
    client_secret='dtLZ9z-AGhid6knEOC54qudr',
    name='google',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    base_url='https://www.googleapis.com/plus/v1/'
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
