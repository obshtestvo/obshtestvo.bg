# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'User.is_browsable'
        db.add_column(u'projects_user', 'is_browsable',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'User.is_browsable'
        db.delete_column(u'projects_user', 'is_browsable')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'projects.event': {
            'Meta': {'object_name': 'Event'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'contact': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'organizers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'events'", 'blank': 'True', 'to': u"orm['projects.Organisation']"}),
            'strategy': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'projects.member': {
            'Meta': {'object_name': 'Member'},
            'availability': ('django.db.models.fields.CharField', [], {'default': "'reader'", 'max_length': '20'}),
            'available_after': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'contact_frequency': ('django.db.models.fields.CharField', [], {'default': "'d'", 'max_length': '2'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'facebook': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_paid_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_contacted_at': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'latest_answer': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'offered_help': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'projects_active': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'active_members'", 'blank': 'True', 'to': u"orm['projects.Project']"}),
            'projects_interests': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'interested_members'", 'blank': 'True', 'to': u"orm['projects.Project']"}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'members'", 'blank': 'True', 'to': u"orm['projects.Skill']"}),
            'types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'members'", 'blank': 'True', 'to': u"orm['projects.MemberType']"}),
            'update_from_user': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'member'", 'null': 'True', 'to': u"orm['projects.User']"}),
            'working_on': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'working_members'", 'null': 'True', 'to': u"orm['projects.Project']"})
        },
        u'projects.membertype': {
            'Meta': {'object_name': 'MemberType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'projects.organisation': {
            'Meta': {'object_name': 'Organisation'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'contact': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'found_via': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'middlemen': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'middleman_organisations'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['projects.Member']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'partnered_project': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'partners'", 'null': 'True', 'to': u"orm['projects.Project']"}),
            'provided_help': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'representatives': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'strategy': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'organisations'", 'blank': 'True', 'to': u"orm['projects.OrganisationType']"}),
            'working_with': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'projects.organisationtype': {
            'Meta': {'object_name': 'OrganisationType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'projects.project': {
            'Meta': {'ordering': "['order']", 'object_name': 'Project'},
            'complimenting_color': ('django.db.models.fields.CharField', [], {'max_length': '7', 'blank': 'True'}),
            'cover_image': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'facebook_group': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'github_repo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'has_static_page': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_forced_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'logo': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'logo_styled': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'logo_thumb': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pm_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'blank': 'True'}),
            'strategy': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'projects.projectactivity': {
            'Meta': {'object_name': 'ProjectActivity'},
            'can_accomodate': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_organisational': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_template': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'activities'", 'null': 'True', 'to': u"orm['projects.Project']"}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'project_activities'", 'symmetrical': 'False', 'through': u"orm['projects.UserActivity']", 'to': u"orm['projects.User']"})
        },
        u'projects.projectmilestone': {
            'Meta': {'object_name': 'ProjectMilestone'},
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_technical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'percent': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '3'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'milestones'", 'to': u"orm['projects.Project']"}),
            'target_date': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'projects.projectmotive': {
            'Meta': {'object_name': 'ProjectMotive'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'motives'", 'to': u"orm['projects.Project']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'projects.projectusageexamplestep': {
            'Meta': {'object_name': 'ProjectUsageExampleStep'},
            'example_number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'example_steps'", 'to': u"orm['projects.Project']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        u'projects.skill': {
            'Meta': {'ordering': "['id']", 'object_name': 'Skill'},
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'skills'", 'blank': 'True', 'to': u"orm['projects.SkillGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'projects.skillgroup': {
            'Meta': {'ordering': "['order']", 'object_name': 'SkillGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'projects.task': {
            'Meta': {'object_name': 'Task'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks'", 'to': u"orm['projects.ProjectActivity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'points': ('django.db.models.fields.PositiveIntegerField', [], {'default': '5', 'max_length': '4'})
        },
        u'projects.update': {
            'Meta': {'object_name': 'Update'},
            'change': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'projects.user': {
            'Meta': {'object_name': 'User'},
            'available_after': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'avatar': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'bio': ('django.db.models.fields.TextField', [], {}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            'has_confirmed_data': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_browsable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'profession': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'projects_interests': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'interested_users'", 'blank': 'True', 'to': u"orm['projects.Project']"}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'users'", 'blank': 'True', 'to': u"orm['projects.Skill']"}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'projects.useractivity': {
            'Meta': {'unique_together': "(('person', 'project_activity'),)", 'object_name': 'UserActivity'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_stopped_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'needs_replacement': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'activities'", 'to': u"orm['projects.User']"}),
            'progress': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'project_activity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_activities'", 'to': u"orm['projects.ProjectActivity']"})
        },
        u'projects.userpointspending': {
            'Meta': {'object_name': 'UserPointSpending'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'spendings'", 'to': u"orm['projects.User']"}),
            'points': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'}),
            'product': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'projects.userprojectpause': {
            'Meta': {'unique_together': "(('project', 'person'),)", 'object_name': 'UserProjectPause'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pauses'", 'to': u"orm['projects.User']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pauses'", 'to': u"orm['projects.Project']"})
        }
    }

    complete_apps = ['projects']