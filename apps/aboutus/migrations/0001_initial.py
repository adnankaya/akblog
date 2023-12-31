# Generated by Django 4.1.3 on 2023-08-08 13:19

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=120)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Hakkımızda',
                'verbose_name_plural': 'Hakkımızda',
                'db_table': 't_aboutus',
            },
        ),
        migrations.CreateModel(
            name='MainService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=120)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('icon_html', models.CharField(blank=True, max_length=120, null=True)),
                ('path', models.CharField(default='/', max_length=32)),
                ('index', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Ana Hizmet',
                'verbose_name_plural': 'Ana Hizmetler',
                'db_table': 't_aboutus_main_service',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=120)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('icon_html', models.CharField(blank=True, max_length=120, null=True)),
                ('path', models.CharField(default='/', max_length=32)),
                ('main_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aboutus.mainservice')),
            ],
            options={
                'verbose_name': 'Hizmet',
                'verbose_name_plural': 'Hizmetler',
                'db_table': 't_aboutus_service',
            },
        ),
    ]
