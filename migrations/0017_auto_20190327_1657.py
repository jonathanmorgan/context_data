# Generated by Django 2.1.7 on 2019-03-27 16:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('sourcenet', '0022_article_data_work_log'),
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('context', '0004_auto_20190305_1858'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sourcenet_datasets', '0016_auto_20190204_1908'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataMention',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField(blank=True, null=True)),
                ('value_in_context', models.TextField(blank=True, null=True)),
                ('value_index', models.IntegerField(blank=True, default=0, null=True)),
                ('value_length', models.IntegerField(blank=True, default=0, null=True)),
                ('canonical_index', models.IntegerField(blank=True, default=0, null=True)),
                ('value_word_number_start', models.IntegerField(blank=True, default=0, null=True)),
                ('value_word_number_end', models.IntegerField(blank=True, default=0, null=True)),
                ('paragraph_number', models.IntegerField(blank=True, default=0, null=True)),
                ('context_before', models.TextField(blank=True, null=True)),
                ('context_after', models.TextField(blank=True, null=True)),
                ('capture_method', models.CharField(blank=True, max_length=255, null=True)),
                ('uuid', models.TextField(blank=True, null=True)),
                ('uuid_name', models.CharField(blank=True, max_length=255, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('team_name', models.CharField(blank=True, max_length=255, null=True)),
                ('mention_type', models.CharField(choices=[('mention', 'mention'), ('analysis', 'analysis')], default='mention', max_length=255)),
                ('score', models.FloatField(blank=True, null=True)),
                ('start_index', models.IntegerField(blank=True, null=True)),
                ('occurrence_number', models.IntegerField(blank=True, null=True)),
                ('article', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sourcenet.Article')),
                ('article_data', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sourcenet.Article_Data')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DataReference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('citation_type', models.CharField(choices=[('mention', 'mention'), ('analysis', 'analysis')], default='mention', max_length=255)),
                ('match_confidence_level', models.DecimalField(blank=True, decimal_places=10, default=0.0, max_digits=11, null=True)),
                ('match_status', models.TextField(blank=True, null=True)),
                ('capture_method', models.CharField(blank=True, max_length=255, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('score', models.FloatField(blank=True, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('key_terms', models.TextField(blank=True, null=True)),
                ('context_text', models.TextField(blank=True, null=True)),
                ('coder_type', models.CharField(blank=True, max_length=255, null=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sourcenet.Article')),
                ('article_data', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sourcenet.Article_Data')),
                ('coder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('data_set', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sourcenet_datasets.DataSet')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('work_log', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='context.Work_Log')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='datamention',
            name='data_reference',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sourcenet_datasets.DataReference'),
        ),
        migrations.AddField(
            model_name='datamention',
            name='data_set_citation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sourcenet_datasets.DataSetCitation'),
        ),
        migrations.AddField(
            model_name='datamention',
            name='data_set_citation_data',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sourcenet_datasets.DataSetCitationData'),
        ),
        migrations.AddField(
            model_name='datamention',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='datamention',
            name='work_log',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='context.Work_Log'),
        ),
    ]
