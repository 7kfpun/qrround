from celery import task
from django.contrib.auth import logout
from django.core.files import File
from django.db import transaction
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
)
from django.shortcuts import redirect, render   # , get_object_or_404
# from django.template import Context, Template
from django.utils.translation import ugettext_lazy as _
# from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from jinja2 import Template
import json
import logging
import os
from ratelimit.decorators import ratelimit
import re
import requests
from settings.settings import MEDIA_ROOT, PROJECT_NAME_TEST  # TODO: real NAME
from time import time
import tweepy
from urllib import urlencode

import qrcode
from .channels import *  # noqa
from .channels_settings import *  # noqa
from .forms import ContactForm, QueryForm
from .helpers import unique_generator
from .models import (
    CachedImage,
    Contact,
    UserClient,
    Query,
    QRCode,
)


logger = logging.getLogger(__name__)


def login(request):
    if request.method == 'POST':
        pass
    return render(request, 'login.html')


def index(request):
    get = request.GET.get('get', '')

    return render(request, 'index.html', {
        'qrcode': QRCode.objects.get(
            photo__contains='/%s.' % get) if get else '',
        'form': QueryForm(session=request.session),
        'contact_form': ContactForm(),
    })


def sendcontact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = Contact(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                topic=form.cleaned_data['topic'],
                message=form.cleaned_data['message'],
            )
            contact.save()
            return HttpResponse('{"success": 1}')
        else:
            return HttpResponseBadRequest(json.dumps(form.errors))
    else:
        return redirect('/')


def getgallery(request):
    all_clients = [client for channel in channels
                   for client in request.session.get(channel, [])]
    return render(request, 'gallery.html', {
        'qrcodes': QRCode.objects.filter(
            query__user__client__in=all_clients).order_by('-pk')[:12]})


def postfacebookphotos(request):
    posts = []
    for client in request.session.get('facebook', []):
        user = UserClient.objects.get(client=client)
        """ # Share to feed
        url = 'https://graph.facebook.com/%s/feed' % user.client.split('#')[1]
        data = {
            'access_token': user.access_token,
            'message': PROJECT_NAME_TEST,
            'caption': PROJECT_NAME_TEST,
            'type': 'photo',
            'picture': 'http://img.photobucket.com/albums/v317/phillycrazy/blog/ZhangXuan.jpg',  # user.profile_picture_url,  # noqa
            'link': 'http://img.photobucket.com/albums/v317/phillycrazy/blog/ZhangXuan.jpg',  # user.profile_picture_url,  # noqa
        }
        r = requests.post(url, urlencode(data))
        posts.append(r.json()['id'])
        """

        if user.album_id:
            album_id = user.album_id
        else:
            url = 'https://graph.facebook.com/%s/albums' \
                % user.client.split('#')[1]
            data = {
                'access_token': user.access_token,
                'name': PROJECT_NAME_TEST,
                'message': PROJECT_NAME_TEST,
            }
            r = requests.post(url, urlencode(data))
            album_id = r.json()['id']
            user.album_id = r.json()['id']
            user.save()

        url = 'https://graph.facebook.com/%s/photos' % album_id
        data = {
            'access_token': user.access_token,
            'message': PROJECT_NAME_TEST,
        }
        r = requests.post(
            url, data=data,
            files={'source': open('ZhangXuan.jpg', 'rb')})
        posts.append(r.text)

#     Refresh token
#     https://graph.facebook.com/oauth/access_token?
#     client_id=APP_ID&
#     client_secret=APP_SECRET&
#     grant_type=fb_exchange_token&
#     fb_exchange_token=EXISTING_ACCESS_TOKEN

    return HttpResponse('\n'.join(posts))


# ssl connection needed
def postkaixin001photos(request):
    posts = []
    for client in request.session.get('kaixin001', []):
        user = UserClient.objects.get(client=client)

        if user.album_id:
            album_id = user.album_id
        else:
            url = 'https://api.kaixin001.com/album/create.json'
            data = {
                'access_token': user.access_token,
                'title': PROJECT_NAME_TEST,
                'description': PROJECT_NAME_TEST,
            }
            r = requests.post(url, urlencode(data))
            return HttpResponse(r.text)
            album_id = r.json()['albumid']
            user.album_id = r.json()['albumid']
            user.save()

        url = 'https://api.kaixin001.com/photo/upload.json'
        data = {
            'access_token': user.access_token,
            'albumid': album_id,
            'title': PROJECT_NAME_TEST,
        }
        r = requests.post(
            url, data=data,
            files={'pic': open('ZhangXuan.jpg', 'rb')})
        posts.append(r.text)

    return HttpResponse('\n'.join(posts))


