# Generated by Django 3.2.7 on 2021-09-26 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '0003_remove_song_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='song',
            field=models.ManyToManyField(blank=True, related_name='songs', to='playlist.Song'),
        ),
    ]
