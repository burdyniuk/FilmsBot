from django.db import models
from django.db.models.base import Model

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Film(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    genre = models.ManyToManyField(Genre)
    year_published = models.IntegerField()
    trailler_link = models.CharField(max_length=200, blank=True)
    link_to_film = models.CharField(max_length=200)
    rating = models.FloatField()
    image = models.ImageField(upload_to='images/')
    likes = models.IntegerField(blank=True, default=0)
    dislikes = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name


class BotUser(models.Model):
    user_id = models.BigIntegerField()
    nickname = models.CharField(max_length=200)
    chat_id = models.BigIntegerField(default=-1)
    date_started = models.DateTimeField('Started bot')
    phone_number = models.CharField(max_length=20, blank=True)
    last_day_active = models.DateTimeField('Last time used bot', blank=True)
    favorite_films = models.ManyToManyField(Film, blank=True)


class Ad(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    link = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='images/')
    video = models.FileField(upload_to='videos/', blank=True)
    