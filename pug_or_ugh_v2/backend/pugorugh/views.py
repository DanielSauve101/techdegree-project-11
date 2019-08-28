from django.contrib.auth import get_user_model

from rest_framework import mixins, permissions, viewsets
from rest_framework.generics import CreateAPIView

from . import models
from . import serializers



class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class DogViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer