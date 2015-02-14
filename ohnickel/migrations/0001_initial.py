# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table(u'ohnickel_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.TextField')(default='')),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('jointed_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'ohnickel', ['User'])

        # Adding model 'Forum'
        db.create_table(u'ohnickel_forum', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')(default='')),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='forums', to=orm['ohnickel.User'])),
            ('sticky', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'ohnickel', ['Forum'])

        # Adding model 'Thread'
        db.create_table(u'ohnickel_thread', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('forum', self.gf('django.db.models.fields.related.ForeignKey')(related_name='threads', to=orm['ohnickel.Forum'])),
            ('name', self.gf('django.db.models.fields.TextField')(default='')),
            ('views', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='threads', to=orm['ohnickel.User'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'ohnickel', ['Thread'])

        # Adding model 'Post'
        db.create_table(u'ohnickel_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('thread', self.gf('django.db.models.fields.related.ForeignKey')(related_name='posts', to=orm['ohnickel.Thread'])),
            ('name', self.gf('django.db.models.fields.TextField')(default='')),
            ('text', self.gf('django.db.models.fields.TextField')(default='')),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='posts', to=orm['ohnickel.User'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'ohnickel', ['Post'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'ohnickel_user')

        # Deleting model 'Forum'
        db.delete_table(u'ohnickel_forum')

        # Deleting model 'Thread'
        db.delete_table(u'ohnickel_thread')

        # Deleting model 'Post'
        db.delete_table(u'ohnickel_post')


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'jointed_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'username': ('django.db.models.fields.TextField', [], {'default': "''"})
        }
    }

    complete_apps = ['ohnickel']