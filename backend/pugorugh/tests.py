from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from . import models


class DogModelTest(TestCase):
    def setUp(self):
        self.dog = models.Dog.objects.create(
            name='Dublido',
            image_filename='',
            breed='wild',
            age=5,
            gender='f',
            size='l'
        )

    def tearDown(self):
        self.dog.delete()

    def testCreation(self):
        dog = models.Dog.objects.get(pk=self.dog.pk)
        self.assertEqual(dog, self.dog)


class APIViewTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_superuser(
            username='admin',
            email='test@example.com',
            password='password'
        )
        Token.objects.create(
            user=cls.user
        )

    def setUp(self):
        token = Token.objects.get(user__username='admin')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.dog = models.Dog.objects.create(
            name='Dublido',
            image_filename='',
            breed='wild',
            age=5,
            gender='f',
            size='l'
        )

    def testDogRetrieveView(self):
        resp = self.client.get(reverse('next-dog',
                                       kwargs={'pk': '-1',
                                               'status': 'undecided'}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, {'id': 1,
                                     'name': 'Dublido',
                                     'image_filename': '',
                                     'breed': 'wild',
                                     'age': 5,
                                     'gender': 'f',
                                     'size': 'l'})

    def testUserDogUpdateView(self):
        resp = self.client.put(reverse('update-status',
                                       kwargs={'pk': str(self.dog.pk),
                                               'status': 'liked'}))
        self.assertEqual(resp.status_code, 200)
        status = models.UserDog.objects.get(dog=self.dog,
                                            user=self.user).status
        self.assertEqual(status, 'l')
        self.client.put(reverse('update-status',
                                kwargs={'pk': str(self.dog.pk),
                                        'status': 'undecided'}))
