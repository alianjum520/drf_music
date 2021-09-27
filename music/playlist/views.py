from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from .serializers import *
from .models import *
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.

class AdminSongsViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAdminUser]
    queryset = Song.objects.all()
    serializer_class = AdminSongSerializer



class SongView(GenericAPIView,mixins.ListModelMixin):

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

        return self.list(request)



class SongDetailView(APIView):

    permission_classes = [AllowAny]

    def get(self,request,id):

        try:
            song = Song.objects.get(id=id)
            serializer = SongDetailSerializer(song)

            return Response(serializer.data)

        except Song.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)



class SongsAddComment(APIView):

    permission_classes = [IsAuthenticated]


    def get(self,request,songs_id):

        comment = Comments.objects.filter(songs__id=songs_id)
        if comment.exists():
            serializer = AddCommentSerializer(comment, many = True)
            return Response(serializer.data)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self,request,songs_id):
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

    permission_classes = [IsAuthenticated]

    def get_object(self,request,songs_id,id):

        try:
            songs = Comments.objects.get(songs__id=songs_id,id=id,user=self.request.user)
            return songs
        except Comments.DoesNotExist:

            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self,request,songs_id,id):

        songs = self.get_object(request,songs_id,id)
        serializer = AddCommentSerializer(songs)

        return Response(serializer.data)

    def put(self,request,songs_id,id):

        songs = self.get_object(request,songs_id,id)
        serializer = AddCommentSerializer(songs,data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self,request,songs_id,id):

        comment = self.get_object(request,songs_id,id)
        comment.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)



class AllFavView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request):

        fav = Favorite.objects.filter(user = self.request.user)
        if fav.exists():
            serializer = FavouriteSerialzier(fav, many = True)
            return Response(serializer.data)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)



class SongsAddFavourite(APIView):

    permission_classes = [IsAuthenticated]


    def get(self,request,songs_id):

        fav = Favorite.objects.filter(songs__id=songs_id,user = self.request.user)
        if fav.exists():
            serializer = FavouriteSerialzier(fav, many = True)
            return Response(serializer.data)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self,request,songs_id):
        songs = Song.objects.get(id= songs_id)
        user = self.request.user
        new_fav = Favorite.objects.create(songs = songs,user=user)
        serializer = FavouriteSerialzier(new_fav, data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



class SongsFavouriteView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self,request,id):

        try:
            fav_songs = Favorite.objects.get(id=id,user=self.request.user)
            return fav_songs
        except Favorite.DoesNotExist:

            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self,request,id):

        fav_songs = self.get_object(request,id)
        serializer = FavouriteSerialzier(fav_songs)

        return Response(serializer.data)

    def delete(self,request,id):

        fav_song = self.get_object(request,id)
        fav_song.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)




class LikeSong(APIView):

    permission_classes =[IsAuthenticated]

    def get(self,request):

        like_song = Like.objects.filter(user = self.request.user)
        if like_song.exists():
            serializer = LikeSerialzier(like_song, many = True)
            return Response(serializer.data)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class AddLikeSongs(APIView):

    permission_classes = [IsAuthenticated]


    def get(self,request,songs_id):

        like_song = Like.objects.filter(songs__id=songs_id,user = self.request.user)
        if like_song.exists():
            serializer = LikeSerialzier(like_song, many = True)
            return Response(serializer.data)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self,request,songs_id):
        like_song = Song.objects.get(id= songs_id)
        user = self.request.user
        new_like = Like.objects.create(songs = like_song,user=user)
        serializer = LikeSerialzier(new_like, data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



class LikeUpdateView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self,request,id):

        try:
            like_song = Like.objects.get(id=id,user=self.request.user)
            return like_song
        except Like.DoesNotExist:

            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self,request,id):

        like_song = self.get_object(request,id)
        serializer = LikeSerialzier(like_song)

        return Response(serializer.data)

    def put(self,request,id):

        songs = self.get_object(request,id)
        serializer = LikeSerialzier(songs,data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):

        like_song = self.get_object(request,id)
        like_song.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)



class AlbumViewset(viewsets.ModelViewSet):

    permission_classes= [IsAuthenticated]
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(creater=self.request.user)
        return query_set



class PublicAlbum(APIView):

    permission_classes = [AllowAny]

    def get(self,request):

        album = Album.objects.filter(status = "public")
        if album.exists():
            serializer = PublicAlbumSerializer(album, many = True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)



class PublicAlbumDetail(APIView):

    permission_classes = [AllowAny]

    def get(self,request,id):

        album = Album.objects.filter(id=id,status = "public")
        if album.exists():
            serializer = AlbumSerializer(album, many = True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)



class FollowedAlbum(APIView):

    permission_classes =[IsAuthenticated]

    def get(self,request):

        follow_album = Follow.objects.filter(user = self.request.user)
        if follow_album.exists():
            serializer = LikeSerialzier(follow_album, many = True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)



class FollowAlbum(APIView):

    permission_classes = [IsAuthenticated]


    def get(self,request,album_id):

        follow_album = Follow.objects.filter(album__id=album_id,user = self.request.user)
        if follow_album.exists():
            serializer = FollowSerialzier(follow_album, many = True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self,request,album_id):
        follow_album = Album.objects.get(id= album_id)
        user = self.request.user
        follow = Follow.objects.create(album = follow_album,user=user)
        serializer = FollowSerialzier(follow, data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



class FollowUpdateView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self,request,id):

        try:
            follow_album = Follow.objects.get(id=id,user=self.request.user)
            return follow_album
        except Follow.DoesNotExist:

            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self,request,id):

        follow_album = self.get_object(request,id)
        serializer = FollowSerialzier(follow_album)

        return Response(serializer.data)

    def put(self,request,id):

        album = self.get_object(request,id)
        serializer = FollowSerialzier(album,data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):

        follow_album = self.get_object(request,id)
        follow_album.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

