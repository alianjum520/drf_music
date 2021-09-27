from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

# Create your models here.


class Song(models.Model):

    song_name = models.CharField(max_length=100)
    time_offer = models.DateTimeField(blank=True,null=True)
    added_on = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.song_name



class Album(models.Model):

    PRIVATE = 'private'
    PUBLIC = 'public'
    STATUS = (
        (PRIVATE,'private'),
        (PUBLIC, 'public')
    )
    creater = models.ForeignKey(User,related_name = 'creater',on_delete=models.CASCADE)
    album_name = models.CharField(max_length=100)
    status = models.CharField(max_length=100,choices=STATUS,default=PUBLIC)
    song = models.ManyToManyField(Song,related_name='songs',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.album_name



class Comments(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    songs = models .ForeignKey(Song,on_delete=models.CASCADE,related_name='comments')
    comment = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.comment


class Favorite(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    songs = models .ForeignKey(Song,on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) :

        return self.songs.song_name


class Like(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    songs = models .ForeignKey(Song,on_delete=models.CASCADE)
    like_song = models.BooleanField(default=False)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) :

        return self.songs.song_name


class Follow(models.Model):

    user =  models.ForeignKey(User,on_delete=models.CASCADE)
    album  = models.ForeignKey(Album,on_delete=models.CASCADE)
    follow =  models.BooleanField(default=False)
    followed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return  self.album.album_name



# Function used to send emails this is a test email they don not send mail on gmail 

@receiver(post_save, sender=Album)
def SendEmail(sender , instance, **kwargs):


        email_sender = instance.creater.email
        followers = Follow.objects.filter(follow=True)
        for followers in followers:

            send_mail(str( instance.album_name),'New Song added in Album',email_sender, [followers.user.email], fail_silently=False)