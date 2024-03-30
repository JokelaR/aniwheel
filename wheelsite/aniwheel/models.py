from django.db import models

# Create your models here.

class Anime(models.Model):
    anilist_id = models.IntegerField(primary_key=True)
    title_en = models.CharField(max_length=255, null=True)
    title_romaji = models.CharField(max_length=255, null=True)
    format = models.CharField(max_length=255)
    banner_image = models.URLField(null=True)
    cover_image = models.URLField(null=True)
    cover_color = models.CharField(max_length=7, null=True)

class AnilistUser(models.Model):
    anilist_userid = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=255)
    avatar = models.URLField(null=True)
    associated_emoji = models.CharField(max_length=8, blank=True)
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
    description = models.TextField(blank=True)

class WheelAnime(models.Model):
    wheel = models.ForeignKey(Wheel, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    owner = models.ForeignKey(AnilistUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)