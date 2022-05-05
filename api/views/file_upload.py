
from django.http import HttpResponse, HttpResponseRedirect

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from api.models import CustomUser, MusicLike
from api.serializers import MusicLikeSerializer, MusicSerializer, MusicViewSerializer, UserSerializer
from django.core.signals import request_started, request_finished
from api.signals import file_upload_started_callback, file_upload_finished_callback
import logging

logger = logging.getLogger('django')

@api_view(["POST"])
def upload_image(request):
    if request.method == "POST":
        logger.info("Files: {}".format(request.FILES))
        user = CustomUser.objects.get(id=request.user.id)
        logger.info("User: {}".format(user))
        user.logo_image = request.FILES['image']
        user.save()
        return Response({"message": "Image successfully uploaded"})