from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from jsonfield import JSONField
import os
from settings.settings import MEDIA_ROOT
import urllib


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
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    client = models.CharField(max_length=200, unique=True, db_index=True,
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
    created_time = models.DateTimeField(auto_now_add=True)

    # Options
    colour = models.CharField(max_length=10, default='#000000',
                              blank=True, null=True)

    def __unicode__(self):
        return self.text

    @property
    def client(self):
        return self.user.client


# CustomStorage
class CustomStorage(FileSystemStorage):

    def _open(self, name, mode='rb'):
        return File(open(self.path(name), mode))

    def _save(self, name, content):
        # here, you should implement how the file is to be saved
        # like on other machines or something, and return the name of the file.
        # In our case, we just return the name, and disable any kind of save
        return name.replace('_1', '').replace('_2', '').replace('_3', '')


def get_available_name(self, name):
    return name

custom_store = CustomStorage()
# EndCustomStorage


class QRCode(models.Model):
    query = models.ForeignKey(Query)

    photo = models.ImageField(
        max_length=255,
        storage=custom_store,
        upload_to='qrcode',
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

    @property
    def text(self):
        return self.query.text


class CachedImage(models.Model):
    user = models.ForeignKey(UserClient, blank=True, null=True)

    url = models.URLField(unique=True, db_index=True)
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
