"""
Playlist file serializer
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
                    Song,Album,Comments,
                    Favorite,Like,Follow
                    )




class UserSerializer(serializers.ModelSerializer):

    """
    This Serializer is used for only nested serialization just only to
    get username from db to check which person is logged in this Serializer
    has realtion with CommentSerializer, PublicAlbumSerializer and FollowSerialzier
    """

    class Meta: # pylint: disable=too-few-public-methods

        """In class Meta model User is used and its field username is only used"""

        model = User
        fields = ['username']


class AdminSongSerializer(serializers.ModelSerializer):

    """
    This serializer is used by admin to add update,del songs
    Moreover this serializer has nested relation with AddCommentSerializer,
    FavouriteSerialzier,LikeSerialzier and AlbumSerializer,AddCommentSerializer,
    FavouriteSerialzier,LikeSerialzier,AlbumSerializer
    """

    class Meta: # pylint: disable=too-few-public-methods

        """In class Meta model Song is used and its all db fields are used"""

        model = Song
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    """
    This serializer is has a nested relation with SongDetailSerializer
    The purpose of this serializer was to view all comments user wise in
    SongDetailSerializer
    """

    user  = UserSerializer(read_only=True)

    class Meta: # pylint: disable=too-few-public-methods

        """In class Meta model Comments is used and fields user and comment
        are only used"""

        model = Comments
        fields = ['user','comment']



class SongDetailSerializer(serializers.ModelSerializer):

    """
    This serialzier has a realtion with Comment Serialzier, this serializer was
    used for the display detail view of songs with comments on it(comments would be
    user wise)
    """

    comments = CommentSerializer(many=True)

    class Meta: # pylint: disable=too-few-public-methods

        """In class Meta model Song is used """

        model = Song
        fields =['id','song_name','time_offer','added_on','comments']


class AddCommentSerializer(serializers.ModelSerializer):

    """
    This serialzier is used to add comments on songs and
    has realtion with AdminSongs and user, Admin Song serializer
    is in relation because  user will choose song from list
    of songs then add comment on that  sepecific song,
    """

    songs = AdminSongSerializer(read_only=True)
    user  = UserSerializer(read_only=True)


    class Meta: # pylint: disable=too-few-public-methods

        """In class Meta model Comments is used and its field songs,user,comment and id"""

        model = Comments
        fields = ['songs','user','comment','id']


class FavouriteSerialzier(serializers.ModelSerializer):

    """
    This serialzier is used to add songs to favourite each user
    will have its own favourits songs list thats why it has realtion
    with UserSerializer and user will select songs from list created by
    AdminSongSerializer
    """

    songs = AdminSongSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta: # pylint: disable=too-few-public-methods

        """In class Meta model Favorite is used and its field songs,user and id"""

        model = Favorite
        fields = ['songs','user','id']


class LikeSerialzier(serializers.ModelSerializer):

    """
    This serialzier is used to like songs each user
    will have its own liked songs list thats why it has realtion
    with UserSerializer and user will select songs from list created by
    AdminSongSerializer
    """

    songs = AdminSongSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta: # pylint: disable=too-few-public-methods

        """In class Meta model like is used"""

        model = Like
        fields = ['songs','user','like_song','id']


class AlbumSerializer(serializers.ModelSerializer):

    """
    Registered user can create its own album It has 3 nested
    relationships one with UserSerailzier any registered user
    can create his/her album and AdminSongSerializer to get the
    details of songs in an album and Primary key realtion with songs
    so that he can add songs with id

    """

    creater = UserSerializer(read_only = True,many=False)
    song = AdminSongSerializer(many = True,read_only = True)
    song_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Song.objects.all()
    )

    class Meta: # pylint: disable=too-few-public-methods

        """In class Meta model Album is used """

        model = Album
        fields = ['id','creater','album_name','status','song','song_ids']


    def create(self, validated_data):

        """
        This function is used to create album for user by creating
        details of songs requesting user and setting song with ids in
        that album
        """

        song = validated_data.pop("song_ids", None)
        validated_data["creater"] = self.context["request"].user
        album = Album.objects.create(**validated_data)
        if song:
            album.song.set(song)

        return album


class PublicAlbumSerializer(serializers.ModelSerializer):

    """
    This Serailzier is used to For display public albums to clients
    on websites
    """

    creater = UserSerializer(read_only = True,many=False)

    class Meta: # pylint: disable=too-few-public-methods

        """In class Meta model Album is used and its fields are creater,album_name and id"""

        model = Album
        fields = ['creater','album_name','id']


class FollowSerialzier(serializers.ModelSerializer):

    """
    This Serailzier is used to For following albums and only registered user
    can follow an album
    """

    album = AlbumSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta: # pylint: disable=too-few-public-methods

        """In class Meta model Follow is used and its fields are album,user,follow,id"""

        model = Follow
        fields = ['album','user','follow','id']
