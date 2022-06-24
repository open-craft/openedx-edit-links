# Generated by Django 3.2.13 on 2022-06-24 06:36

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EditLinkedCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('course_id', models.CharField(max_length=255)),
                ('repository_url', models.URLField(max_length=255)),
                ('edit_tool_base_url', models.URLField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
