from django.contrib import admin
from django.contrib.auth.models import User
from qrround.models import (
    UserProfile,
    Query,
)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['test_field', 'user']
    fields = ['test_field', 'user']
    

class QueryProfileAdmin(admin.ModelAdmin):
    list_display = Query._meta.get_all_field_names()
    fields = ['query', 'test_field', 'year_in_school']


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Query, QueryProfileAdmin)
