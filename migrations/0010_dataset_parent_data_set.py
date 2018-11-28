# Generated by Django 2.1 on 2018-09-11 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sourcenet_datasets', '0009_dataset_family_identifier'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='parent_data_set',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sourcenet_datasets.DataSet'),
        ),
    ]