# flake8:noqa
FACEBOOK_CLIENT_ID = '236929692994329'
FACEBOOK_CLIENT_SECRET = '9d65f7d0069567d6958f559ad918ada7'

local = True
dotcloud = False

if local:
    FACEBOOK_REDIRECT_URI = 'http://127.0.0.1:8001/facebook_callback'

    GOOGLE_CLIENT_ID = '533974579689-j6h3lt2toobuok26n9o5g3n0qo0k2mbm.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = 'dtLZ9z-AGhid6knEOC54qudr'
    GOOGLE_REDIRECT_URI 'http://127.0.0.1:8001/google_callback'

    LINKEDIN_CLIENT_ID = '2ykkt7cjhrcg'
    LINKEDIN_CLIENT_SECRET = 'TV7x10lw1JY6Zfe2'
    LINKEDIN_REDIRECT_URI = 'http://127.0.0.1:8001/linkedin_callback'


else:
    FACEBOOK_REDIRECT_URI = 'http://qrround-710kfpun.dotcloud.com/facebook_callback'

    GOOGLE_CLIENT_ID = '533974579689.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = 'OJyFy0XPYsjtkuq6R7TBcILn'
    GOOGLE_REDIRECT_URI 'http://qrround-710kfpun.dotcloud.com/google_callback'

    LINKEDIN_CLIENT_ID = 'l22w31c7kwzf'
    LINKEDIN_CLIENT_SECRET = 'hJ8GiEDxcLZnVkUS'
    LINKEDIN_REDIRECT_URI = 'http://qrround-710kfpun.dotcloud.com/linkedin_callback'
