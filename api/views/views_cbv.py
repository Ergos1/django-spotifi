from unicodedata import category
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Album, Artist, Category, Playlist
from api.serializers import AlbumSerializer, ArtistSerializer, MusicsContainerSerializer, CategorySerializer, PlaylistSerializer


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

    def get(self, request):
        playlists = Playlist.objects.all()
        serializer = MusicsContainerSerializer(playlists, many=True)
        return Response({"playlists": serializer.data})

    def post(self, request):
        
        serializer = PlaylistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
