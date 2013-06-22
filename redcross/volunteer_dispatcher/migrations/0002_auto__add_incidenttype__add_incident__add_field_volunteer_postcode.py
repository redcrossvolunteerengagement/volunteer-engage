# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'IncidentType'
        db.create_table('volunteer_dispatcher_incidenttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('volunteer_dispatcher', ['IncidentType'])

        # Adding model 'Incident'
        db.create_table('volunteer_dispatcher_incident', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('county', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('postcode', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=6)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=6)),
            ('incident_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['volunteer_dispatcher.IncidentType'])),
            ('dispatcher_initial_description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('volunteer_dispatcher', ['Incident'])

        # Adding field 'Volunteer.postcode'
        db.add_column('volunteer_dispatcher_volunteer', 'postcode',
                      self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting model 'IncidentType'
        db.delete_table('volunteer_dispatcher_incidenttype')

        # Deleting model 'Incident'
        db.delete_table('volunteer_dispatcher_incident')

        # Deleting field 'Volunteer.postcode'
        db.delete_column('volunteer_dispatcher_volunteer', 'postcode')

    models = {
        'volunteer_dispatcher.incident': {
            'Meta': {'object_name': 'Incident'},
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