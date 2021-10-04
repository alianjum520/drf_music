"""
This is views.py file for playlist
"""
from django_filters.rest_framework import DjangoFilterBackend # pylint: disable=import-error
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from .serializers import *  # pylint: disable=wildcard-import # pylint: disable=unused-wildcard-import
from .models import *  #pylint: disable=wildcard-import  # pylint: disable=unused-wildcard-import



# Create your views here.

class AdminSongsViewSet(viewsets.ModelViewSet):

    """
    This is song Viewset This is used get,update,del
    songs and only admin is authorized to use this viewset only
    """

    permission_classes = [IsAdminUser]
    queryset = Song.objects.all()
    serializer_class = AdminSongSerializer



class SongView(GenericAPIView,mixins.ListModelMixin):

    """
    This is used to to view all songs present in site anyone
    can see this
    """

    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        'added_on':['exact', 'gt', 'lt'],
        'song_name': ['exact']
    }
    search_fields = ['$song_name']
    ordering_fields = ['song_name', 'id']
    ordering = ['-id']
    serializer_class = AdminSongSerializer
    queryset = Song.objects.all()

    def get(self,request):

        """
        This is used to list the songs
        """

        return self.list(request)



class SongDetailView(APIView):

    """
    This class displays the detail view of songs
    """

    permission_classes = [AllowAny]

    def get(self,request,id):

        """
        This funtion get the id and displays the detail view of song
        of that specific song id
        """

        try:
            song = Song.objects.get(id=id)
            serializer = SongDetailSerializer(song)

            return Response(serializer.data)

        except Song.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)



class SongsAddComment(APIView):

    """
    This view class is used to add comments
    and only authenticated user can add comment
    """

    permission_classes = [IsAuthenticated]


    def get(self,request,songs_id):

        """
        This function filters all the comments of that specific song
        """

        comment = Comments.objects.filter(songs__id=songs_id)
        if comment.exists():
            serializer = AddCommentSerializer(comment, many = True)
            return Response(serializer.data)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self,request,songs_id):
        """
        This function is used to post comment on a specific song and authencticated user can only
        access that
        """
        data=request.data
        songs = Song.objects.get(id= songs_id)
        user = self.request.user
        new_comment = Comments.objects.create(comment=data["comment"],songs = songs,user=user)
        serializer = AddCommentSerializer(new_comment, data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



class SongsCommentView(APIView):

    """
    This view is used to  update comment but user who created that
    comment can only update that
    """

    permission_classes = [IsAuthenticated]

    def get_object(self,request,songs_id,id):

        """
        This function gets object song id, id of comment and user who created that
        comment
        """

        try:
            songs = Comments.objects.get(songs__id=songs_id,id=id,user=self.request.user)
            return songs
        except Comments.DoesNotExist:

            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self,request,songs_id,id):

        """
        The get function shows the detail view of the comment
        """

        songs = self.get_object(request,songs_id,id)
        serializer = AddCommentSerializer(songs)

        return Response(serializer.data)

    def put(self,request,songs_id,id):

        """
        This is used to update the comment
        """

        songs = self.get_object(request,songs_id,id)
        serializer = AddCommentSerializer(songs,data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self,request,songs_id,id):

        """
        This is used to delete a specific comment created by a user
        """

        comment = self.get_object(request,songs_id,id)
        comment.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)



class AllFavView(APIView):

    """
    THis view shows all the Fav songs by user(user specified)
    """

    permission_classes = [IsAuthenticated]

    def get(self,request):

        """
        This function is used to get all Fav songs
        """

        fav = Favorite.objects.filter(user = self.request.user)
        if fav.exists():
            serializer = FavouriteSerialzier(fav, many = True)
            return Response(serializer.data)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)



class SongsAddFavourite(APIView):

    """
    This view is used to add song to favs
    """

    permission_classes = [IsAuthenticated]


    def get(self,request,songs_id):

        """
        This function gets the songs id  and user
        """

        fav = Favorite.objects.filter(songs__id=songs_id,user = self.request.user)
        if fav.exists():
            serializer = FavouriteSerialzier(fav, many = True)
            return Response(serializer.data)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self,request,songs_id):

        """
        This function is used to add  the song in Fav playlist of user
        """

        songs = Song.objects.get(id= songs_id)
        user = self.request.user
        new_fav = Favorite.objects.create(songs = songs,user=user)
        serializer = FavouriteSerialzier(new_fav, data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



class SongsFavouriteView(APIView):

    """
    This view is used to update fav on song
    """

    permission_classes = [IsAuthenticated]

    def get_object(self,request,id):

        """
        This function gets the object
        """

        try:
            fav_songs = Favorite.objects.get(id=id,user=self.request.user)
            return fav_songs
        except Favorite.DoesNotExist:

            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self,request,id):

        """
        This function displays the fav song of sepecific id
        """

        fav_songs = self.get_object(request,id)
        serializer = FavouriteSerialzier(fav_songs)

        return Response(serializer.data)

    def delete(self,request,id):

        """
        This function is used to delete the song from Fav db
        """

        fav_song = self.get_object(request,id)
        fav_song.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)




