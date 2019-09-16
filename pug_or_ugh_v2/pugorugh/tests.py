from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from pugorugh.models import Dog, UserPref, UserDog
from pugorugh.views import (UserRegisterView, RetrieveDogView,
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

        self.test_dog2 = Dog.objects.create(
            name='test_dog2',
            image_filename='2.jpg',
            breed='lab',
            age=25,
            gender='m',
            size='m'
        )

        self.test_user_pref = UserPref.objects.create(
            user=self.test_user,
            age='b,y,a,s',
            gender='f,m',
            size='s,m,l'
        )

        self.test_user_dog = UserDog.objects.create(
            user=self.test_user,
            dog=self.test_dog,
            status='u'
        )

        self.test_user_dog = UserDog.objects.create(
            user=self.test_user,
            dog=self.test_dog2,
            status='l'
        )

    def test_user_register_view(self):
        self.client.post(reverse('register-user'),
                        {'username': 'Testing123',
                        'password': 'testing'})
        test = User.objects.get(username='Testing123')
        self.assertEqual(User.objects.count(), 2)
        self.assertTrue(test)
            
    def test_retrieve_unknown_dog_view(self):
        factory = APIRequestFactory()
        request = factory.get(reverse('dog-decision',
                              kwargs={'pk': 1, 'decision': 'unknown'}))
        force_authenticate(request, user=self.test_user)
        view = RetrieveDogView.as_view()
        resp = view(request, pk='1', decision='unknown')
        self.assertEqual(resp.status_code, 200)

    def test_retrieve_liked_dog_view(self):
        factory = APIRequestFactory()
        request = factory.get(reverse('dog-decision',
                                      kwargs={'pk': 2, 'decision': 'liked'}))
        force_authenticate(request, user=self.test_user)
        view = RetrieveDogView.as_view()
        resp = view(request, pk='2', decision='liked')
        self.assertEqual(resp.status_code, 200)

    def test_update_dog_status_view(self):
        factory = APIRequestFactory()
        request = factory.put(reverse('dog-status',
                                      kwargs={'pk': 1, 'decision': 'liked'}))
        force_authenticate(request, user=self.test_user)
        view = UpdateDogStatusView.as_view()
        resp = view(request, pk='1', decision='liked')
        self.assertEqual(resp.status_code, 200)

    def test_get_user_preferences_update(self):
        factory = APIRequestFactory()
        request = factory.get(reverse('user-pref'))
        force_authenticate(request, user=self.test_user)
        view = RetrieveUpdateUserPrefView.as_view()
        resp = view(request)
        self.assertEqual(resp.status_code, 200)

    def test_put_user_preferences_update(self):
        factory = APIRequestFactory()
        request = factory.put(reverse('user-pref'))
        force_authenticate(request, user=self.test_user)
        view = RetrieveUpdateUserPrefView.as_view()
        resp = view(request, age='b', gender='m', size='l')
        self.assertEqual(resp.status_code, 200)

        