from django.contrib import admin
from .models import *

# Register your models here.


class SongAdmin(admin.ModelAdmin):

    list_display=['id','song_name','time_offer','added_on']
    search_fields = ['id','song_name']
    list_filter=['song_name']


class AlbumAdmin(admin.ModelAdmin):

    list_display=['id','creater','album_name','status','created_at']
    search_fields = ['album_name','creater','id']
    list_filter=['album_name']


class CommentAdmin(admin.ModelAdmin):

    list_display=['id','user','songs','comment','added_on']
    search_fields = ['id','songs','comment']
    list_filter=['user','songs']


class FavoriteAdmin(admin.ModelAdmin):

    list_display=['id','user','songs','added_on']
    search_fields = ['songs','user']
    list_filter=['songs']


class LikeAdmin(admin.ModelAdmin):

    list_display=['id','user','songs','like_song','added_on']
    search_fields = ['songs','id','user']
    list_filter=['songs']



class FollowAdmin(admin.ModelAdmin):

    list_display=['id','user','album','follow','followed_date']
    search_fields = ['album','id','user']
    list_filter=['album']




admin.site.register(Song,SongAdmin)
admin.site.register(Album,AlbumAdmin)
admin.site.register(Comments,CommentAdmin)
admin.site.register(Favorite,FavoriteAdmin)
admin.site.register(Like,LikeAdmin)
admin.site.register(Follow,FollowAdmin)


