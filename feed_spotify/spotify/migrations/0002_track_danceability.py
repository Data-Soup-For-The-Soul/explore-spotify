# Generated by Django 3.0.4 on 2020-03-05 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='danceability',
            field=models.FloatField(null=True),
        ),
    ]
