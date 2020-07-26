# Generated by Django 2.2.13 on 2020-07-13 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signature', '0002_auto_20200702_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='category',
            field=models.CharField(choices=[('initialization', 'Initialization'), ('completion', 'Completion'), ('category', 'Category'), ('response', 'Response'), ('negotiation', 'Negotiation'), ('signature', 'Signature')], default='unknown', max_length=20),
        ),
    ]
