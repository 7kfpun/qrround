from django.contrib.auth.models import User
from django.db import models
import datetime
from settings.settings import MEDIA_ROOT
import urllib
import os
from django.core.files import File
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit


class UserProfile(models.Model):  
    user = models.OneToOneField(User)  
    test_field = models.CharField(max_length=200)

    def __unicode__(self):  
          return "%s's profile" % self.user


class CachedImage(models.Model):
    reporter = models.ForeignKey(UserProfile)
    url = models.CharField(max_length=255, unique=True)
    photo = models.ImageField(
        upload_to='cachedimages/%Y/%m/%d',
        blank=True
    )
    photo_thumbnail = ImageSpecField(
        image_field='photo',
        processors=[ResizeToFit(500, 500)],
        format='JPEG',
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


class Query(models.Model):
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
