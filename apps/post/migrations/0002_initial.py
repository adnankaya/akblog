# Generated by Django 4.1.3 on 2023-08-08 13:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('post', '0001_initial'),
        ('taggit', '0005_auto_20220424_2025'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='orderedpackage',
            name='package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='post.package'),
        ),
        migrations.AddField(
            model_name='orderedpackage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='inappropriatepost',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.post'),
        ),
        migrations.AddField(
            model_name='inappropriatepost',
            name='reported_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reported_inappropriate_posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='post',
            unique_together={('created_by', 'slug')},
        ),
        migrations.AlterUniqueTogether(
            name='inappropriatepost',
            unique_together={('post', 'reported_by')},
        ),
    ]