class LikeSong(APIView):

    """
    THis view shows all the liked songs by user(user specified)
    """

    permission_classes =[IsAuthenticated]

    def get(self,request):

        """
        This function is used to get all liked songs
        """

        like_song = Like.objects.filter(user = self.request.user)
        if like_song.exists():
            serializer = LikeSerialzier(like_song, many = True)
            return Response(serializer.data)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class AddLikeSongs(APIView):

    """
    This song is used to like song
    """

    permission_classes = [IsAuthenticated]


    def get(self,request,songs_id):

        """
        This function gets the songs id  and user
        """

        like_song = Like.objects.filter(songs__id=songs_id,user = self.request.user)
        if like_song.exists():
            serializer = LikeSerialzier(like_song, many = True)
            return Response(serializer.data)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self,request,songs_id):

        """
        This function is used to add  the song in liked playlist of user
        """

        like_song = Song.objects.get(id= songs_id)
        user = self.request.user
        new_like = Like.objects.create(songs = like_song,user=user)
        serializer = LikeSerialzier(new_like, data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



class LikeUpdateView(APIView):

    """
    This view is used to update like on song
    """

    permission_classes = [IsAuthenticated]

    def get_object(self,request,id):

        """
        This function gets the object
        """

        try:
            like_song = Like.objects.get(id=id,user=self.request.user)
            return like_song
        except Like.DoesNotExist:

            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self,request,id):

        """
        This function displays the liked song of sepecific id
        """

        like_song = self.get_object(request,id)
        serializer = LikeSerialzier(like_song)

        return Response(serializer.data)

    def put(self,request,id):

        """
        This function is used to update the status of liked song
        """

        songs = self.get_object(request,id)
        serializer = LikeSerialzier(songs,data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):

        """
        This function is used to delete the song from liked db
        """

        like_song = self.get_object(request,id)
        like_song.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)



class AlbumViewset(viewsets.ModelViewSet):

    """
    This viewset is used by authenticated user only
    user can crete update and delete its album
    """

    permission_classes= [IsAuthenticated]
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    def get_queryset(self):

        """
        This function is used to set user of the album
        """
        queryset = self.queryset
        query_set = queryset.filter(creater=self.request.user)
        return query_set



class PublicAlbum(APIView):

    """
    This view displays all public albums
    """

    permission_classes = [AllowAny]

    def get(self,request):

        """
        This gets all the public albums in db
        """

        album = Album.objects.filter(status = "public")
        if album.exists():
            serializer = PublicAlbumSerializer(album, many = True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)



class PublicAlbumDetail(APIView):

    """
    This view is used to display detail view of sepecific public album
    """

    permission_classes = [AllowAny]

    def get(self,request,id):

        """
        Used to deisplay detail view of sepecific public album
        """

        album = Album.objects.filter(id=id,status = "public")
        if album.exists():
            serializer = AlbumSerializer(album, many = True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)



class FollowedAlbum(APIView):

    """
    This function is used to display all  followed albums
    followed by a specific user
    """

    permission_classes =[IsAuthenticated]

    def get(self,request):
        """
        THis function displays all the followed albums by user
        """



        follow_album = Follow.objects.filter(user = self.request.user)
        if follow_album.exists():
            serializer = LikeSerialzier(follow_album, many = True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)



class FollowAlbum(APIView):

    """
    This view is used to Follow a sepcific album
    """

    permission_classes = [IsAuthenticated]


    def get(self,request,album_id):

        """
        This function gets the album id and user
        """

        follow_album = Follow.objects.filter(album__id=album_id,user = self.request.user)
        if follow_album.exists():
            serializer = FollowSerialzier(follow_album, many = True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self,request,album_id):

        """
        This function is used to follow any new album
        """

        follow_album = Album.objects.get(id= album_id)
        user = self.request.user
        follow = Follow.objects.create(album = follow_album,user=user)
        serializer = FollowSerialzier(follow, data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



class FollowUpdateView(APIView):

    """
    This class is used to update followed ablum
    """

    permission_classes = [IsAuthenticated]

    def get_object(self,request,id):

        """
        This object is used to get followed album with id
        """

        try:
            follow_album = Follow.objects.get(id=id,user=self.request.user)
            return follow_album
        except Follow.DoesNotExist:

            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self,request,id):

        """
        This function is used to get specified  followed album with id
        """

        follow_album = self.get_object(request,id)
        serializer = FollowSerialzier(follow_album)

        return Response(serializer.data)

    def put(self,request,id):

        """
        This function is used to update follow request on album
        """

        album = self.get_object(request,id)
        serializer = FollowSerialzier(album,data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):

        """
        This function is used to unfollow album
        """

        follow_album = self.get_object(request,id)
        follow_album.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
