# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Volunteer.cell_phone'
        db.add_column('volunteer_dispatcher_volunteer', 'cell_phone',
                      self.gf('phonenumber_field.modelfields.PhoneNumberField')(max_length=128, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Volunteer.work_phone'
        db.add_column('volunteer_dispatcher_volunteer', 'work_phone',
                      self.gf('phonenumber_field.modelfields.PhoneNumberField')(max_length=128, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Volunteer.home_phone'
        db.add_column('volunteer_dispatcher_volunteer', 'home_phone',
                      self.gf('phonenumber_field.modelfields.PhoneNumberField')(max_length=128, null=True, blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'Volunteer.cell_phone'
        db.delete_column('volunteer_dispatcher_volunteer', 'cell_phone')

        # Deleting field 'Volunteer.work_phone'
        db.delete_column('volunteer_dispatcher_volunteer', 'work_phone')

        # Deleting field 'Volunteer.home_phone'
        db.delete_column('volunteer_dispatcher_volunteer', 'home_phone')

    models = {
        'volunteer_dispatcher.incident': {
            'Meta': {'object_name': 'Incident'},
            'addr1': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'addr2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'addr3': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'dispatcher_initial_description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'incident_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['volunteer_dispatcher.IncidentType']"}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'volunteer_dispatcher.incidenttype': {
            'Meta': {'object_name': 'IncidentType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'volunteer_dispatcher.volunteer': {
            'Meta': {'object_name': 'Volunteer'},
            'addr1': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'addr2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'addr3': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'cell_phone': ('phonenumber_field.modelfields.PhoneNumberField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'home_phone': ('phonenumber_field.modelfields.PhoneNumberField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'work_phone': ('phonenumber_field.modelfields.PhoneNumberField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['volunteer_dispatcher']