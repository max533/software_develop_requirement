# Generated by Django 2.2.13 on 2020-07-20 07:51

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField(max_length=1000)),
                ('read_status', models.BooleanField(default=False, verbose_name='the read status of the notification')),
                ('category', models.CharField(choices=[('initialization', 'Initialization'), ('completion', 'Completion'), ('category', 'Category'), ('response', 'Response'), ('negotiation', 'Negotiation'), ('signature', 'Signature')], default='unknown', max_length=20)),
                ('recipient', models.CharField(max_length=20, verbose_name='the owner of the notification')),
                ('actor', models.TextField()),
                ('verb', models.TextField()),
                ('action_object', models.TextField()),
                ('target', models.TextField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('deleted_time', models.DateTimeField(null=True)),
            ],
            options={
                'verbose_name': 'notification',
                'verbose_name_plural': 'notifications',
                'ordering': ['recipient', 'read_status', 'created_time'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.IntegerField(verbose_name="order's account")),
                ('project', models.IntegerField(verbose_name="order's project")),
                ('develop_team_function', models.CharField(max_length=20, verbose_name="developer's function team")),
                ('develop_team_sub_function', models.CharField(max_length=20, verbose_name="developer's sub function team")),
                ('status', django.contrib.postgres.fields.jsonb.JSONField(verbose_name="order's current status")),
                ('initiator', models.CharField(max_length=50, verbose_name="initiator's employee_id")),
                ('assigner', models.CharField(max_length=50, verbose_name="assigner's employee_id (PO/PM)")),
                ('developers', django.contrib.postgres.fields.jsonb.JSONField(default=dict, verbose_name="employee_ids of the developer's contactor and member")),
                ('title', models.CharField(max_length=500)),
                ('description', models.TextField()),
                ('form_begin_time', models.DateTimeField(auto_now_add=True, verbose_name="order's begin time")),
                ('form_end_time', models.DateTimeField(null=True, verbose_name="order's end time")),
                ('expected_develop_duration_day', models.FloatField(blank=True, null=True, verbose_name='expected development duration (days)')),
                ('actual_develop_duration_day', models.FloatField(blank=True, null=True, verbose_name='actual development duration (days)')),
                ('repository_url', models.URLField(blank=True, max_length=1000, verbose_name='repository url of source code')),
                ('update_time', models.DateTimeField(auto_now=True, null=True)),
                ('update_staff', models.CharField(max_length=50)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='signature.Order')),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
                'ordering': ['form_begin_time'],
            },
        ),
        migrations.CreateModel(
            name='Signature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence', models.PositiveIntegerField(null=True)),
                ('signer', models.CharField(max_length=20)),
                ('sign_unit', models.CharField(max_length=20, verbose_name='the department of signing')),
                ('status', models.CharField(max_length=20)),
                ('comment', models.TextField()),
                ('signed_time', models.DateTimeField(null=True)),
                ('role_group', models.CharField(max_length=20)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signature.Order')),
            ],
            options={
                'verbose_name': 'signature',
                'verbose_name_plural': 'signatures',
                'ordering': ['order', 'sequence'],
            },
        ),
        migrations.CreateModel(
            name='ScheduleTracker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('confirm_status', models.BooleanField(default=False)),
                ('expected_time', models.DateTimeField(null=True)),
                ('actual_time', models.DateField(null=True)),
                ('complete_rate', models.PositiveIntegerField(null=True, verbose_name='the complete rate of schedule event')),
                ('created_time', models.DateTimeField(null=True)),
                ('update_time', models.DateTimeField(null=True)),
                ('version', models.IntegerField(null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signature.Order')),
            ],
            options={
                'verbose_name': 'schedule tracker',
                'verbose_name_plural': 'schedule trackers',
                'ordering': ['order', 'version'],
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('confirm_status', models.BooleanField(default=False)),
                ('expected_time', models.DateTimeField(null=True)),
                ('actual_time', models.DateField(null=True)),
                ('complete_rate', models.PositiveIntegerField(verbose_name='the complete rate of schedule event')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('version', models.IntegerField(null=True, verbose_name='current version')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signature.Order')),
            ],
            options={
                'verbose_name': 'schedule',
                'verbose_name_plural': 'schedules',
                'ordering': ['order', 'created_time'],
            },
        ),
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('complete_rate', models.PositiveIntegerField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('editor', models.CharField(max_length=20)),
                ('update_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signature.Order')),
            ],
            options={
                'verbose_name': 'progress',
                'verbose_name_plural': 'progress',
                'ordering': ['order', 'update_time'],
            },
        ),
        migrations.CreateModel(
            name='OrderTracker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.IntegerField(null=True, verbose_name="order's account")),
                ('project', models.IntegerField(null=True, verbose_name="order's project")),
                ('develop_team_function', models.CharField(max_length=20, verbose_name="developer's function team")),
                ('develop_team_sub_function', models.CharField(max_length=20, verbose_name="developer's sub function team")),
                ('status', django.contrib.postgres.fields.jsonb.JSONField(default=dict, verbose_name="order's current status")),
                ('initiator', models.CharField(max_length=50, verbose_name="initiator's employee_id")),
                ('assigner', models.CharField(max_length=50, verbose_name="assigner's employee_id (PO/PM)")),
                ('developers', django.contrib.postgres.fields.jsonb.JSONField(default=dict, verbose_name="employee_ids of the developer's contactor and member")),
                ('title', models.CharField(max_length=500)),
                ('description', models.TextField()),
                ('form_begin_time', models.DateTimeField(verbose_name="order's begin time")),
                ('form_end_time', models.DateTimeField(null=True, verbose_name="order's end time")),
                ('expected_develop_duration_day', models.FloatField(blank=True, null=True, verbose_name='expected development duration (days)')),
                ('actual_develop_duration_day', models.FloatField(blank=True, null=True, verbose_name='actual development duration (days)')),
                ('repository_url', models.URLField(blank=True, max_length=1000, verbose_name='repository url of source code')),
                ('update_time', models.DateTimeField(auto_now=True, null=True)),
                ('update_staff', models.CharField(max_length=50)),
                ('parent', models.PositiveIntegerField(null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signature.Order')),
            ],
            options={
                'verbose_name': 'order tracker',
                'verbose_name_plural': 'order trackers',
                'ordering': ['order', 'update_time'],
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.FileField(max_length=200, upload_to='', verbose_name="document's relative path")),
                ('name', models.CharField(max_length=200, verbose_name="docuemnt's name")),
                ('description', models.CharField(max_length=1000, verbose_name="document's description")),
                ('size', models.PositiveIntegerField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('uploader', models.CharField(max_length=20)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signature.Order')),
            ],
            options={
                'verbose_name': 'document',
                'verbose_name_plural': 'documents',
                'ordering': ['order', 'created_time'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('editor', models.CharField(max_length=20)),
                ('comment', models.TextField()),
                ('created_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signature.Order')),
            ],
            options={
                'verbose_name': 'history',
                'verbose_name_plural': 'histories',
                'ordering': ['order', 'created_time'],
            },
        ),
    ]
