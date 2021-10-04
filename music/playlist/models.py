"""
Playlist Models File
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class Song(models.Model):

    """
    This is a song model
    """

    song_name = models.CharField(max_length=100)
    time_offer = models.DateTimeField(blank=True,null=True)
    added_on = models.DateTimeField(auto_now_add=True)



    def __str__(self):

        """
        This function returns the name of the  song in
        string format it is pythons built-in function
        """
        return '{self.song_name}'.format(self=self)



class Album(models.Model):

    """
    This is Album Model it has Foreign Key relation with user and
    many to many realtion with Song mode
    """

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

        """
        This function returns the name of the  album in
        string format it is pythons built-in function
        """

        return '{self.album_name}'.format(self=self)



class Comments(models.Model):

    """
    This is Comment model it has Foreign Key Relation
    with User and Song model
    """

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    songs = models .ForeignKey(Song,on_delete=models.CASCADE,related_name='comments')
    comment = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        """
        This function returns the comment on the  song in
        string format it is pythons built-in function
        """

        return '{self.comment}'.format(self=self)


class Favorite(models.Model):

    """
    This is Favorite model it has foreign key relation with
    Song and User model
    """

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    songs = models .ForeignKey(Song,on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) :

        """
        This function returns the name of the  song in
        string format it is pythons built-in function
        """

        return '{self.songs.song_name}'.format(self=self)


class Like(models.Model):

    """
    This is Like model it has foreign key relation with
    Song and User model
    """

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    songs = models .ForeignKey(Song,on_delete=models.CASCADE)
    like_song = models.BooleanField(default=False)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) :

        """
        This function returns the name of the  song in
        string format it is pythons built-in function
        """
        return "{self.songs.song_name}".format(self=self)


class Follow(models.Model):

    """
    This is Follow model it has foreign key relation with
    Album and User model
    """

    user =  models.ForeignKey(User,on_delete=models.CASCADE)
    album  = models.ForeignKey(Album,on_delete=models.CASCADE)
    follow =  models.BooleanField(default=False)
    followed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        """
        This function returns the name of the  song in
        string format it is pythons built-in function
        """

        return  '{self.album.album_name}'.format(self=self)



# Function used to send emails this is a test email they don not send mail on gmail

@receiver(post_save, sender=Album)
def send_email( instance):

    """
    This Function is used to send email to followers of album whenever an album is updated
    """

    email_sender = instance.creater.email
    followers = Follow.objects.filter(follow=True)
    for follower in followers:

        send_mail(str( instance.album_name),'New Song added in Album',email_sender,
                [follower.user.email], fail_silently=False)
