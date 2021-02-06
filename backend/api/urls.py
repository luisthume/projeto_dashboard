from django.urls import path

from .views import (XMLsAPIView, XMLAPIView, NFesAPIView, NFeAPIView, UserCreate, UserAPIView, UsersAPIView, DatasAPIView, Login, Logout, DatasCSVAPIView)

from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('signup/', UserCreate.as_view()),
    path('login/', Login.as_view()),
    path('logout/', Logout.as_view()),

    path('users/', UsersAPIView.as_view(), name='users'),
    path('users/<int:pk>/', UserAPIView.as_view(), name='user'),

    path('xmls/', XMLsAPIView.as_view(),name= 'xmls'),
    path('xmls/<int:pk>', XMLAPIView.as_view(), name='xml'),

    path('nfes/', NFesAPIView.as_view(),name= 'nfes'),
    path('nfes/<int:pk>', NFeAPIView.as_view(), name='nfe'),    

    path('datas/', DatasAPIView.as_view(),name= 'datas'),

    path('datasCSV/', DatasCSVAPIView.as_view(),name= 'datasCSV'),
]