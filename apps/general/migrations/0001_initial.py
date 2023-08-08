# Generated by Django 4.1.3 on 2023-08-08 13:19

import ckeditor.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('index', models.SmallIntegerField()),
                ('interval', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(100), django.core.validators.MaxValueValidator(20000)])),
                ('title', models.CharField(blank=True, max_length=140, null=True)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/slides/', verbose_name='Slide Image')),
                ('position', models.CharField(choices=[('header', 'header'), ('rightbar1', 'rightbar1'), ('rightbar2', 'rightbar2'), ('rightbar3', 'rightbar3')], default='rightbar3', max_length=24)),
            ],
            options={
                'db_table': 't_slide',
            },
        ),
        migrations.CreateModel(
            name='ThankYou',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', ckeditor.fields.RichTextField()),
            ],
            options={
                'db_table': 't_thankyou',
            },
        ),
    ]