@ratelimit(rate='40/m')
def getauthurls(request):
    if getattr(request, 'limited', False):
        # Reach rate limit
        return HttpResponseBadRequest(
            _('We are poor, cannot afford too much server cost. '
              'Donate us so that we can buy more server time<br />'
              'Try agains after seconds please...'))

    elif True:  # and request.is_ajax():
        state = request.session['state'] = str(time())[:-3]

        # facebook
        params = {
            'scope': 'read_stream,publish_actions,publish_stream,user_photos',
            'response_type': 'code',
            'state': state,
            'redirect_uri': FACEBOOK_REDIRECT_URI,
        }
        facebook_auth_url = facebook.get_authorize_url(**params)

        # google
        google.params.update({'state': state})
        google_auth_url = google.step1_get_authorize_url()

        # kaixin001
        params = {
            'scope': 'create_album',
            'response_type': 'code',
            'state': state,
            'redirect_uri': KAIXIN001_REDIRECT_URI,
        }
        kaixin001_auth_url = kaixin001.get_authorize_url(**params)

        # linkedin
        params = {
            'scope': 'r_basicprofile r_emailaddress r_network rw_nus',
            'response_type': 'code',
            'state': state,
            'redirect_uri': LINKEDIN_REDIRECT_URI,
        }
        linkedin_auth_url = linkedin.get_authorize_url(**params)

        # renren
        params = {
            'response_type': 'code',
            'state': state,
            'redirect_uri': RENREN_REDIRECT_URI,
        }
        renren_auth_url = renren.get_authorize_url(**params)

#         try:
#             twitter.callback = "%(redirect_url)s?state=%(state)s" \
#                 % {'redirect_url': RENREN_REDIRECT_URI, 'state': state}
#             twitter_auth_url = twitter.get_authorization_url()
#         except tweepy.TweepError:
#             twitter_auth_url = None
#             logger.error('Error! Failed to get access token.')

        # weibo
        params = {
            'scope': 'email,direct_messages_write,friendships_groups_read',
            'state': state,
            'redirect_uri': WEIBO_REDIRECT_URI,
            'grant_type': 'authorization_code',
        }
        weibo_auth_url = weibo.get_authorize_url(**params)

        return render(request, 'auth_urls.html', {
            'facebook': facebook_auth_url,
            'google': google_auth_url,
            'kaixin001': kaixin001_auth_url,
            'linkedin': linkedin_auth_url,
            'renren': renren_auth_url,
            # 'twitter': twitter_auth_url,
            'weibo': weibo_auth_url,
        })


def store_session(request, channel, client_id, access_token, me, friends):
    data = {
        'meta': {
            'text': 'this is text',
            'method': 'text',
            'channel': channel,
            'access_token': access_token,
        },
        'user': me,
        'friends': friends,
    }

    if channel == 'facebook':
        first_name = data['user']['first_name']
        last_name = data['user']['last_name']
        username = data['user']['username']
        url = data['user']['profile_url'].replace('www.', '')

    elif channel == 'google':
        first_name = data['user']['name']['givenName']
        last_name = data['user']['name']['familyName']
        username = data['user']['displayName']
        url = data['user']['url']

    elif channel == 'linkedin':
        first_name = data['user']['firstName']
        last_name = data['user']['lastName']
        username = first_name + ' ' + last_name
        url = 'https://linkedin.com/e/fpf/' + str(data['user']['id'])

    elif channel == 'kaixin001':
        first_name = ''
        last_name = ''
        username = data['user']['name']
        url = 'http://kaixin001.com/home/?uid=' + str(data['user']['uid'])

    elif channel == 'twitter':
        first_name = ''
        last_name = ''
        username = data['user']['username']
        url = ''

    elif channel == 'weibo':
        first_name = ''
        last_name = ''
        username = data['user']['screen_name']
        url = ''

    logger.info('> Start create: ' + client_id)
    # Store user
    userclient, created = UserClient.objects.get_or_create(
        client=client_id,
    )
    logger.info('> Created: ' + client_id)
    userclient.username = username
    userclient.first_name = first_name
    userclient.last_name = last_name
    userclient.friends = data['friends']
    userclient.access_token = data['meta']['access_token']
    userclient.url = url

    if channel == 'facebook':
        profile_picture_url = data['user'].get('pic_square', None)
    elif channel == 'google':
        profile_picture_url = data['user']['image']['url'] \
            if 'image' in data['user'] else None
    elif channel == 'linkedin':
        profile_picture_url = data['user'].get('pictureUrl', None)
    elif channel == 'kaixin001':
        profile_picture_url = data['user'].get('logo50', None)
    elif channel == 'twitter' or channel == 'weibo':
        profile_picture_url = data['user']['profile_image_url']
    else:
        profile_picture_url = None

    userclient.profile_picture_url = profile_picture_url
    userclient.save()

    logger.info('> Saved and start saving session: ' + client_id)
    # Session store --> login
    if channel in request.session:
        tmp = request.session[channel]
        if client_id not in tmp:
            tmp.append(client_id)
        request.session[channel] = tmp
    else:
        request.session[channel] = [client_id]
    logger.info('> Call get frds: ' + client_id)

    # Async task for getting caced images for friends
    task = callgetfriends.apply_async([client_id])
    data['meta']['task'] = str(task)
    return HttpResponse(json.dumps(data))

    # response = redirect('close_window_reload')
    # response.delete_cookie('user_location')
    # return response


