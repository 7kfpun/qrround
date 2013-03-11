import datetime
from django.contrib.auth.models import User
from django.core.files import File
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
import os
from settings.settings import MEDIA_ROOT
import urllib


class UserClient(models.Model):
    user = models.OneToOneField(User)

    client = models.CharField(max_length=200, blank=True, null=True)
    client_id = models.CharField(max_length=200, blank=True, null=True)

    profile_picture = models.ImageField(
        upload_to='profile_picture',
        blank=True,
        null=True,
    )
    profile_picture_url = models.URLField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    class Meta:
        unique_together = (("client", "client_id"),)

    def __unicode__(self):  
          return "%s's UserClient" % self.user


class Friend(models.Model):
    user = models.ForeignKey(UserClient)

    client_id = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    profile_picture = models.ImageField(
        upload_to='profile_picture',
        blank=True,
        null=True,
    )
    profile_picture_url = models.URLField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __unicode__(self):  
          return "%s's Friend" % self.username

    @property
    def client(self):
        return self.user.client


class Query(models.Model):
    user = models.ForeignKey(UserClient, blank=True, null=True)

    text = models.CharField(max_length=200, blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)

    # Options
    colour = models.CharField(max_length=10, default='#000000',
                              blank=True, null=True)

    def __unicode__(self):  
          return self.text


class QRCode(models.Model):
    query = models.ForeignKey(Query)

    photo = models.ImageField(
        upload_to='qrcode/%Y/%m/%d',
        blank=True
    )
    photo_thumbnail = ImageSpecField(
        image_field='photo',
        processors=[ResizeToFit(480, 480)],
        format='JPEG',
        options={'quality': 60}
    )

    def __unicode__(self):
        return self.query.text


# No need
class CachedImage(models.Model):

    url = models.CharField(max_length=255, unique=True)
    photo = models.ImageField(
        upload_to='cachedimages/%Y/%m/%d',
        blank=True
    )
    photo_thumbnail = ImageSpecField(
        image_field='photo',
        processors=[ResizeToFit(50, 50)],
        format='JPG',
        options={'quality': 60}
    )

    def cache(self):
        """Store image locally if we have a URL"""
        if self.url and not self.photo:
            result = urllib.urlretrieve(self.url)
            self.photo.save(
                os.path.basename(self.url), 
                File(open(result[0], 'rb')),
                save=False,
            )
            self.save()

    def __unicode__(self):
        return self.url


class TestQuery(models.Model):
    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'
    YEAR_IN_SCHOOL_CHOICES = (
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
    )

    query = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    test_field = models.CharField(max_length=200)
    year_in_school = models.CharField(max_length=2,
                                      choices=YEAR_IN_SCHOOL_CHOICES,
                                      default=FRESHMAN)
    colour = models.CharField(max_length=10)
    photo = models.ImageField(upload_to='/'.join([MEDIA_ROOT, 'phtotos']),
                              blank=True)

    def __unicode__(self):  
          return self.query
