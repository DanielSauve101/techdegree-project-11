from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from pugorugh.models import Dog, UserPref, UserDog
from pugorugh.views import (UserRegisterView, ListDogView, RetrieveDogView,
                            UpdateDogStatusView, RetrieveUpdateUserPrefView)
from pugorugh.serializers import (DogSerializer, UserSerializer,
                                  UserPrefSerializer, UserDogSerializer)

class ViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.test_user = User.objects.create_user(
            username='test_user',
            email='test@gmail.com',
            password='test123'
        )

        self.test_dog = Dog.objects.create(
            name='test_dog',
            image_filename='1.jpg',
            breed='retriever',
            age=32,
            gender='f',
            size='l'
        )

        self.test_user_pref = UserPref.objects.create(
            user=self.test_user,
            age='a',
            gender='f',
            size='l'
        )

        self.test_user_dog = UserDog.objects.create(
            user=self.test_user,
            dog=self.test_dog,
            status='l'
        )

        def test_user_register_view(self):
            self.client.post(reverse('register-user'),
                            {'username': 'Testing123',
                            'password': 'testing'})
            test = User.objects.get(username='Testing123')
            self.assertEqual(User.objects.count(), 2)
            self.assertTrue(test)

        