def facebookcallback(request):
    if request.GET.get('state', '') == request.session.get('state', '***'):
        session = facebook.get_auth_session(data={
            'code': request.GET.get('code'),
            'redirect_uri': FACEBOOK_REDIRECT_URI})
        access_token = session.access_token

        # me = session.get('me').json()
        # to get pic_square of me()
        me = session.get(
            'fql?q=SELECT uid, first_name, middle_name,'
            + ' last_name, username, name, pic_square, profile_url'
            + ' FROM user WHERE uid = me()').json()['data'][0]

        friends = session.get(
            'fql?q=SELECT uid, first_name, middle_name,'
            + ' last_name, username, name, pic_square, profile_url'
            + ' FROM user WHERE uid in (SELECT uid2 FROM friend'
            + ' WHERE uid1 = me())').json()['data']

        client_id = 'facebook#' + str(me['uid'])
        return store_session(request, 'facebook', client_id,
                             access_token, me, friends)

    else:
        return HttpResponse('CSRF?')


# Still have problem
def googlecallback(request):
    if request.GET.get('state', '') == request.session.get('state', '***'):
        credentials = google.step2_exchange(request.GET.get('code'))
        access_token = credentials.access_token

        me_url = (
            'https://www.googleapis.com/plus/v1/people/me'
            '?access_token=' + access_token
        )
        me = requests.get(me_url).json()

        friends_url = (
            'https://www.googleapis.com/plus/v1/people/me/people/visible'
            '?access_token=' + access_token
        )
        friends = requests.get(friends_url).json()['items']

        client_id = 'google#' + str(me['id'])
        return store_session(request, 'google', client_id,
                             access_token, me, friends)

    else:
        return HttpResponse('CSRF?')


def kaixin001callback(request):
    if request.GET.get('state', '') == request.session.get('state', '***'):
        exchange_url = (
            'https://api.kaixin001.com/oauth2/access_token'
            '?grant_type=authorization_code'
            '&code=' + request.GET.get('code')
            + '&client_id=' + KAIXIN001_CLIENT_ID
            + '&client_secret=' + KAIXIN001_CLIENT_SECRET
            + '&redirect_uri=' + KAIXIN001_REDIRECT_URI
        )
        r = requests.get(exchange_url)
        try:
            access_token = r.json()['access_token']
            logger.info('> access_token: ' + access_token)

            me_url = (
                'https://api.kaixin001.com/users/me.json'
                '?access_token=' + access_token
            )
            me = requests.get(me_url).json()

            friends_url = (
                'https://api.kaixin001.com/friends/me.json'
                '?num=50'
                '&access_token=' + access_token
            )
            friends = requests.get(friends_url).json()['users']

            client_id = 'kaixin001#' + str(me['uid'])
            logger.info('> store_session: ' + client_id)
            return store_session(request, 'kaixin001', client_id,
                                 access_token, me, friends)
        except KeyError, e:
            return HttpResponse(str(e) + r.text)

    else:
        return HttpResponse('CSRF?')


