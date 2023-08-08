# Generated by Django 4.1.3 on 2023-08-08 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialaccount',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='socialaccounts', to='users.profile'),
        ),
        migrations.AddField(
            model_name='socialaccount',
            name='website',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='socialaccounts', to='core.website'),
        ),
        migrations.AddField(
            model_name='phone',
            name='website',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.website'),
        ),
        migrations.AddField(
            model_name='mail',
            name='website',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.website'),
        ),
        migrations.AddField(
            model_name='hitcount',
            name='url_hit',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='core.urlhit'),
        ),
        migrations.AlterUniqueTogether(
            name='socialaccount',
            unique_together={('slug', 'url')},
        ),
    ]