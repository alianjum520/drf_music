from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,

)




urlpatterns = [

    path('register/',RegisterUser.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/',TokenRefreshView.as_view(), name='token_refresh')

]