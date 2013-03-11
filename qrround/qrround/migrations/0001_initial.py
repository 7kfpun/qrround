# -*- coding: utf-8 -*-
# flake8:noqa
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserClient'
        db.create_table(u'qrround_userclient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('client', self.gf('django.db.models.fields.CharField')(max_length=200, unique=True, null=True, blank=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('profile_picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('profile_picture_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'qrround', ['UserClient'])

        # Adding model 'Friend'
        db.create_table(u'qrround_friend', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qrround.UserClient'])),
            ('client', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('profile_picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('profile_picture_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'qrround', ['Friend'])

        # Adding model 'Query'
        db.create_table(u'qrround_query', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qrround.UserClient'], null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('colour', self.gf('django.db.models.fields.CharField')(default='#000000', max_length=10, null=True, blank=True)),
        ))
        db.send_create_signal(u'qrround', ['Query'])

        # Adding model 'QRCode'
        db.create_table(u'qrround_qrcode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('query', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qrround.Query'])),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'qrround', ['QRCode'])

        # Adding model 'CachedImage'
        db.create_table(u'qrround_cachedimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'qrround', ['CachedImage'])

        # Adding model 'TestQuery'
        db.create_table(u'qrround_testquery', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('query', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('test_field', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('year_in_school', self.gf('django.db.models.fields.CharField')(default='FR', max_length=2)),
            ('colour', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'qrround', ['TestQuery'])


    def backwards(self, orm):
        # Deleting model 'UserClient'
        db.delete_table(u'qrround_userclient')

        # Deleting model 'Friend'
        db.delete_table(u'qrround_friend')

        # Deleting model 'Query'
        db.delete_table(u'qrround_query')

        # Deleting model 'QRCode'
        db.delete_table(u'qrround_qrcode')

        # Deleting model 'CachedImage'
        db.delete_table(u'qrround_cachedimage')

        # Deleting model 'TestQuery'
        db.delete_table(u'qrround_testquery')


    models = {
        u'qrround.cachedimage': {
            'Meta': {'object_name': 'CachedImage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'qrround.friend': {
            'Meta': {'object_name': 'Friend'},
            'client': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'profile_picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'profile_picture_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qrround.UserClient']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'qrround.qrcode': {
            'Meta': {'object_name': 'QRCode'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'query': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qrround.Query']"})
        },
        u'qrround.query': {
            'Meta': {'object_name': 'Query'},
            'colour': ('django.db.models.fields.CharField', [], {'default': "'#000000'", 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qrround.UserClient']", 'null': 'True', 'blank': 'True'})
        },
        u'qrround.testquery': {
            'Meta': {'object_name': 'TestQuery'},
            'colour': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'test_field': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'year_in_school': ('django.db.models.fields.CharField', [], {'default': "'FR'", 'max_length': '2'})
        },
        u'qrround.userclient': {
            'Meta': {'object_name': 'UserClient'},
            'client': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'profile_picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'profile_picture_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['qrround']
