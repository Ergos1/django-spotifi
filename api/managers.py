
from django.db import models

import random

import logging
logger = logging.getLogger('django')

class MusicManager(models.Manager):
    def get_by_category(self, category):
        return self.filter(category=category)

    def get_by_album(self, album):
        return self.filter(album=album)
    
    def get_by_artist(self, artist):
        return self.filter(artist=artist)

    def get_max_10_musics_with_shuffle(self):
        items = list(self.all())[:10]
        random.shuffle(items)
        return items

    def clear_from_playlists(self):
        musics = self.all()
        for music in musics:
            music.playlists.clear()
            music.save()

class PlaylistManager(models.Manager):
    def get_personal_playlist(self, user):
        return self.get(owner=user, title="{}'s playlist".format(user.username))

    def create_personal_playlist(self, user, musics):
        logger.info("user: {}; musics: {}".format(user, musics))
        personal_playlist = self.create(owner=user, title="{}'s playlist".format(user.username))
        for music in musics: 
            music.playlists.add(personal_playlist)
            music.save()

        return personal_playlist
    
    def update_personal_playlist(self, user, musics):
        personal_playlist = self.get(owner=user, title="{}'s playlist".format(user.username))
        for music in musics: 
            logger.info("music: {}".format(music))
            music.playlists.add(personal_playlist)
            music.save()

        return personal_playlist


        