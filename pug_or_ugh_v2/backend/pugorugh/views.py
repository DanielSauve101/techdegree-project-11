from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.db.models import Q

from rest_framework import (authentication, generics, 
                            mixins, permissions)
from rest_framework.response import Response

from pugorugh.models import Dog, UserPref, UserDog
from pugorugh.serializers import (DogSerializer, UserSerializer,
                                  UserPrefSerializer, UserDogSerializer)

def retrieve_single_dog(dogs, pk):
    try:
        dog = dogs.filter(id__gt=pk)[:1].get()
    except ObjectDoesNotExist:
        dog = dogs.first()
    return dog

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
    serializer_class = UserSerializer


class ListDogView(generics.ListAPIView):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer

    
class RetrieveDogView(generics.RetrieveAPIView):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer

    def get_queryset(self):
        preference = UserPref.objects.get(
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
                Q(userdog__isnull=True) | Q(userdog__status='u')
            )
            dog = retrieve_single_dog(dogs, pk)
            return dog
        elif decision == 'liked':
            dogs = queryset.filter(
                userdog__status='l'
            )
            dog = retrieve_single_dog(dogs, pk)
            return dog
        elif decision == 'disliked':
            dogs = queryset.filter(
                userdog__status='d'
            )
            dog = retrieve_single_dog(dogs, pk)
            return dog


class UpdateDogStatusView(generics.UpdateAPIView):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer

    def put(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        status = self.kwargs.get('decision')
        dog = Dog.objects.get(id=pk)

        try:
            obj = UserDog.objects.get(
                user=self.request.user,
                dog=dog)
        except ObjectDoesNotExist:
            obj = UserDog.objects.create(
                user=self.request.user,
                dog=dog,
                status=status[0])
        else:
            obj.status = status[0]
            obj.save()

        dog_object = DogSerializer(dog)
        return Response(dog_object.data)


class RetrieveUpdateUserPrefView(generics.RetrieveUpdateAPIView):
    queryset = UserPref.objects.all()
    serializer_class = UserPrefSerializer

    def get_object(self):
        queryset = self.get_queryset()
        try:
            obj = queryset.get(user=self.request.user)
        except ObjectDoesNotExist:
            obj = queryset.create(user=self.request.user)
        return obj

