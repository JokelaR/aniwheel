from django.db import models

# Create your models here.

class Anime(models.Model):
    anilist_id = models.IntegerField(primary_key=True)
    title_en = models.CharField(max_length=255, null=True)
    title_romaji = models.CharField(max_length=255, null=True)
    format = models.CharField(max_length=255)
    banner_image = models.URLField(null=True)

class User(models.Model):
    username = models.CharField(max_length=255)
    associated_emoji = models.CharField(max_length=8, blank=True)

class AnilistUser(User):
    anilist_userid = models.IntegerField(primary_key=True)
    avatar = models.URLField(null=True)
    anime = models.ManyToManyField(Anime)

class Wheel(models.Model):
    name = models.CharField(max_length=255)
    anime = models.ManyToManyField(Anime, through="WheelAnime")


class Session(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    shown_anime = models.ManyToManyField(Anime, through="WatchedAnimeStatus")

class WatchedAnimeStatus(models.Model):
    watched_session = models.ForeignKey(Session, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class WheelAnime(models.Model):
    wheel = models.ForeignKey(Wheel, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)