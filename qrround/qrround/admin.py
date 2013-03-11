from django.contrib import admin
from qrround.models import (
    UserClient,
    Friend,
    QRCode,
    Query,
)


class UserClientAdmin(admin.ModelAdmin):
    list_display = ('client',
                    'is_active', 'is_admin',
                    'last_login', 'date_joined',
                    'username', 'first_name', 'last_name', 'email',
                    'profile_picture', 'profile_picture_url', 'url',)


class FriendAdmin(admin.ModelAdmin):
    list_display = ('user', 'client',
                    'username', 'first_name', 'last_name', 'email',
                    'profile_picture', 'profile_picture_url', 'url',)


class QueryProfileAdmin(admin.ModelAdmin):
    list_display = ('text',)


class QRCodeAdmin(admin.ModelAdmin):
    list_display = ('text', 'photo', 'photo_thumbnail',)


admin.site.register(UserClient, UserClientAdmin)
admin.site.register(Friend, FriendAdmin)
admin.site.register(Query, QueryProfileAdmin)
admin.site.register(QRCode, QRCodeAdmin)
