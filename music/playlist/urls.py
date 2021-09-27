from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('addsongs',AdminSongsViewSet)
router.register('album',AlbumViewset)


urlpatterns = [

    path('playlist/',include(router.urls)),
    path('playlist/<int:pk>/',include(router.urls)),
    path('songs/',SongView.as_view()),
    path('songs/<int:id>/',SongDetailView.as_view()),
    path('songs/<int:songs_id>/comments/',SongsAddComment.as_view()),
    path('songs/<int:songs_id>/comments/<int:id>/',SongsCommentView.as_view()),
    path('songs/fav/',AllFavView.as_view()),
    path('songs/fav/<int:id>/',SongsFavouriteView.as_view()),
    path('songs/<int:songs_id>/fav/',SongsAddFavourite.as_view()),
    path('songs/like/',LikeSong.as_view()),
    path('songs/like/<int:id>/',LikeUpdateView.as_view()),
    path('songs/<int:songs_id>/like/',AddLikeSongs.as_view()),
    path('public/album/',PublicAlbum.as_view()),
    path('public/album/<int:id>/',PublicAlbumDetail.as_view()),
    path('public/album/follow/',FollowedAlbum.as_view()),
    path('public/album/follow/<int:id>/',FollowUpdateView.as_view()),
    path('public/album/<int:album_id>/follow/',FollowAlbum.as_view()),




]