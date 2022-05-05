from django.core.signals import request_finished, request_started
from django.dispatch import receiver
from django.db.models.signals import post_save
import logging

from api.models import CustomUser, Music, PersonalPlaylist

logger = logging.getLogger('django')

@receiver(request_started)
def file_upload_started_callback(sender, **kwargs):
    logger.info("File uploading started")

@receiver(request_finished)
def file_upload_finished_callback(sender, **kwargs):
    logger.info("File uploading finished!")

@receiver(post_save, sender=CustomUser)
def new_user(sender, instance, **kwargs):
    logger.info("New user created: {}".format(instance))
    musics = Music.manager.get_max_10_musics_with_shuffle()
    result_of_create_playlist = PersonalPlaylist.manager.create_personal_playlist(instance, musics)
    # logger.info("New playlist created: {}".format(result_of_create_playlist))