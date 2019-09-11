from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404


from rest_framework import (authentication, generics, 
                            mixins, permissions)
from rest_framework.response import Response

from . import models
from . import serializers


def preferred_dog_age(preferred_age):
    age_groups = []
    b = [b for b in range(1, 13)]
    y = [y for y in range(13, 31)]
    a = [a for a in range(31, 121)]
    s = [s for s in range(121, 240)]

    if 'b' in preferred_age:
        age_groups.extend(b)
    if 'y' in preferred_age:
        age_groups.extend(y)
    if 'a' in preferred_age:
        age_groups.extend(a)
    if 's' in preferred_age:
        age_groups.extend(s)

    return age_groups

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
        preference = models.UserPref.objects.get(
            user=self.request.user)

        queryset = self.queryset.filter(
            age__in=preferred_dog_age(preference.age),
            gender__in=preference.gender,
            size__in=preference.size
        )
        return queryset

    def get_object(self):
        decision = self.kwargs.get('decision')
        pk = self.kwargs.get('pk')
        queryset = self.get_queryset()

        if decision == 'undecided':
            dogs = queryset.filter(
                userdog__isnull=True
            )
            try:
                dog = dogs.filter(id__gt=pk)[:1].get()
                print("Dog id is {}. This pk should be in the url.".format(dog.id))
            except ObjectDoesNotExist:
                dog = dogs.first()
                print("List has looped")
            return dog
        elif decision == 'liked':
            queryset = self.get_queryset().filter(
                userdog__status='l'
            )
            if len(queryset) == 0:
                raise Http404()
            else:
                object = queryset.first()
            return object
        elif decision == 'disliked':
            queryset = self.get_queryset().filter(
                userdog__status='d'
            )
            if len(queryset) == 0:
                raise Http404()
            else:
                object = queryset.first()
            return object


class UpdateDogStatus(generics.UpdateAPIView):
    queryset = models.UserDog.objects.all()
    serializer_class = serializers.UserDogSerializer

    def get_object(self):
        dog = models.Dog.objects.get(id=self.kwargs.get('pk'))
        status = self.kwargs.get('decision')

        if status == 'liked':
            status = 'l'
        else: 
            status = 'd'

        try:
            obj = self.get_queryset().get(
                user=self.request.user,
                dog=dog)
            print(obj.id)
        except ObjectDoesNotExist:
            obj = self.get_queryset().create(
                user=self.request.user,
                dog=dog,
                status=status)
        return obj


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

