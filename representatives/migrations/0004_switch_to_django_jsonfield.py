# Generated by Django 1.10.5 on 2017-02-23 20:05

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0003_auto_20170214_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='extra',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='offices',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=[]),
        ),
        migrations.AlterField(
            model_name='representative',
            name='extra',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
        migrations.AlterField(
            model_name='representative',
            name='offices',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=[]),
        ),
    ]
