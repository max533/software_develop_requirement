# Generated by Django 2.2.19 on 2021-04-28 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signature', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='name',
            field=models.TextField(verbose_name="document's name"),
        ),
    ]
