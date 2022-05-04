from rest_framework import serializers
from .models import Album, Artist, Category, CustomUser, Music, MusicLike, MusicView, Playlist
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_staff = serializers.BooleanField(default=False, read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'password', 'username', 'is_staff')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class MusicsContainerSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()

    class Meta:
        fields = ['id', 'title']


class CategorySerializer(MusicsContainerSerializer, serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"
        # fields = ['id', 'title']


class AlbumSerializer(MusicsContainerSerializer, serializers.ModelSerializer):

    class Meta:
        model = Album
        fields = "__all__"
        # fields = ['id', 'title']


class ArtistSerializer(MusicsContainerSerializer, serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = "__all__"
        # fields = ['id', 'title']


class PlaylistSerializer(MusicsContainerSerializer, serializers.ModelSerializer):

    class Meta:
        model = Playlist
        fields = "__all__"
        # fields = ['id', 'title']


class MusicSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    artist = ArtistSerializer(read_only=True)
    album = AlbumSerializer(read_only=True)
    playlists = PlaylistSerializer(many=True, read_only=True)

    category_title = serializers.CharField(write_only=True)
    artist_title = serializers.CharField(write_only=True)
    album_title = serializers.CharField(write_only=True)

    likes = serializers.IntegerField(source="musiclike_set.count", read_only=True)
    views = serializers.IntegerField(source="musicview_set.count", read_only=True)

    def create(self, validated_data):
        music = Music.objects.create(title=validated_data['title'],
                                     url=validated_data['url'],
                                     category=Category.objects.get_or_create(
                                         title=validated_data['category_title'])[0],
                                     album=Album.objects.get_or_create(
                                         title=validated_data['album_title'])[0],
                                     artist=Artist.objects.get_or_create(title=validated_data['artist_title'])[0])
        return music

    class Meta:
        model = Music
        fields = "__all__"


class UserAndMusicContainerSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    music = MusicSerializer(read_only=True)

    class Meta:
        fields = "__all__"


class MusicLikeSerializer(UserAndMusicContainerSerializer, serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    music_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MusicLike
        fields = "__all__"


class MusicViewSerializer(UserAndMusicContainerSerializer, serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    music_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MusicView
        fields = "__all__"
