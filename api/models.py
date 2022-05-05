from email.policy import default
from statistics import mode
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.conf import settings

from api.managers import MusicManager, PlaylistManager
from django.core.validators import MinLengthValidator


class CustomUser(AbstractUser):
    logo_image = models.ImageField(
        upload_to='images/', blank=False, null=False, default="images/default.png")


class MusicsContainer(models.Model):
    title = models.CharField(
        max_length=255, default="unknown music container :p", unique=True, validators=[MinLengthValidator(4)])

    class Meta:
        abstract = True




class PersonalPlaylist(models.Model):
    title = models.CharField(max_length=255, default="unknown :p", validators=[MinLengthValidator(4)])
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    
    objects = models.Manager()
    manager = PlaylistManager()


class Category(MusicsContainer):
    pass


class Album(MusicsContainer):
    pass


class Artist(MusicsContainer):
    pass


class Music(models.Model):
    title = models.CharField(max_length=255, default="unknown music :p")
    url = models.URLField()
    playlists = models.ManyToManyField(PersonalPlaylist, default=[])
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, default=None, null=True)
    album = models.ForeignKey(
        Album, on_delete=models.CASCADE, default=None, null=True)
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, default=None, null=True)

    objects = models.Manager()
    manager = MusicManager()


class UserAndMusicContainer(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    music = models.ForeignKey(Music, on_delete=models.CASCADE)

    class Meta:
        abstract = True
        unique_together = ('user', 'music')


class MusicLike(UserAndMusicContainer):
    pass


class MusicView(UserAndMusicContainer):
    pass
