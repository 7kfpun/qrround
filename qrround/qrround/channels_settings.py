# flake8:noqa
import os


if 'dotcloud' not in os.environ.get('PYTHONPATH', ''):
    
    FACEBOOK_CLIENT_ID = '236929692994329'
    FACEBOOK_CLIENT_SECRET = '9d65f7d0069567d6958f559ad918ada7'
    FACEBOOK_REDIRECT_URI = 'http://127.0.0.1:8001/facebook_callback'
    
    GOOGLE_CLIENT_ID = '533974579689-j6h3lt2toobuok26n9o5g3n0qo0k2mbm.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = 'dtLZ9z-AGhid6knEOC54qudr'
    GOOGLE_REDIRECT_URI = 'http://127.0.0.1:8001/google_callback'

    LINKEDIN_CLIENT_ID = '2ykkt7cjhrcg'
    LINKEDIN_CLIENT_SECRET = 'TV7x10lw1JY6Zfe2'
    LINKEDIN_REDIRECT_URI = 'http://127.0.0.1:8001/linkedin_callback'

    KAIXIN001_CLIENT_ID = '1214876808351987b5b2f5659b72f67c'
    KAIXIN001_CLIENT_SECRET = 'bf2726ad4eb6dc8e3c41fa6f9edf8ab3'
    KAIXIN001_REDIRECT_URI = 'http://127.0.0.1:8001/kaixin001_callback'

    WEIBO_CLIENT_ID = '1736274547'
    WEIBO_CLIENT_SECRET = 'f6f8fa98288e0cb75d9fe291f14c33eb'
    WEIBO_REDIRECT_URI = 'http://127.0.0.1:8001/weibo_callback'

else:

    FACEBOOK_CLIENT_ID = '450704555005617'
    FACEBOOK_CLIENT_SECRET = '6b17f7ea59856d82187a6981b17df0f0'
    FACEBOOK_REDIRECT_URI = 'http://qrround-710kfpun.dotcloud.com/facebook_callback'

    GOOGLE_CLIENT_ID = '533974579689.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = 'OJyFy0XPYsjtkuq6R7TBcILn'
    GOOGLE_REDIRECT_URI = 'http://qrround-710kfpun.dotcloud.com/google_callback'

    LINKEDIN_CLIENT_ID = 'l22w31c7kwzf'
    LINKEDIN_CLIENT_SECRET = 'hJ8GiEDxcLZnVkUS'
    LINKEDIN_REDIRECT_URI = 'http://qrround-710kfpun.dotcloud.com/linkedin_callback'

    KAIXIN001_CLIENT_ID = '1214876808351987b5b2f5659b72f67c'
    KAIXIN001_CLIENT_SECRET = 'bf2726ad4eb6dc8e3c41fa6f9edf8ab3'
    KAIXIN001_REDIRECT_URI = 'http://qrround-710kfpun.dotcloud.com/kaixin001_callback'

    WEIBO_CLIENT_ID = '1349178671'
    WEIBO_CLIENT_SECRET = 'e631a9f6eb562c6a9761431d74346c8d'
    WEIBO_REDIRECT_URI = 'http://qrround-710kfpun.dotcloud.com/weibo_callback'

RENREN_CLIENT_ID = '229108'
RENREN_CLIENT_SECRET = '8815838e95504011a18673ea9f37f3b4'
RENREN_REDIRECT_URI = 'http://127.0.0.1:8001/renren_callback'

TWITTER_CONSUMER_KEY = '2Icic6DEGROMML9U3Xrrg'
TWITTER_CONSUMER_SECRET = '2T4a3MpeqGSgOAehVrpm6hIO7ymf88XNabZgdZi7M'
