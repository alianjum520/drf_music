from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator



# Create your models here.


class UserProfile(models.Model):

    """
    This is the User Profile class this creates the table of End User
    This class has the one to one relation with Django auth users
    This extends the user class
    """

    user = models.OneToOneField(User,related_name='profile',on_delete=models.CASCADE)
    phone = models.CharField(blank=True,max_length=20)
    age = models.IntegerField(
            validators=[
            MaxValueValidator(100),
            MinValueValidator(10)
        ],
        blank=True,null=True
        )

    def __str__(self):

        """
        This is the dunder method of python which returns
        the vlaue in string

        Returns:
            [string]: [Returns the username of the user]
        """

        return self.user.username

    @property
    def full_name(self):

        """
        This method is used to return the full name of the user

        Returns:
            [string]: [Returns the full name of the user]
        """

        return f"{self.user.first_name} {self.user.last_name}"

    def user_email(self):

        return f'{self.user.email}'
