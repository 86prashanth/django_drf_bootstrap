# Generated by Django 4.2 on 2023-04-16 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drfapp', '0002_streamplatform_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='platform',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='watchlist', to='drfapp.streamplatform'),
            preserve_default=False,
        ),
    ]