def linkedincallback(request):
    if request.GET.get('state', '') == request.session.get('state', '***'):
        exchange_url = (
            'https://www.linkedin.com/uas/oauth2/accessToken'
            '?grant_type=authorization_code'
            '&code=' + request.GET.get('code')
            + '&redirect_uri=' + LINKEDIN_REDIRECT_URI
            + '&client_id=' + LINKEDIN_CLIENT_ID
            + '&client_secret=' + LINKEDIN_CLIENT_SECRET + ''
        )
        r = requests.post(exchange_url)
        try:
            access_token = r.json()['access_token']

            me_url = (
                'https://api.linkedin.com/v1/people/~'
                ':(id,first-name,last-name,headline,picture-url)'
                '?oauth2_access_token=' + access_token + '&format=json'
            )
            me = requests.get(me_url).json()

            try:
                friends_url = (
                    'https://api.linkedin.com/v1/people/~/connections'
                    '?oauth2_access_token=' + access_token + '&format=json')
                friends = requests.get(friends_url).json()['values']
            except KeyError:
                friends = []

            client_id = 'linkedin#' + str(me['id'])
            return store_session(request, 'linkedin', client_id,
                                 access_token, me, friends)
        except KeyError, e:
            return HttpResponse(str(e) + r.text)

    else:
        return HttpResponse('CSRF?')


def twittercallback(request):
    if request.GET.get('state', '') == request.session.get('state', '***'):
        verifier = request.GET.get('oauth_verifier')
        try:
            twitter.get_access_token(verifier)
        except tweepy.TweepError:
            print 'Error! Failed to get access token.'
            return HttpResponseNotFound('Failed to get access token')

        twitter.set_access_token(twitter.access_token.key,
                                 twitter.access_token.secret)
        api = tweepy.API(twitter)
        me = api.me()  # <object>

        friends = api.friends_ids()

#        import jsonpickle
#        me = jsonpickle.encode(me)
#        return HttpResponse(me)

        data = {
            'meta': {
                'text': 'this is text',
                'method': 'text',
                'channel': 'twitter',
            },
            'user': {
                'id': me.id_str,
                'username': me.name,
                'screen_name': me.screen_name,
                'lang': me.lang,
                'url': me.url,
                'location': me.location,
                'time_zone': me.time_zone,
                'profile_image_url': me.profile_image_url,
                'profile_image_url_https': me.profile_image_url_https,
                'profile_background_image_url': me.profile_background_image_url,  # noqa
                'profile_background_image_url_https': me.profile_background_image_url_https,  # noqa
            },
            'friends': [{'id': str(friend)} for friend in friends],
        }

        client_id = 'twitter#' + me.id_str
        return store_session(request, 'twitter', client_id,
                             data['user'], data['friends'])

    else:
        return HttpResponse('CSRF?')


# Still have problem
def renrencallback(request):
    exchange_url = (
        'https://graph.renren.com/oauth/authorize'
        '?response_type=code'
        '&code=' + request.GET.get('code')
        + '&redirect_uri=' + RENREN_REDIRECT_URI
        + '&client_id=' + RENREN_CLIENT_ID
        + '&client_secret=' + RENREN_CLIENT_SECRET
        + '&scope=read_user_album+read_user_feed'
    )

    r = requests.post(exchange_url)
    return HttpResponse(r.text)
    print r.text
    access_token = r.json()['access_token']
    print access_token

    return redirect('/close_window/')  # HttpResponse(response)


def weibocallback(request):
    if request.GET.get('state', '') == request.session.get('state', '***'):
        exchange_url = (
            'https://api.weibo.com/oauth2/access_token'
            '?client_id=' + WEIBO_CLIENT_ID
            + '&client_secret=' + WEIBO_CLIENT_SECRET
            + '&grant_type=authorization_code'
            '&code=' + request.GET.get('code')
            + '&redirect_uri=' + WEIBO_REDIRECT_URI
        )
        r = requests.post(exchange_url)
        access_token = r.json()['access_token']
        uid = str(r.json()['uid'])

        me_url = (
            'https://api.weibo.com/2/users/show.json'
            '?uid=' + uid
            + '&access_token=' + access_token
        )
        me = requests.get(me_url).json()

        friends_url = (
            'https://api.weibo.com/2/friendships/friends.json'
            '?uid=' + uid
            + '&count=200'
            '&access_token=' + access_token
        )
        friends = requests.get(friends_url).json()['users']

        client_id = 'weibo#' + uid
        return store_session(request, 'weibo', client_id,
                             access_token, me, friends)

    else:
        return HttpResponse('CSRF?')


def close_window(request, is_reload=False):
    url = 'window.opener.document.location.href'
    reload_line = 'window.opener.document.location.href = %s;' % url \
        if is_reload else ''
    html = '''<script type="text/javascript">
           %swindow.close();</script>''' % reload_line
    return HttpResponse(html)


def logout_user(request):
    logout(request)
    response = redirect('close_window_reload')
    response.delete_cookie('user_location')
    return response


