from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *




class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ['username']


class AdminSongSerializer(serializers.ModelSerializer):

    class Meta:

        model = Song
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    user  = UserSerializer(read_only=True)

    class Meta:

        model = Comments
        fields = ['user','comment']



class SongDetailSerializer(serializers.ModelSerializer):

    comments = CommentSerializer(many=True)

    class Meta:

        model = Song
        fields =['id','song_name','time_offer','added_on','comments']


class AddCommentSerializer(serializers.ModelSerializer):

    songs = AdminSongSerializer(read_only=True)
    user  = UserSerializer(read_only=True)


    class Meta:

        model = Comments
        fields = ['songs','user','comment','id']


class FavouriteSerialzier(serializers.ModelSerializer):

    songs = AdminSongSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['songs','user','id']


class LikeSerialzier(serializers.ModelSerializer):

    songs = AdminSongSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['songs','user','like_song','id']


class AlbumSerializer(serializers.ModelSerializer):


    creater = UserSerializer(read_only = True,many=False)
    song = AdminSongSerializer(many = True,read_only = True)
    song_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Song.objects.all()
    )

    class Meta:

        model = Album
        fields = ['id','creater','album_name','status','song','song_ids']

    def create(self, validated_data):
        song = validated_data.pop("song_ids", None)
        validated_data["creater"] = self.context["request"].user
        album = Album.objects.create(**validated_data)
        if song:
            album.song.set(song)

        return album


class PublicAlbumSerializer(serializers.ModelSerializer):

    creater = UserSerializer(read_only = True,many=False)

    class Meta:

        model = Album
        fields = ['creater','album_name','id']


class FollowSerialzier(serializers.ModelSerializer):

    album = AlbumSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ['album','user','follow','id']

