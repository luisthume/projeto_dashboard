from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from django_filters import rest_framework as filters

from .serializers import (XMLSerializer, NFeSerializer)

from .models import (XMLFile, NFe)

# Create your views here.

class XMLsAPIView(generics.ListCreateAPIView):
    queryset = XMLFile.objects.all()
    serializer_class = XMLSerializer
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    search_fields = ['id']
    filter_backends = (filters.DjangoFilterBackend,)

    def create(self, request, *args, **kwargs):
        """checa se o post data está em um array se não inicia normal"""
        data = request.data.get("items") if "items" in request.data else request.data
        
        value_list = []
    
        for i in range(len(data.getlist('xml'))):
            values = {}
            for key in data.keys():

                lista = data.getlist(key)

                if i < len(lista):
                    values[key] = lista[i]

            value_list.append(values)

        many = isinstance(data.getlist('xml'), list)
        serializer = self.get_serializer(data=value_list, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class XMLAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = XMLFile.objects.all()
    serializer_class = XMLSerializer
    permission_classes = (AllowAny,)
    search_fields = ['id']
    filter_backends = (filters.DjangoFilterBackend,)


class NFesAPIView(generics.ListCreateAPIView):
    queryset = NFe.objects.all()
    serializer_class = NFeSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.DjangoFilterBackend,)

    def get_queryset(self):
        if self.kwargs.get('nfe_pk'):
            return self.queryset.filter(company_id = self.kwargs.get('nfe_pk'))
        return self.queryset.all()


class NFeAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NFe.objects.all()
    serializer_class = NFeSerializer
    permission_classes = (AllowAny,)  