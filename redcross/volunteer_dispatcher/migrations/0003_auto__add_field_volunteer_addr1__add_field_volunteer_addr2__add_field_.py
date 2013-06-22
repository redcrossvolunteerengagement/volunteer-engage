# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Volunteer.addr1'
        db.add_column('volunteer_dispatcher_volunteer', 'addr1',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Volunteer.addr2'
        db.add_column('volunteer_dispatcher_volunteer', 'addr2',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Volunteer.addr3'
        db.add_column('volunteer_dispatcher_volunteer', 'addr3',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Incident.addr1'
        db.add_column('volunteer_dispatcher_incident', 'addr1',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Incident.addr2'
        db.add_column('volunteer_dispatcher_incident', 'addr2',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Incident.addr3'
        db.add_column('volunteer_dispatcher_incident', 'addr3',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'Volunteer.addr1'
        db.delete_column('volunteer_dispatcher_volunteer', 'addr1')

        # Deleting field 'Volunteer.addr2'
        db.delete_column('volunteer_dispatcher_volunteer', 'addr2')

        # Deleting field 'Volunteer.addr3'
        db.delete_column('volunteer_dispatcher_volunteer', 'addr3')

        # Deleting field 'Incident.addr1'
        db.delete_column('volunteer_dispatcher_incident', 'addr1')

        # Deleting field 'Incident.addr2'
        db.delete_column('volunteer_dispatcher_incident', 'addr2')

        # Deleting field 'Incident.addr3'
        db.delete_column('volunteer_dispatcher_incident', 'addr3')

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
            'city': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        }
    }

    complete_apps = ['volunteer_dispatcher']