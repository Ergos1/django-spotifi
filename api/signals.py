from django.core.signals import request_finished, request_started
from django.dispatch import receiver
import logging

logger = logging.getLogger('django')

@receiver(request_started)
def file_upload_started_callback(sender, **kwargs):
    logger.info("File uploading started")

@receiver(request_finished)
def file_upload_finished_callback(sender, **kwargs):
    logger.info("File uploading finished!")