@ratelimit(rate='20/m')
def getqrcode(request):
    if request.method == 'GET':
        return HttpResponseBadRequest('Noooone')

    elif getattr(request, 'limited', False):
        # Reach rate limit
        return HttpResponseBadRequest(
            _('Was_limited: we are poor, cannot afford server cost. '
              'Donate some and we can buy more server time'))

    elif request.method == 'POST' and request.is_ajax():

        form = QueryForm(request.POST, session=request.session)
        if not form.is_valid():
            return HttpResponseBadRequest(json.dumps(form.errors))

        text = form.data['text']
        error_correct = form.data['error_correct_choice']
        channel_choice = form.data.getlist('channel_choice', [])
        options = {}
        # Convert string 'rgb(x,x,x)' --> tuple (x,x,x)
        options['color'] = tuple(map(
            lambda x: int(x),
            re.findall(r'\b\d+\b', form.data.get('color', 'rgb(0, 0, 0)'))))
        options['style'] = form.data.get('style', '0')

        try:
            qr = qrcode.QRCode(
                version=None,
                error_correction=getattr(qrcode.constants, error_correct),
                box_size=25,
                border=1,
                users=channel_choice,
                options=options,
            )
            qr.add_data(text)
            qr.make(fit=True)

            img = qr.make_image()
            filename = unique_generator() + '.png'
            img.save(os.path.join(MEDIA_ROOT + '/qrcode', filename))

            query = Query(
                text=text,
                user=UserClient.objects.get(client=channel_choice[0])
            )
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
                Template(
                    '<img src="{{ MEDIA_URL }}{{ photo.photo_jpg.url }}" '
                    'width="480" height="480" />').render(photo=photo)
            )

        except IndexError, e:
            return HttpResponse(e)


@csrf_exempt
@transaction.commit_on_success
def getfriendsrequest(request):
    if request.method == 'GET':
        return HttpResponse('Geeeet')

    elif getattr(request, 'limited', False):
        # Reach rate limit
        return HttpResponseBadRequest(
            _('Was_limited: we are poor, cannot afford server cost. '
              'Donate some and we can buy more server time'))

    # and request.is_ajax()
    elif request.method == 'POST' and 'import' in request.POST:
        client_id = request.POST['import']
        friends_data = UserClient.objects.get(client=client_id).friends

        print '>>>>>>>>>>>>>', client_id

        getfriendstask(client_id, True)

        html = client_id + ' has v ' + str(len(friends_data)) + '\n'
        logger.info('Finished get friends: %s' % html)
        return HttpResponse(html)


@task(ignore_result=True, max_retries=3, default_retry_delay=10, priority=5)
def callgetfriends(import_=None):
    r = requests.post('%sgetfriends' % SITE_URL,
                      data={'import': import_})
    print r.text[:7000]


# @task(ignore_result=True, max_retries=3, default_retry_delay=10, priority=5)
@transaction.commit_on_success
def getfriendstask(client_id, cache_image=False):
    userclient = UserClient.objects.get(client=client_id)
    channel = userclient.client.split('#')[0]

    print '>>>>>>>>>>>>>', client_id, channel

    if userclient.profile_picture_url:
        cachedimage, created = CachedImage.objects.get_or_create(
            user=userclient,
            url=userclient.profile_picture_url
        )
        cachedimage.cache_and_save()

    if cache_image:
        frd_cachedimage = userclient.cachedimage_set.values_list(
            'url', flat=True)

        # Caching friend's profile picture
        for frd in UserClient.objects.get(client=client_id).friends:
            logger.info(frd)

            if channel == 'facebook':
                profile_picture_url = frd.get('pic_square', None)
            elif channel == 'google':
                profile_picture_url = frd['image']['url'] \
                    if 'image' in frd else None
            elif channel == 'linkedin':
                profile_picture_url = frd.get('pictureUrl', None)
            elif channel == 'kaixin001':
                profile_picture_url = frd.get('logo50', None)
            elif channel == 'weibo':
                profile_picture_url = frd.get('profile_image_url', None)
            elif channel == 'twitter':
                profile_picture_url = None
                # TODO: complicated get
            else:
                profile_picture_url = None

            if profile_picture_url \
                    and profile_picture_url not in frd_cachedimage:
                cachedimage, created = CachedImage.objects.get_or_create(
                    url=profile_picture_url)
                # cachedimage = CachedImage(url=url)
                cachedimage.user = userclient
                cachedimage.cache_and_save()

    return 'Succesfull'


def testtasks(request):
    x = int(request.GET.get('x', '1'))
    y = int(request.GET.get('y', '2'))
    t = add.apply_async([x, y])
    return HttpResponse(t.get())


@task(ignore_result=True, max_retries=3, default_retry_delay=10, priority=5)
def add(x, y):
    return x + y
