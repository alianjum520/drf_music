from django.contrib import admin
from .models import UserProfile

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):

    list_display=['user','user_email','full_name','phone','age']
    search_fields = ['user','phone']
    list_filter=['user']

admin.site.register(UserProfile,UserProfileAdmin)