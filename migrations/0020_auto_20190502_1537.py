# Generated by Django 2.2.1 on 2019-05-02 15:37

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('context_data', '0019_auto_20190327_2213'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dataset',
            options={'ordering': ['last_modified']},
        ),
        migrations.AddField(
            model_name='dataset',
            name='details_json',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dataset',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
