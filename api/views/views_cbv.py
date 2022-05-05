from ssl import create_default_context
from unicodedata import category
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Album, Artist, Category, CustomUser, Music, MusicLike, PersonalPlaylist
from api.serializers import AlbumSerializer, ArtistSerializer, MusicSerializer, MusicsContainerSerializer, CategorySerializer, PersonalPlaylistSerializer, PlaylistSerializer
from django.core.cache import cache

import logging

from api.views.views_fbv import get_user_personal_musics
logger = logging.getLogger('django')


class CategoryList(APIView):

    def get(self, request):
        categories = Category.objects.all()
        serializer = MusicsContainerSerializer(categories, many=True)
        return Response({"categories": serializer.data})

    def post(self, request):

        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlbumList(APIView):

    def get(self, request):
        albums = Album.objects.all()
        serializer = MusicsContainerSerializer(albums, many=True)
        return Response({"albums": serializer.data})

    def post(self, request):
        serializer = AlbumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArtistList(APIView):

    def get(self, request):
        artists = Artist.objects.all()
        serializer = MusicsContainerSerializer(artists, many=True)
        return Response({"artists": serializer.data})

    def post(self, request):

        serializer = ArtistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlaylistList(APIView):
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

    def get(self, request):
        if cache.get("updated")!=None:
            logger.info("no time to update!")
        else: 
            Music.manager.clear_from_playlists()
            users = CustomUser.objects.all()
            for user in users:
                logger.info("user:{}".format(user))
                musics_data = get_user_personal_musics(user)
                musics_ids = [music_data['id'] for music_data in musics_data]
                logger.info("ids: {}".format(musics_ids))
                musics = Music.objects.filter(id__in=musics_ids)
                PersonalPlaylist.manager.update_personal_playlist(user, musics)
            cache.set("updated", True, timeout=1)
        playlist = PersonalPlaylist.manager.get_personal_playlist(request.user)
        serializer = PersonalPlaylistSerializer(playlist, many=False)
        return Response({"playlist: ": serializer.data})
