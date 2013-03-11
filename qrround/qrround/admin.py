from django.contrib import admin
from django.contrib.auth.models import User
from qrround.models import (
    UserClient,
    Friend,
    QRCode,
    Query,
)


class UserClientAdmin(admin.ModelAdmin):
    list_display = ['user', 'client', 'client_id']
    fields = ['user', 'client', 'client_id']
    

class QueryProfileAdmin(admin.ModelAdmin):
    list_display = ['text']
    fields = ['text']


admin.site.register(UserClient, UserClientAdmin)
admin.site.register(Query, QueryProfileAdmin)
