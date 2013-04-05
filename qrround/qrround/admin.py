# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import Group
from imagekit.admin import AdminThumbnail
from .models import (
    CachedImage,
    Contact,
    Friend,
    Query,
    QRCode,
    UserClient,
)


class CachedImageAdmin(admin.ModelAdmin):
    list_display = ('url', 'photo', 'photo_thumbnail',)
    photo_thumbnail = AdminThumbnail(image_field='photo')


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'topic', 'message', 'created_at')


class FriendAdmin(admin.ModelAdmin):
    list_display = ('user', 'client',
                    'username', 'first_name', 'last_name', 'email',
                    'profile_picture', 'profile_picture_url', 'url',)


class UserClientAdmin(admin.ModelAdmin):
    list_display = ('client', 'access_token', 'album_id',
                    'is_active', 'is_superuser', 'is_admin',
                    'last_login', 'date_joined',
                    'username', 'first_name', 'last_name', 'email',
                    'profile_picture', 'profile_picture_url', 'url',)
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class QueryProfileAdmin(admin.ModelAdmin):
    list_display = ('text', 'created_at')


class QRCodeAdmin(admin.ModelAdmin):
    list_display = ('text', 'photo', 'photo_thumbnail',)
    photo_thumbnail = AdminThumbnail(image_field='photo_thumbnail')


admin.site.register(CachedImage, CachedImageAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Friend, FriendAdmin)
admin.site.register(Query, QueryProfileAdmin)
admin.site.register(QRCode, QRCodeAdmin)
admin.site.register(UserClient, UserClientAdmin)
admin.site.unregister(Group)
