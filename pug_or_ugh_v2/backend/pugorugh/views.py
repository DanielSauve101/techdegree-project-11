from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404


from rest_framework import (authentication, generics, 
                            mixins, permissions)
from rest_framework.response import Response

from . import models
from . import serializers


class UserRegisterView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class ListDog(generics.ListAPIView):
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    
class RetrieveDog(generics.RetrieveAPIView):
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(id__gt=self.kwargs.get('pk'))
        return queryset

    def get_object(self):
        queryset = self.get_queryset()
        if len(queryset) == 0:
            raise Http404()
        else:
            object = queryset.first()
            return object


class UpdateDogStatus(generics.UpdateAPIView):
    queryset = models.UserDog.objects.all()
    serializer_class = serializers.UserDogSerializer


class RetrieveUpdateUserPref(generics.RetrieveUpdateAPIView, mixins.CreateModelMixin):
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer

    def get_object(self):
        queryset = self.get_queryset()
        try:
            obj = queryset.get(user=self.request.user)
        except ObjectDoesNotExist:
            obj = queryset.create(user=self.request.user)
        return obj

