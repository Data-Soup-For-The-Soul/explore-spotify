# Generated by Django 3.0.4 on 2020-03-05 02:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('identifier', models.SlugField(unique=True)),
                ('energy', models.FloatField(null=True)),
                ('key', models.PositiveSmallIntegerField(null=True)),
                ('loudness', models.FloatField(null=True)),
                ('mode', models.PositiveSmallIntegerField(null=True)),
                ('speechiness', models.FloatField(null=True)),
                ('acousticness', models.FloatField(null=True)),
                ('instrumentalness', models.FloatField(null=True)),
                ('valence', models.FloatField(null=True)),
                ('tempo', models.FloatField(null=True)),
                ('liveness', models.FloatField(null=True)),
                ('time_signature', models.PositiveSmallIntegerField(null=True)),
                ('duration', models.PositiveIntegerField(null=True)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tracks', to='spotify.Artist')),
            ],
        ),
        migrations.CreateModel(
            name='Hit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveSmallIntegerField()),
                ('streams', models.PositiveIntegerField(null=True)),
                ('country', models.CharField(max_length=10)),
                ('week_of', models.DateField()),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hits', to='spotify.Track')),
            ],
        ),
    ]
