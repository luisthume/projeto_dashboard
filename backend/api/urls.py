from django.urls import path

from .views import (XMLsAPIView, XMLAPIView, NFesAPIView, NFeAPIView)

urlpatterns = [
    path('xmls/', XMLsAPIView.as_view(),name= 'xmls'),
    path('xmls/<int:pk>', XMLAPIView.as_view(), name='xml'),

    path('nfes/', NFesAPIView.as_view(),name= 'nfes'),
    path('nfes/<int:pk>', NFeAPIView.as_view(), name='nfe'),    
]