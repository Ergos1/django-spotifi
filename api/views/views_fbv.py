
from urllib import request
from django.http import HttpResponse, HttpResponseRedirect

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from api.models import CustomUser, Music, MusicLike, PersonalPlaylist
from api.serializers import MusicLikeSerializer, MusicSerializer, MusicViewSerializer, PersonalPlaylistSerializer, UserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny

import logging
logger = logging.getLogger('django')


@api_view(["POST"])
@permission_classes([AllowAny])
def sign_up_user(request):
    if request.method == 'POST':
        logger.info("{} try to register".format(
            request.data.get("username", "unknown")))
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User was created"}, status=status.HTTP_201_CREATED)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def like_music(request):
    if request.method == 'POST':
        request.data['user_id'] = request.user.id
        serializer = MusicLikeSerializer(data=request.data)
        logger.info("{} try like {}".format(
            request.user.username, serializer.initial_data))
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Successfully liked"}, status=status.HTTP_200_OK)
        return Response({'message': "Already liked"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def view_music(request):
    if request.method == 'POST':
        request.data['user_id'] = request.user.id
        serializer = MusicViewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Successfully viewd"}, status=status.HTTP_200_OK)
        return Response({'message': "Already viewed"}, status=status.HTTP_400_BAD_REQUEST)

