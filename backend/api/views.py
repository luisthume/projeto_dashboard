from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from django_filters import rest_framework as filters
from rest_framework.exceptions import APIException

from .serializers import XMLSerializer, NFeSerializer, UserSerializer, DataSerializer

from .models import XMLFile, NFe, User

from .permissions import IsSuperUser, IsOwner

from .filters import XMLFileFilter, DatasFilter

from .pagination import CustomPagination
# Create your views here.

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class UsersAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsSuperUser,)
    #filter_class = UserFilter
    filter_backends = (filters.DjangoFilterBackend,)


class UserAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsSuperUser,)


class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class Login(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.name + ' ' + user.last_name
        })


class XMLsAPIView(generics.ListCreateAPIView):
    queryset = XMLFile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = XMLSerializer
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    filter_class = XMLFileFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def list(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            queryset = XMLFile.objects.all()
            serializer = XMLSerializer(queryset, many=True)
            return Response(serializer.data)

        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(user=self.request.user)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        """checa se o post data está em um array se não inicia normal"""
        data = request.data.get("items") if "items" in request.data else request.data
        
        value_list = []
    
        xmls = len(data.getlist('xml'))

        if xmls == 0:
            return Response("Not found 'xml' field", status=status.HTTP_403_FORBIDDEN)

        for i in range(xmls):
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
    permission_classes = (IsOwner,)
    search_fields = ['id']
    filter_backends = (filters.DjangoFilterBackend,)


class NFesAPIView(generics.ListAPIView):
    queryset = NFe.objects.all()
    serializer_class = NFeSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)

    def list(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            queryset = XMLFile.objects.all()
            serializer = XMLSerializer(queryset, many=True)
            return Response(serializer.data)

        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(user=self.request.user)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)    

    def get_queryset(self):
        if self.kwargs.get('nfe_pk'):
            return self.queryset.filter(company_id = self.kwargs.get('nfe_pk'))
        return self.queryset.all()


class NFeAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NFe.objects.all()
    serializer_class = NFeSerializer
    permission_classes = (IsOwner,)


class DatasAPIView(generics.ListAPIView):
    queryset = NFe.objects.all()
    serializer_class = DataSerializer
    permission_classes = (IsAuthenticated,)
    filter_class = DatasFilter
    filter_backends = (filters.DjangoFilterBackend,)
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            queryset = NFe.objects.all()
            serializer = NFeSerializer(queryset, many=True)
            return Response(serializer.data)

        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(user=self.request.user)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        if self.kwargs.get('nfe_pk'):
            return self.queryset.filter(company_id = self.kwargs.get('nfe_pk'))
        return self.queryset.all()