# -*- coding: utf-8 -*-
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.files import File
from django.db import models
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFit
from jsonfield import JSONField
import os
# from settings.settings import MEDIA_ROOT
import urllib
import caching.base


class UserClientManager(BaseUserManager):
    def create_user(self, client, password=None):
        if not client:
            raise ValueError('Users must have a client')

        user = self.model(client=client)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, client, password):
        user = self.create_user(
            client,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserClient(AbstractBaseUser):
    objects = UserClientManager()

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    client = models.CharField(db_index=True, max_length=200, unique=True,
                              blank=True, null=True)

    username = models.CharField(max_length=200, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    profile_picture = models.ImageField(
        max_length=255,
        upload_to='profile_picture',
        blank=True,
        null=True,
    )
    profile_picture_url = models.URLField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    friends = JSONField(blank=True, null=True)

    access_token = models.CharField(max_length=255, blank=True, null=True)
    album_id = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'client'

    def __unicode__(self):
        return "%s's UserClient" % self.client

    def get_full_name(self):
        return self.client

    def get_short_name(self):
        return self.client

    def has_perm(self, perm, obj=None):
        # Handle whether the user has a specific permission?"
        return True

    def has_module_perms(self, app_label):
        # Handle whether the user has permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        # Handle whether the user is a member of staff?"
        return self.is_admin


class Friend(models.Model):
    user = models.ForeignKey(UserClient)

    client = models.CharField(max_length=200, unique=True,
                              blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    profile_picture = models.ImageField(
        max_length=255,
        upload_to='profile_picture',
        blank=True,
        null=True,
    )
    profile_picture_url = models.URLField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __unicode__(self):
        return "%s's Friend" % self.username


class Query(models.Model):
    user = models.ForeignKey(UserClient, blank=True, null=True)

    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Options
    colour = models.CharField(max_length=10, default='#000000',
                              blank=True, null=True)

    def __unicode__(self):
        return self.text

    @property
    def client(self):
        return self.user.client


class QRCode(caching.base.CachingMixin, models.Model):
    query = models.ForeignKey(Query)

    photo = ProcessedImageField(
        max_length=255,
        upload_to='qrcode',
        processors=[ResizeToFit(1500, 1500)],
        format='JPEG',
        options={'quality': 70})

    photo_thumbnail = ImageSpecField(
        image_field='photo',
        processors=[ResizeToFit(100, 100)],
        format='JPEG',
        options={'quality': 30},
    )

    # objects = caching.base.CachingManager()

    def __unicode__(self):
        return self.query.text

    @property
    def text(self):
        return self.query.text

    def save(self, *args, **kwargs):
        # TODO: add save thumbnail manually
        super(self.__class__, self).save(*args, **kwargs)


class CachedImage(caching.base.CachingMixin, models.Model):
    user = models.ForeignKey(UserClient, blank=True, null=True)

    url = models.URLField(db_index=True, unique=True)
    photo = models.ImageField(
        max_length=255,
        upload_to='cachedimages/%Y/%m/%d',
        blank=True
    )
    photo_thumbnail = ImageSpecField(
        image_field='photo',
        processors=[ResizeToFit(50, 50)],
        format='JPG',
        options={'quality': 60}
    )

    # objects = caching.base.CachingManager()

    def cache_and_save(self):
        """Store image locally if we have a URL"""
        if self.url and not self.photo:
            result = urllib.urlretrieve(self.url)
            self.photo.save(
                os.path.basename(self.url),
                File(open(result[0], 'rb')),
            )
        self.save()

    def __unicode__(self):
        return self.url


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    topic = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.email + ': ' + self.topic
