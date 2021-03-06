from rest_framework import serializers
from .models import Album, Artist, Category, CustomUser, Music, MusicLike, MusicView, PersonalPlaylist
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_staff = serializers.BooleanField(default=False, read_only=True)

    def validate_password(self, value: str) -> str:
        return make_password(value)

    class Meta:
        model = CustomUser
        fields = ('id', 'password', 'username', 'is_staff')


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

        validators = [
            UniqueTogetherValidator(
                queryset=Category.objects.all(),
                fields=['title']
            )
        ]


class AlbumSerializer(MusicsContainerSerializer, serializers.ModelSerializer):

    class Meta:
        model = Album
        fields = "__all__"
        # fields = ['id', 'title']
        validators = [
            UniqueTogetherValidator(
                queryset=Album.objects.all(),
                fields=['title']
            )
        ]


class ArtistSerializer(MusicsContainerSerializer, serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = "__all__"
        # fields = ['id', 'title']

        validators = [
            UniqueTogetherValidator(
                queryset=Artist.objects.all(),
                fields=['title']
            )
        ]


class PlaylistSerializer(MusicsContainerSerializer, serializers.ModelSerializer):

    class Meta:
        model = PersonalPlaylist
        fields = "__all__"
        # fields = ['id', 'title']

        validators = [
            UniqueTogetherValidator(
                queryset=PersonalPlaylist.objects.all(),
                fields=['title']
            )
        ]


class MusicSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    artist = ArtistSerializer(read_only=True)
    album = AlbumSerializer(read_only=True)
    playlists = PlaylistSerializer(many=True, read_only=True)

    category_title = serializers.CharField(write_only=True)
    artist_title = serializers.CharField(write_only=True)
    album_title = serializers.CharField(write_only=True)

    likes = serializers.IntegerField(
        source="musiclike_set.count", read_only=True)
    views = serializers.IntegerField(
        source="musicview_set.count", read_only=True)

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


class PersonalPlaylistSerializer(PlaylistSerializer):
    musics = MusicSerializer(source="music_set", many=True)

    class Meta:
        model = PersonalPlaylist
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

        validators = [
            UniqueTogetherValidator(
                queryset=MusicLike.objects.all(),
                fields=['user', 'music']
            )
        ]


class MusicViewSerializer(UserAndMusicContainerSerializer, serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    music_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MusicView
        fields = "__all__"

        validators = [
            UniqueTogetherValidator(
                queryset=MusicView.objects.all(),
                fields=['user', 'music']
            )
        ]
