# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'User.last_login'
        db.alter_column(u'ohnickel_user', 'last_login', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):

        # Changing field 'User.last_login'
        db.alter_column(u'ohnickel_user', 'last_login', self.gf('django.db.models.fields.DateTimeField')(default=None))

    models = {
        u'ohnickel.forum': {
            'Meta': {'object_name': 'Forum'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'sticky': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'forums'", 'to': u"orm['ohnickel.User']"})
        },
        u'ohnickel.post': {
            'Meta': {'object_name': 'Post'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'text': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posts'", 'to': u"orm['ohnickel.Thread']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posts'", 'to': u"orm['ohnickel.User']"})
        },
        u'ohnickel.thread': {
            'Meta': {'object_name': 'Thread'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'threads'", 'to': u"orm['ohnickel.Forum']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'threads'", 'to': u"orm['ohnickel.User']"}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'ohnickel.user': {
            'Meta': {'object_name': 'User'},
            'email': ('django.db.models.fields.TextField', [], {'default': "''"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'jointed_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'uid': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'username': ('django.db.models.fields.TextField', [], {'default': "''"})
        }
    }

    complete_apps = ['ohnickel']