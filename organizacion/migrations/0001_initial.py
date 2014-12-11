# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Unidad'
        db.create_table(u'organizacion_unidad', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('descripcion', self.gf('django.db.models.fields.TextField')()),
            ('documento', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'organizacion', ['Unidad'])

        # Adding model 'Cargo'
        db.create_table(u'organizacion_cargo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('descripcion', self.gf('django.db.models.fields.TextField')()),
            ('documento', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('unidad', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['organizacion.Unidad'], null=True, blank=True)),
        ))
        db.send_create_signal(u'organizacion', ['Cargo'])

        # Adding model 'Planificacion'
        db.create_table(u'organizacion_planificacion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descripcion', self.gf('django.db.models.fields.TextField')()),
            ('cantidad', self.gf('django.db.models.fields.IntegerField')(default='1')),
            ('fecha_plani', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('estado', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('cargo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['organizacion.Cargo'])),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
        ))
        db.send_create_signal(u'organizacion', ['Planificacion'])


    def backwards(self, orm):
        # Deleting model 'Unidad'
        db.delete_table(u'organizacion_unidad')

        # Deleting model 'Cargo'
        db.delete_table(u'organizacion_cargo')

        # Deleting model 'Planificacion'
        db.delete_table(u'organizacion_planificacion')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'organizacion.cargo': {
            'Meta': {'ordering': "['unidad']", 'object_name': 'Cargo'},
            'descripcion': ('django.db.models.fields.TextField', [], {}),
            'documento': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'unidad': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['organizacion.Unidad']", 'null': 'True', 'blank': 'True'})
        },
        u'organizacion.planificacion': {
            'Meta': {'ordering': "['fecha_plani']", 'object_name': 'Planificacion'},
            'cantidad': ('django.db.models.fields.IntegerField', [], {'default': "'1'"}),
            'cargo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['organizacion.Cargo']"}),
            'descripcion': ('django.db.models.fields.TextField', [], {}),
            'estado': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'fecha_plani': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'organizacion.unidad': {
            'Meta': {'ordering': "['nombre']", 'object_name': 'Unidad'},
            'descripcion': ('django.db.models.fields.TextField', [], {}),
            'documento': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['organizacion']