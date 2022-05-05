
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


@api_view(["GET"])
def get_user_personal_playlist(request):
    logger.info("playlist {}".format(request))
    if request.method == "GET":
        logger.info("playlist {}".format(playlist))
        playlist = PersonalPlaylist.objects.get(owner=request.user)
        logger.info("playlist {}".format(playlist))
        if len(playlist) == 0:
            createOrUpdatePersonalPlaylists()

        serializer = PersonalPlaylistSerializer(playlist)

        return Response({"playlist": serializer.data})


def get_user_personal_musics(user):
    liked_musics = MusicLike.objects.filter(user=user)
    liked_musics_ids = [
        liked_music.music.id for liked_music in liked_musics]
    logger.info("musics id: {}".format(liked_musics_ids))
    logger.info("musics in id: {}".format(6 in liked_musics_ids))
    musics = Music.objects.all()
    musics = list(filter(lambda music: (
        music.id in liked_musics_ids) == False, musics))
    logger.info("music filtered: {}".format(
        list(filter(lambda music: (music.id in liked_musics_ids) == False, musics))))
    for liked_music in liked_musics:
        musics.append(liked_music.music)
    serializer = MusicSerializer(musics, many=True)
    for music in serializer.data:
        music['points'] = music['likes']
        if music['id'] in liked_musics_ids:
            music['points'] += 1
    return sorted(serializer.data, key=lambda m: m['points'], reverse=True)[:min(10, len(serializer.data))]


def createOrUpdatePersonalPlaylists():
    users = CustomUser.objects.all()
    for user in users:
        playlist = PersonalPlaylist.objects.get_or_create(
            owner=user, title=user.username+" playlist")
        musics = get_user_personal_musics(user)
        for music in musics:
            logger.info("music: {}".format(music))
            music.playlists.add(playlist)
            music.save()
