# Generated by Django 2.1.5 on 2019-02-02 21:56

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('context_text', '0022_article_data_work_log'),
        ('context', '0001_initial'),
        ('context_data', '0011_datasetcitationdata_work_log'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkDataSetCitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('citation_type', models.CharField(choices=[('mention', 'mention'), ('analysis', 'analysis')], default='mention', max_length=255)),
                ('match_confidence_level', models.DecimalField(blank=True, decimal_places=10, default=0.0, max_digits=11, null=True)),
                ('match_status', models.TextField(blank=True, null=True)),
                ('capture_method', models.CharField(blank=True, max_length=255, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='context_text.Article')),
                ('article_data', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='context_text.Article_Data')),
                ('data_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='context_data.DataSet')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('work_log', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='context.Work_Log')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkDataSetMention',
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
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='context_text.Article')),
                ('article_data', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='context_text.Article_Data')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('work_data_set_citation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='context_data.WorkDataSetCitation')),
                ('work_log', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='context.Work_Log')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkResearchField',
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
                ('article', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='context_text.Article')),
                ('article_data', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='context_text.Article_Data')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('work_log', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='context.Work_Log')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkResearchMethod',
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
                ('article', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='context_text.Article')),
                ('article_data', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='context_text.Article_Data')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('work_log', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='context.Work_Log')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='datasetmention',
            options={},
        ),
        migrations.AddField(
            model_name='datasetcitation',
            name='work_log',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='context.Work_Log'),
        ),
        migrations.AddField(
            model_name='datasetmention',
            name='publication',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='context_text.Article'),
        ),
        migrations.AddField(
            model_name='datasetmention',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='datasetmention',
            name='work_log',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='context.Work_Log'),
        ),
    ]
