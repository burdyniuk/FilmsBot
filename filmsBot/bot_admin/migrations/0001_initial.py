# Generated by Django 3.2.4 on 2021-12-18 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('year_published', models.IntegerField()),
                ('trailler_link', models.CharField(blank=True, max_length=200)),
                ('link_to_film', models.CharField(max_length=200)),
                ('rating', models.FloatField()),
                ('image', models.ImageField(upload_to='images/')),
                ('likes', models.IntegerField(blank=True)),
                ('dislikes', models.IntegerField(blank=True)),
                ('genre', models.ManyToManyField(to='bot_admin.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='BotUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField()),
                ('nickname', models.CharField(max_length=200)),
                ('date_started', models.DateTimeField(verbose_name='Started bot')),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('last_day_active', models.DateTimeField(blank=True, verbose_name='Last time used bot')),
                ('favorite_films', models.ManyToManyField(blank=True, to='bot_admin.Film')),
            ],
        ),
    ]
